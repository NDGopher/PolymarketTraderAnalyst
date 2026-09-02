from __future__ import annotations

import threading
import time
import tkinter as tk
from datetime import datetime, timezone
from tkinter import messagebox, scrolledtext, ttk

from suspension_lab.config import LabConfig
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.market_labels import MarketLabel
from suspension_lab.soccer_discovery import SoccerGame, discover_tickers_for_lab
from suspension_lab.tape_engine import TapeEngine, TapeEvent

BG = "#0e1116"
CARD = "#161b22"
INK = "#e6edf3"
MUTED = "#8b949e"
GREEN = "#3fb950"
RED = "#f85149"
AMBER = "#d29922"
LINE = "#30363d"
GOAL_BG = "#16351f"
VAR_BG = "#3d1418"
SPOOF_BG = "#3d2e10"


class SuspensionLabApp:
    def __init__(self, config: LabConfig) -> None:
        self.config = config
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
        slug = config.game_label.replace(" ", "_")[:40] if config.game_label else "session"
        session_dir = config.output_dir / f"{ts}_{slug}"
        paper_on = config.paper_enabled or True
        self.engine = TapeEngine.create(
            session_dir,
            config.tickers,
            game_label=config.game_label,
            games=list(getattr(config, "games", []) or []),
            rest_base=config.rest_base,
            paper_enabled=paper_on,
        )
        self.engine.on_event = self._queue_event
        self.logger = self.engine.logger
        self.trader = self.engine.trader
        self.feed = KalshiBookFeed(config, on_book=self._on_book, on_status=self._on_status)
        self.logger.bind_book_provider(self._books_for_log)
        self._sample_stop = threading.Event()
        self._sample_thread: threading.Thread | None = None
        self._labels = self.engine.labels
        self._ticker_boxes: dict[str, dict] = {}
        self._active_tickers: list[str] = list(config.tickers)
        self._pending_events: list[TapeEvent] = []
        self._event_lock = threading.Lock()
        self._last_rediscover = time.time()

        self.root = tk.Tk()
        self.root.title("PTA · Soccer paper tape")
        self.root.geometry("1320x900")
        self.root.configure(bg=BG, padx=12, pady=10)
        self._style()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._labels.load_all_async(on_update=self._on_label_loaded)
        self.root.after(200, self._drain_events)
        self.root.after(400, self._refresh_display)
        self.root.after(300_000, self._rediscover)

    def _style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(".", background=BG, foreground=INK, fieldbackground=CARD)
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=INK)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED)
        style.configure("Card.TFrame", background=CARD)
        style.configure("TButton", background=CARD, foreground=INK)
        style.configure("TCheckbutton", background=BG, foreground=INK)
        style.configure("TLabelframe", background=BG, foreground=INK)
        style.configure("TLabelframe.Label", background=BG, foreground=MUTED)

    def _build_ui(self) -> None:
        top = tk.Frame(self.root, bg=BG)
        top.pack(fill="x")
        tk.Label(
            top,
            text="SOCCER PAPER TAPE",
            font=("Segoe UI", 16, "bold"),
            fg=INK,
            bg=BG,
        ).pack(side="left")
        tk.Label(
            top,
            text="  PAPER ONLY · no live bets",
            font=("Segoe UI", 10),
            fg=AMBER,
            bg=BG,
        ).pack(side="left", padx=(8, 0))
        tk.Label(
            top,
            text=self.logger.session_dir.name,
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=BG,
        ).pack(side="right")

        board = tk.Frame(self.root, bg=BG)
        board.pack(fill="x", pady=(8, 6))
        self._would_var = tk.StringVar(value="Would-have  0 · +0¢")
        self._burn_var = tk.StringVar(value="Burned  0 · 0¢")
        self._open_var = tk.StringVar(value="Open  0")
        for textvar, color in (
            (self._would_var, GREEN),
            (self._burn_var, RED),
            (self._open_var, MUTED),
        ):
            tk.Label(
                board,
                textvariable=textvar,
                font=("Segoe UI", 13, "bold"),
                fg=color,
                bg=BG,
            ).pack(side="left", padx=(0, 28))

        self.status_var = tk.StringVar(value="Starting…")
        tk.Label(self.root, textvariable=self.status_var, font=("Segoe UI", 9), fg=MUTED, bg=BG).pack(
            anchor="w"
        )

        trader_row = tk.Frame(self.root, bg=BG)
        trader_row.pack(fill="x", pady=(4, 6))
        self._trader_enabled = tk.BooleanVar(value=self.trader.config.enabled)
        tk.Checkbutton(
            trader_row,
            text="Paper scalp on book GOAL (never live)",
            variable=self._trader_enabled,
            command=self._sync_trader_toggle,
            fg=INK,
            bg=BG,
            selectcolor=CARD,
            activebackground=BG,
            activeforeground=INK,
        ).pack(side="left")

        add_row = tk.Frame(self.root, bg=BG)
        add_row.pack(fill="x", pady=(0, 6))
        self._ticker_entry = tk.Entry(
            add_row, bg=CARD, fg=INK, insertbackground=INK, relief="flat", font=("Consolas", 10)
        )
        self._ticker_entry.pack(side="left", fill="x", expand=True, ipady=4)
        self._ticker_entry.insert(0, "Optional: paste extra Kalshi ticker(s)")
        self._ticker_entry.bind("<FocusIn>", self._clear_ticker_placeholder)
        tk.Button(
            add_row,
            text="Add",
            command=self._add_ticker_from_ui,
            bg=CARD,
            fg=INK,
            relief="flat",
            padx=12,
        ).pack(side="left", padx=(8, 0))

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)
        right = tk.Frame(body, bg=BG, width=380)
        right.pack(side="right", fill="y", padx=(12, 0))
        right.pack_propagate(False)

        canvas = tk.Canvas(left, bg=BG, highlightthickness=0)
        scroll = ttk.Scrollbar(left, orient="vertical", command=canvas.yview)
        self._cards = tk.Frame(canvas, bg=BG)
        self._cards.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self._cards, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        games: list[SoccerGame] = list(getattr(self.config, "games", []) or [])
        placed: set[str] = set()
        if games:
            for game in games:
                self._create_game_card(game)
                placed.update(game.get_tickers())
        leftover = [t for t in self.config.tickers if t not in placed]
        if leftover:
            self._create_loose_card(leftover)

        tk.Label(
            right,
            text="DETECTED EVENTS",
            font=("Segoe UI", 11, "bold"),
            fg=INK,
            bg=BG,
        ).pack(anchor="w")
        tk.Label(
            right,
            text="GOAL from the book · not a score feed",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(0, 4))
        self.events_text = scrolledtext.ScrolledText(
            right, height=22, font=("Consolas", 9), bg=CARD, fg=INK, relief="flat", wrap="word"
        )
        self.events_text.pack(fill="both", expand=True)
        self.events_text.configure(insertbackground=INK)
        self.events_text.tag_configure("GOAL", foreground=GREEN)
        self.events_text.tag_configure("VAR", foreground=RED)
        self.events_text.tag_configure("SPOOF", foreground=AMBER)
        self.events_text.tag_configure("SKIP", foreground=MUTED)
        self.events_text.tag_configure("EXIT", foreground=INK)
        self.events_text.tag_configure("PAPER", foreground=MUTED)

        notes = tk.LabelFrame(
            self.root,
            text="Notes (optional)",
            fg=MUTED,
            bg=BG,
            font=("Segoe UI", 9),
        )
        notes.pack(fill="x", pady=(8, 0))
        self.notes_text = scrolledtext.ScrolledText(
            notes, height=4, font=("Consolas", 9), bg=CARD, fg=INK, relief="flat"
        )
        self.notes_text.pack(fill="x", padx=4, pady=4)

    def _create_game_card(self, game: SoccerGame) -> None:
        card = tk.Frame(self._cards, bg=CARD, highlightbackground=LINE, highlightthickness=1, padx=10, pady=8)
        card.pack(fill="x", pady=(0, 10), padx=2)
        kick = (game.occurrence_time or game.close_time or "")[:16].replace("T", " ")
        head = f"{game.title}"
        tk.Label(card, text=head, font=("Segoe UI", 13, "bold"), fg=INK, bg=CARD, anchor="w").pack(fill="x")
        tk.Label(
            card,
            text=f"{kick} UTC   ·   24h vol {game.total_24h_volume:.0f}   ·   {game.series}",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=CARD,
            anchor="w",
        ).pack(fill="x", pady=(0, 6))
        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x")
        slots = [
            ("Home ML", game.home_ml_ticker),
            ("Away ML", game.away_ml_ticker),
            (game.total_atm_label or "ATM total", game.total_atm_ticker or game.over_05_ticker),
            (game.total_up_label or "ATM+1", game.total_up_ticker or game.over_15_ticker),
        ]
        for title, ticker in slots:
            self._create_book_box(row, ticker, title)

    def _create_loose_card(self, tickers: list[str]) -> None:
        card = tk.Frame(self._cards, bg=CARD, highlightbackground=LINE, highlightthickness=1, padx=10, pady=8)
        card.pack(fill="x", pady=(0, 10), padx=2)
        tk.Label(card, text="Books", font=("Segoe UI", 13, "bold"), fg=INK, bg=CARD).pack(anchor="w")
        row = tk.Frame(card, bg=CARD)
        row.pack(fill="x")
        for ticker in tickers:
            self._create_book_box(row, ticker, ticker.rsplit("-", 1)[-1])

    def _create_book_box(self, parent: tk.Widget, ticker: str | None, title: str) -> None:
        box = tk.Frame(parent, bg=BG, highlightbackground=LINE, highlightthickness=1, padx=8, pady=6)
        box.pack(side="left", fill="both", expand=True, padx=3)
        if not ticker:
            tk.Label(box, text=f"{title}\n—", fg=MUTED, bg=BG, font=("Segoe UI", 9), justify="left").pack()
            return
        name = tk.Label(box, text=title, font=("Segoe UI", 10, "bold"), fg=INK, bg=BG, anchor="w")
        name.pack(fill="x")
        sub = tk.Label(box, text=ticker.rsplit("-", 1)[-1], font=("Consolas", 8), fg=MUTED, bg=BG, anchor="w")
        sub.pack(fill="x")
        body = tk.Label(box, text="Waiting…", font=("Consolas", 9), fg=INK, bg=BG, justify="left", anchor="w")
        body.pack(fill="x", pady=(4, 0))
        banner = tk.Label(box, text="", font=("Segoe UI", 8, "bold"), fg=INK, bg=BG, anchor="w")
        self._ticker_boxes[ticker] = {
            "box": box,
            "title": name,
            "subtitle": sub,
            "body": body,
            "banner": banner,
        }

    def _sync_trader_toggle(self) -> None:
        self.trader.config.enabled = self._trader_enabled.get()
        self.trader.config.live = False

    def _clear_ticker_placeholder(self, _event=None) -> None:
        if self._ticker_entry.get().startswith("Optional:"):
            self._ticker_entry.delete(0, tk.END)

    def _add_ticker_from_ui(self) -> None:
        raw = self._ticker_entry.get().strip()
        if not raw or raw.startswith("Optional:"):
            return
        parts = [p.strip() for p in raw.replace("\n", ",").split(",") if p.strip()]
        added = 0
        new: list[str] = []
        for ticker in parts:
            if ticker in self._ticker_boxes:
                continue
            if not self.feed.add_ticker(ticker):
                continue
            self.logger.register_ticker(ticker)
            self._labels.register_ticker(ticker)
            self._active_tickers.append(ticker)
            new.append(ticker)
            added += 1
        if added:
            self._create_loose_card(new)
            self._ticker_entry.delete(0, tk.END)
            for ticker in new:
                self._labels.fetch_one_async(ticker, on_update=self._on_label_loaded)
        else:
            messagebox.showinfo("Add ticker", "Ticker already tracked or invalid.")

    def _books_for_log(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for t, book in self.feed.books.items():
            levels = book.top_levels()
            levels["book_json"] = book.full_json()
            out[t] = levels
        return out

    def _on_book(self, ticker: str, book) -> None:
        self.engine.handle_book(ticker, book)

    def _queue_event(self, event: TapeEvent) -> None:
        with self._event_lock:
            self._pending_events.append(event)

    def _drain_events(self) -> None:
        with self._event_lock:
            pending = list(self._pending_events)
            self._pending_events.clear()
        for event in pending:
            self.events_text.insert(tk.END, f"{event.ts_iso[11:19]}  {event.kind:5}  {event.detail}\n", event.kind)
            self.events_text.see(tk.END)
            box = self._ticker_boxes.get(event.ticker)
            if box:
                colors = {
                    "GOAL": (GREEN, GOAL_BG),
                    "VAR": (RED, VAR_BG),
                    "SPOOF": (AMBER, SPOOF_BG),
                    "SKIP": (MUTED, BG),
                    "EXIT": (INK, BG),
                }
                fg, bg = colors.get(event.kind, (INK, BG))
                box["banner"].config(text=f"{event.kind}: {event.detail[:80]}", fg=fg, bg=bg)
                box["banner"].pack(fill="x", pady=(4, 0))
                box["box"].config(highlightbackground=fg, highlightthickness=2)
        self._refresh_scoreboard()
        self.root.after(200, self._drain_events)

    def _refresh_scoreboard(self) -> None:
        b = self.trader.scoreboard()
        self._would_var.set(
            f"Would-have  {b['would_have_count']} · {b['would_have_pnl_cents']:+d}¢  [paper]"
        )
        self._burn_var.set(f"Burned  {b['burned_count']} · {b['burned_pnl_cents']:+d}¢")
        self._open_var.set(f"Open  {b['open']}")

    def _on_label_loaded(self, ticker: str, label: MarketLabel) -> None:
        self.root.after(0, lambda: self._apply_label(ticker, label))

    def _apply_label(self, ticker: str, label: MarketLabel) -> None:
        box = self._ticker_boxes.get(ticker)
        if box:
            if label.line:
                box["title"].config(text=label.line)
            box["subtitle"].config(text=label.display[:48])

    def _on_status(self, msg: str) -> None:
        self.root.after(0, lambda: self.status_var.set(msg))

    def _format_book(self, lv: dict) -> str:
        return (
            f"YES {lv.get('yes_bid', '?')} x {lv.get('yes_bid_qty', '?')}\n"
            f"    {lv.get('yes_ask', '?')} x {lv.get('yes_ask_qty', '?')}\n"
            f"NO  {lv.get('no_bid', '?')} / {lv.get('no_ask', '?')}\n"
            f"spr {lv.get('spread_cents', '?')}¢"
        )

    def _refresh_display(self) -> None:
        for ticker, book in self.feed.books.items():
            box = self._ticker_boxes.get(ticker)
            if not box:
                continue
            box["body"].config(text=self._format_book(book.top_levels()))
        self.root.after(250, self._refresh_display)

    def _rediscover(self) -> None:
        def _run() -> None:
            try:
                tickers, _log, games = discover_tickers_for_lab(
                    rest_base=self.config.rest_base, max_games=8
                )
            except Exception:  # noqa: BLE001
                self.root.after(300_000, self._rediscover)
                return
            self.root.after(0, lambda: self._absorb_discovery(tickers, games))

        threading.Thread(target=_run, name="rediscover", daemon=True).start()

    def _absorb_discovery(self, tickers: list[str], games: list[SoccerGame]) -> None:
        new_games = [g for g in games if not any(t in self._ticker_boxes for t in g.get_tickers())]
        for game in new_games:
            added = []
            for ticker in game.get_tickers():
                if ticker in self._ticker_boxes:
                    continue
                if self.feed.add_ticker(ticker):
                    self.logger.register_ticker(ticker)
                    self._labels.register_ticker(ticker)
                    self._active_tickers.append(ticker)
                    added.append(ticker)
            if added:
                self._create_game_card(game)
                self.engine.games.append(game)
                for ticker in added:
                    self._labels.fetch_one_async(ticker, on_update=self._on_label_loaded)
                self.events_text.insert(tk.END, f"AUTO-FUND  {game.title}\n", "PAPER")
        self.root.after(300_000, self._rediscover)

    def _sample_loop(self) -> None:
        interval = max(self.config.poll_ms, 100) / 1000.0
        while not self._sample_stop.is_set():
            books = self._books_for_log()
            if books:
                self.logger.log_book_sample(books)
            time.sleep(interval)

    def run(self) -> None:
        self.feed.start()
        self._sample_stop.clear()
        self._sample_thread = threading.Thread(target=self._sample_loop, daemon=True)
        self._sample_thread.start()
        self.root.mainloop()

    def _on_close(self) -> None:
        notes_preview = self.notes_text.get("1.0", tk.END).strip()
        choice = messagebox.askyesnocancel(
            "End session",
            f"Session: {self.logger.session_dir.name}\n"
            f"Would-have: {self.trader.would_have_count}  Burned: {self.trader.burned_count}\n\n"
            "Yes = Save logs\nNo = Delete session\nCancel = Keep running",
        )
        if choice is None:
            return
        self._sample_stop.set()
        self.feed.stop()
        if choice:
            self.logger.finalize(saved=True, notes_text=notes_preview)
            messagebox.showinfo("Session saved", f"Logs saved to:\n{self.logger.session_dir}")
        else:
            folder = self.logger.session_dir
            self.logger.delete_session()
            messagebox.showinfo("Session deleted", f"Removed:\n{folder}")
        self.root.destroy()


def run_app(config: LabConfig) -> None:
    app = SuspensionLabApp(config)
    app.run()
