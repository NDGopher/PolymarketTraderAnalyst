from __future__ import annotations

import threading
import time
import tkinter as tk
from datetime import datetime, timezone
from tkinter import messagebox, scrolledtext, ttk

from suspension_lab.config import BOND_MID_THRESHOLD, GOAL_HIGHLIGHT_SECONDS, LabConfig
from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.market_labels import MarketLabel, MarketLabelCache
from suspension_lab.session import SessionLogger

GOAL_BORDER = "#16a34a"
GOAL_BORDER_WIDTH = 6
IDLE_BORDER = "#d1d5db"
IDLE_BORDER_WIDTH = 2


class SuspensionLabApp:
    def __init__(self, config: LabConfig) -> None:
        self.config = config
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
        slug = config.game_label.replace(" ", "_")[:40] if config.game_label else "session"
        session_dir = config.output_dir / f"{ts}_{slug}"
        self.logger = SessionLogger(session_dir, config.tickers, game_label=config.game_label)
        self.feed = KalshiBookFeed(config, on_book=self._on_book, on_status=self._on_status)
        self.logger.bind_book_provider(self._books_for_log)
        self._book_cache: dict[str, dict] = {}
        self._sample_stop = threading.Event()
        self._sample_thread: threading.Thread | None = None
        self._goal_detector = GoalSignalDetector()
        self._labels = MarketLabelCache(config.tickers, rest_base=config.rest_base)
        self._highlight_until: dict[str, float] = {}
        self._ticker_panels: dict[str, dict] = {}

        self.root = tk.Tk()
        self.root.title("Suspension Edge Lab")
        self.root.geometry("1040x780")
        self.root.configure(padx=8, pady=8)
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<KeyPress-b>", lambda _e: self._toggle("b365"))
        self.root.bind("<KeyPress-B>", lambda _e: self._toggle("b365"))
        self.root.bind("<KeyPress-f>", lambda _e: self._toggle("fanduel"))
        self.root.bind("<KeyPress-F>", lambda _e: self._toggle("fanduel"))
        self.root.bind("<KeyPress-d>", lambda _e: self._toggle("draftkings"))
        self.root.bind("<KeyPress-D>", lambda _e: self._toggle("draftkings"))

        self._labels.load_all_async(on_update=self._on_label_loaded)

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text=f"Game: {self.config.game_label or '(unnamed)'}").pack(side="left")
        ttk.Label(top, text=f"Session: {self.logger.session_dir.name}").pack(side="right")

        self.status_var = tk.StringVar(value="Starting…")
        ttk.Label(self.root, textvariable=self.status_var, foreground="#444").pack(anchor="w")

        books_frame = ttk.LabelFrame(self.root, text="Kalshi orderbooks (live)")
        books_frame.pack(fill="both", expand=True, pady=8)

        outer = ttk.Frame(books_frame)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        self._books_scroll = ttk.Frame(canvas)
        self._books_scroll.bind(
            "<Configure>",
            lambda _e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=self._books_scroll, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for ticker in self.config.tickers:
            self._create_ticker_panel(ticker)

        flags_frame = ttk.LabelFrame(self.root, text="Book flags - click or press B / F / D")
        flags_frame.pack(fill="x", pady=4)
        self.b365_var = tk.StringVar(value="UP")
        self.fd_var = tk.StringVar(value="UP")
        self.dk_var = tk.StringVar(value="UP")

        btn_row = ttk.Frame(flags_frame)
        btn_row.pack(fill="x", pady=4)
        ttk.Button(btn_row, text="B365 toggle (B)", command=lambda: self._toggle("b365"), width=18).pack(
            side="left", padx=4
        )
        ttk.Label(btn_row, textvariable=self.b365_var, width=8, font=("Consolas", 12, "bold")).pack(side="left")
        ttk.Button(btn_row, text="FanDuel toggle (F)", command=lambda: self._toggle("fanduel"), width=18).pack(
            side="left", padx=12
        )
        ttk.Label(btn_row, textvariable=self.fd_var, width=8, font=("Consolas", 12, "bold")).pack(side="left")
        ttk.Button(btn_row, text="DraftKings (D)", command=lambda: self._toggle("draftkings"), width=16).pack(
            side="left", padx=12
        )
        ttk.Label(btn_row, textvariable=self.dk_var, width=8, font=("Consolas", 12, "bold")).pack(side="left")

        log_frame = ttk.LabelFrame(self.root, text="Event log")
        log_frame.pack(fill="both", expand=True, pady=4)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

        help_text = (
            "B = bet365 · F = FanDuel · D = DraftKings · "
            f"Green box = bid jump goal signal (≥10¢ + size) · Bond skip: {BOND_MID_THRESHOLD:.0%}"
        )
        ttk.Label(self.root, text=help_text, foreground="#666").pack(anchor="w", pady=(4, 0))

    def _create_ticker_panel(self, ticker: str) -> None:
        label = self._labels.get(ticker)
        border = tk.Frame(
            self._books_scroll,
            highlightthickness=IDLE_BORDER_WIDTH,
            highlightbackground=IDLE_BORDER,
            highlightcolor=GOAL_BORDER,
            bd=0,
            padx=6,
            pady=6,
        )
        border.pack(fill="x", padx=4, pady=6)

        title = tk.Label(
            border,
            text=label.display,
            font=("Segoe UI", 11, "bold"),
            anchor="w",
            justify="left",
        )
        title.pack(fill="x")

        subtitle = tk.Label(
            border,
            text=ticker,
            font=("Segoe UI", 8),
            fg="#666",
            anchor="w",
        )
        subtitle.pack(fill="x")

        body = tk.Label(
            border,
            text="Waiting for book…",
            font=("Consolas", 10),
            anchor="w",
            justify="left",
        )
        body.pack(fill="x", pady=(4, 0))

        signal_banner = tk.Label(
            border,
            text="",
            font=("Segoe UI", 10, "bold"),
            fg="#166534",
            bg="#dcfce7",
            anchor="w",
            padx=6,
            pady=4,
        )

        self._ticker_panels[ticker] = {
            "border": border,
            "title": title,
            "subtitle": subtitle,
            "body": body,
            "signal_banner": signal_banner,
        }

    def _on_label_loaded(self, ticker: str, label: MarketLabel) -> None:
        self.root.after(0, lambda: self._apply_label(ticker, label))

    def _apply_label(self, ticker: str, label: MarketLabel) -> None:
        panel = self._ticker_panels.get(ticker)
        if not panel:
            return
        panel["title"].config(text=label.display)
        panel["subtitle"].config(text=label.ticker)

    def _books_for_log(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for t, book in self.feed.books.items():
            levels = book.top_levels()
            levels["book_json"] = book.full_json()
            out[t] = levels
        return out

    def _on_book(self, ticker: str, book) -> None:
        signal = self._goal_detector.evaluate(ticker, book)
        if signal:
            self.root.after(0, lambda s=signal: self._on_goal_signal(s))
        self.root.after(0, self._refresh_display)

    def _on_goal_signal(self, signal: GoalSignal) -> None:
        label = self._labels.get(signal.ticker)
        self._highlight_until[signal.ticker] = time.time() + GOAL_HIGHLIGHT_SECONDS
        panel = self._ticker_panels.get(signal.ticker)
        if panel:
            banner: tk.Label = panel["signal_banner"]
            banner.config(
                text=f"⚽ GOAL SIGNAL — {signal.summary}",
            )
            banner.pack(fill="x", pady=(6, 0))
            panel["border"].config(
                highlightbackground=GOAL_BORDER,
                highlightthickness=GOAL_BORDER_WIDTH,
            )
        self.logger.log_goal_signal(
            ticker=signal.ticker,
            market_label=label.display,
            prev_bid=f"{signal.prev_bid:.4f}",
            new_bid=f"{signal.new_bid:.4f}",
            bid_jump_cents=signal.bid_jump_cents,
            bid_qty=f"{signal.bid_qty:.2f}",
            prev_ask=f"{signal.prev_ask:.4f}" if signal.prev_ask is not None else "",
            new_ask=f"{signal.new_ask:.4f}" if signal.new_ask is not None else "",
            reason=signal.reason,
            ts_ms=signal.ts_ms,
        )
        msg = f"{label.display}\n{signal.summary}"
        self.log_text.insert(tk.END, f"GOAL SIGNAL @ {datetime.now().strftime('%H:%M:%S.%f')[:-3]} — {msg}\n")
        self.log_text.see(tk.END)
        try:
            self.root.bell()
        except tk.TclError:
            pass

    def _on_status(self, msg: str) -> None:
        self.root.after(0, lambda: self.status_var.set(msg))

    def _refresh_display(self) -> None:
        now = time.time()
        for ticker in self.config.tickers:
            book = self.feed.books.get(ticker)
            panel = self._ticker_panels.get(ticker)
            if not book or not panel:
                continue
            lv = book.top_levels()
            self._book_cache[ticker] = lv

            bond = " [BOND - skip]" if lv.get("is_bond") else ""
            wide = " [WIDE - no taker]" if lv.get("wide_spread") else ""
            tight = " [TIGHT - ok]" if lv.get("tight_spread") else ""
            body_text = (
                f"bid {lv.get('yes_bid', '?')} x {lv.get('yes_bid_qty', '?')} "
                f"(3lvl {lv.get('bid_depth_3', '?')})  |  "
                f"ask {lv.get('yes_ask', '?')} x {lv.get('yes_ask_qty', '?')} "
                f"(3lvl {lv.get('ask_depth_3', '?')})\n"
                f"spread {lv.get('spread_cents', '?')}¢  mid {lv.get('yes_mid', '?')}  "
                f"suggest bid {lv.get('suggested_bid_plus_2c', '?')}"
                f"{bond}{wide}{tight}"
            )
            panel["body"].config(text=body_text)

            until = self._highlight_until.get(ticker, 0)
            if until <= now:
                panel["border"].config(
                    highlightbackground=IDLE_BORDER,
                    highlightthickness=IDLE_BORDER_WIDTH,
                )
                banner: tk.Label = panel["signal_banner"]
                if banner.winfo_ismapped():
                    banner.pack_forget()

    def _sync_flag_labels(self) -> None:
        self.b365_var.set(self.logger.flags.b365)
        self.fd_var.set(self.logger.flags.fanduel)
        self.dk_var.set(self.logger.flags.draftkings)

    def _toggle(self, book: str) -> None:
        event_type = self.logger.toggle_book(book)
        self._sync_flag_labels()
        msg = f"{event_type} @ {datetime.now().strftime('%H:%M:%S.%f')[:-3]}"
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)

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
        events = self.logger.event_count
        session_name = self.logger.session_dir.name
        hint = ""
        if events == 0:
            hint = "\n\nNo B/F clicks logged - Delete is fine for empty sessions."

        choice = messagebox.askyesnocancel(
            "End session",
            f"Session: {session_name}\n"
            f"Events logged: {events}\n"
            f"Folder: {self.logger.session_dir}"
            f"{hint}\n\n"
            "Yes = Save logs\n"
            "No = Delete this session folder\n"
            "Cancel = Keep running",
        )
        if choice is None:
            return

        self._sample_stop.set()
        self.feed.stop()

        if choice:
            self.logger.finalize(saved=True)
            messagebox.showinfo(
                "Session saved",
                f"Logs saved to:\n{self.logger.session_dir}",
            )
        else:
            folder = self.logger.session_dir
            self.logger.delete_session()
            messagebox.showinfo("Session deleted", f"Removed:\n{folder}")

        self.root.destroy()


def run_app(config: LabConfig) -> None:
    if not config.tickers:
        raise SystemExit("At least one ticker required")
    app = SuspensionLabApp(config)
    app.run()
