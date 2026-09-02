from __future__ import annotations

import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, scrolledtext, ttk

from suspension_lab.lab_runtime import LabRuntime
from suspension_lab.market_labels import MarketLabel
from suspension_lab.soccer_discovery import SoccerGame
from suspension_lab.tape_engine import TapeEvent
from suspension_lab.ui_layout import (
    CLOCK_FONT,
    DISPLAY_FONT,
    FLASH_SECONDS,
    HEARTBEAT_MS,
    LINE_FONT,
    PRICE_FONT,
    STATUS_FONT,
    TAPE_FONT,
    TICKER_FONT,
    WINDOW_GEOMETRY,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    ascii_text,
    english_line,
    format_clock,
    format_last_book,
    format_paper_pnl,
    format_tape_line,
    format_yes_cents,
    health_badge_text,
    matchup_hero,
    show_on_tape,
    slot_title_for_ticker,
    stale_banner_text,
    tape_kind_tag,
    ticker_subtitle,
    tile_columns_for_width,
    transport_label,
)

BG = "#0e1116"
CARD = "#161b22"
INK = "#e6edf3"
MUTED = "#8b949e"
GREEN = "#3fb950"
RED = "#f85149"
AMBER = "#d29922"
LINE = "#30363d"
GOAL_BG = "#16351f"
GOAL_FLASH = "#0f8a3e"
GOAL_FLASH_FG = "#d8ffe6"
VAR_BG = "#3d1418"
SPOOF_BG = "#3d2e10"
STALE_BG = "#3d2a08"
FROZEN_BG = "#4a1515"
RATE_BG = "#3d3210"
STRIP = "#12171e"
OK = "#238636"
WARN = "#9e6a03"
DANGER = "#da3633"

class BookGrid:
    """Wrapping 2-3 column tile grid. Never pack(side=left)."""

    def __init__(self, parent: tk.Widget) -> None:
        self.host = tk.Frame(parent, bg=CARD)
        self.host.pack(fill="x")
        self.tiles: list[tk.Widget] = []

    def add(self, tile: tk.Widget) -> None:
        self.tiles.append(tile)

    def reflow(self, card_width: int) -> None:
        cols = tile_columns_for_width(card_width)
        for col in range(4):
            self.host.columnconfigure(col, weight=1 if col < cols else 0, minsize=0)
        for index, tile in enumerate(self.tiles):
            tile.grid(
                row=index // cols,
                column=index % cols,
                sticky="nsew",
                padx=3,
                pady=3,
            )


class SuspensionLabApp:
    def __init__(self, runtime: LabRuntime) -> None:
        self.runtime = runtime
        self.config = runtime.config
        self.engine = runtime.engine
        self.logger = runtime.logger
        self.trader = runtime.trader
        self._labels = runtime.engine.labels
        self._ticker_boxes: dict[str, dict] = {}
        self._game_cards: dict[str, tk.Widget] = {}
        self._grids: list[BookGrid] = []
        self._idle_card = None
        self._active_tickers: list[str] = list(self.config.tickers)
        self._wheel_armed = False
        self._ticker_to_card: dict[str, tk.Widget] = {}
        self._card_heroes: dict[tk.Widget, tk.Label] = {}
        self._card_chrome: dict[tk.Widget, list[tk.Widget]] = {}
        self._flash_until: dict[int, float] = {}
        self._last_fill = "-"
        self._board_stale = False
        self.trader.config.live = False

        self.root = tk.Tk()
        self.root.title("PTA - Suspension desk")
        self.root.geometry(WINDOW_GEOMETRY)
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.root.configure(bg=BG, padx=10, pady=8)
        self._style()
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._labels.load_all_async(on_update=self._on_label_loaded)
        self.root.after(150, self._drain_runtime)
        self.root.after(400, self._refresh_display)
        self.root.after(HEARTBEAT_MS, self._refresh_heartbeat)

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
        strip = tk.Frame(self.root, bg=STRIP, padx=8, pady=6)
        strip.pack(fill="x")
        self._paper_badge = tk.Label(
            strip,
            text="PAPER",
            font=("Segoe UI", 11, "bold"),
            fg="#0d1117",
            bg=AMBER,
            padx=8,
            pady=2,
        )
        self._paper_badge.pack(side="left")
        self._health_var = tk.StringVar(value="LIVE")
        self._health_badge = tk.Label(
            strip,
            textvariable=self._health_var,
            font=("Segoe UI", 11, "bold"),
            fg="#0d1117",
            bg=OK,
            padx=8,
            pady=2,
        )
        self._health_badge.pack(side="left", padx=(8, 0))
        self._transport_var = tk.StringVar(value="IDLE")
        self._transport_badge = tk.Label(
            strip,
            textvariable=self._transport_var,
            font=("Segoe UI", 11, "bold"),
            fg=INK,
            bg=CARD,
            padx=8,
            pady=2,
        )
        self._transport_badge.pack(side="left", padx=(8, 0))
        self._health_detail = tk.StringVar(value="last book -")
        tk.Label(
            strip,
            textvariable=self._health_detail,
            font=STATUS_FONT,
            fg=INK,
            bg=STRIP,
        ).pack(side="left", padx=(10, 0))
        self._clock_var = tk.StringVar(value=format_clock(datetime.now()))
        tk.Label(
            strip,
            textvariable=self._clock_var,
            font=CLOCK_FONT,
            fg=INK,
            bg=STRIP,
        ).pack(side="right")
        tk.Label(
            strip,
            text=self.logger.session_dir.name,
            font=("Segoe UI", 9),
            fg=MUTED,
            bg=STRIP,
        ).pack(side="right", padx=(0, 12))

        pnl = tk.Frame(self.root, bg=BG)
        pnl.pack(fill="x", pady=(6, 2))
        self._pnl_var = tk.StringVar(value=format_paper_pnl(0, 0, "-"))
        self._would_var = tk.StringVar(value="Would-have  0 - +0c")
        self._burn_var = tk.StringVar(value="Burned  0 - 0c")
        self._open_var = tk.StringVar(value="Open  0")
        tk.Label(
            pnl,
            textvariable=self._pnl_var,
            font=DISPLAY_FONT,
            fg=GREEN,
            bg=BG,
        ).pack(side="left")
        tk.Label(
            pnl,
            textvariable=self._would_var,
            font=STATUS_FONT,
            fg=GREEN,
            bg=BG,
        ).pack(side="left", padx=(20, 0))
        tk.Label(
            pnl,
            textvariable=self._burn_var,
            font=STATUS_FONT,
            fg=RED,
            bg=BG,
        ).pack(side="left", padx=(16, 0))
        tk.Label(
            pnl,
            textvariable=self._open_var,
            font=STATUS_FONT,
            fg=MUTED,
            bg=BG,
        ).pack(side="left", padx=(16, 0))

        self._stale_slot = tk.Frame(self.root, bg=BG)
        self._stale_slot.pack(fill="x")
        self._stale_var = tk.StringVar(value="")
        self._stale_banner = tk.Label(
            self._stale_slot,
            textvariable=self._stale_var,
            font=("Segoe UI", 16, "bold"),
            fg="#ffe8a3",
            bg=STALE_BG,
            padx=8,
            pady=6,
            anchor="w",
        )

        self.status_var = tk.StringVar(
            value="Waiting for live soccer..." if not self.config.tickers else "Starting..."
        )
        tk.Label(self.root, textvariable=self.status_var, font=STATUS_FONT, fg=MUTED, bg=BG).pack(
            anchor="w"
        )
        self._waiting_var = tk.StringVar(
            value="WAITING FOR LIVE SOCCER - WS idle until books appear"
            if not self.config.tickers
            else ""
        )
        self._waiting_label = tk.Label(
            self.root,
            textvariable=self._waiting_var,
            font=("Segoe UI", 11, "bold"),
            fg=AMBER,
            bg=BG,
        )
        if not self.config.tickers:
            self._waiting_label.pack(anchor="w", pady=(4, 0))

        trader_row = tk.Frame(self.root, bg=BG)
        trader_row.pack(fill="x", pady=(4, 4))
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
        right = tk.Frame(body, bg=BG, width=320)
        right.pack(side="right", fill="y", padx=(10, 0))
        right.pack_propagate(False)

        self._canvas = tk.Canvas(left, bg=BG, highlightthickness=0)
        scroll = ttk.Scrollbar(left, orient="vertical", command=self._canvas.yview)
        self._cards = tk.Frame(self._canvas, bg=BG)
        self._canvas_window = self._canvas.create_window((0, 0), window=self._cards, anchor="nw")
        self._canvas.configure(yscrollcommand=scroll.set)
        self._canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._cards.bind("<Configure>", self._on_cards_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_board_scroll()

        games: list[SoccerGame] = list(self.engine.games or getattr(self.config, "games", []) or [])
        placed: set[str] = set()
        if games:
            for game in games:
                self._create_game_card(game)
                placed.update(game.get_tickers())
        leftover = [t for t in self.config.tickers if t not in placed]
        if leftover:
            self._create_loose_card(leftover)
        if not games and not leftover:
            idle = tk.Frame(self._cards, bg=CARD, highlightbackground=LINE, highlightthickness=1, padx=10, pady=16)
            idle.pack(fill="x", pady=(0, 10), padx=2)
            tk.Label(
                idle,
                text="No live soccer tape yet",
                font=("Segoe UI", 13, "bold"),
                fg=INK,
                bg=CARD,
                anchor="w",
            ).pack(fill="x")
            tk.Label(
                idle,
                text="Waiting for live soccer. One discover until a book seats, then WS only. No 60s rediscover.",
                font=("Segoe UI", 9),
                fg=MUTED,
                bg=CARD,
                anchor="w",
            ).pack(fill="x", pady=(4, 0))
            self._idle_card = idle
        else:
            self._idle_card = None

        tk.Label(
            right,
            text="TAPE",
            font=("Segoe UI", 11, "bold"),
            fg=INK,
            bg=BG,
        ).pack(anchor="w")
        tk.Label(
            right,
            text="GOAL from the book - not a score feed",
            font=STATUS_FONT,
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(0, 4))
        self.events_text = scrolledtext.ScrolledText(
            right, height=22, font=TAPE_FONT, bg="#0a0d10", fg=INK, relief="flat", wrap="word"
        )
        self.events_text.pack(fill="both", expand=True)
        self.events_text.configure(insertbackground=INK)
        self.events_text.tag_configure("GOAL", foreground=GOAL_FLASH_FG, background=GOAL_FLASH)
        self.events_text.tag_configure("FILL", foreground=GREEN)
        self.events_text.tag_configure("LIMIT", foreground=AMBER, background=RATE_BG)
        self.events_text.tag_configure("VAR", foreground=RED, background=VAR_BG)
        self.events_text.tag_configure("SPOOF", foreground=AMBER)
        self.events_text.tag_configure("SKIP", foreground=MUTED)
        self.events_text.tag_configure("EXIT", foreground=GREEN)
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
            notes, height=3, font=("Consolas", 9), bg=CARD, fg=INK, relief="flat"
        )
        self.notes_text.pack(fill="x", padx=4, pady=4)

    def _bind_board_scroll(self) -> None:
        self._canvas.bind("<Enter>", self._arm_wheel)
        self._cards.bind("<Enter>", self._arm_wheel)
        self._canvas.bind("<Leave>", self._maybe_disarm_wheel)
        self._canvas.bind("<MouseWheel>", self._on_mousewheel)
        self._cards.bind("<MouseWheel>", self._on_mousewheel)
        self._canvas.bind("<Button-4>", self._on_button_scroll)
        self._canvas.bind("<Button-5>", self._on_button_scroll)
        self._cards.bind("<Button-4>", self._on_button_scroll)
        self._cards.bind("<Button-5>", self._on_button_scroll)

    def _arm_wheel(self, _event=None) -> None:
        if self._wheel_armed:
            return
        self._wheel_armed = True
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", self._on_button_scroll)
        self.root.bind_all("<Button-5>", self._on_button_scroll)

    def _maybe_disarm_wheel(self, event=None) -> None:
        if event is not None:
            widget = self.root.winfo_containing(event.x_root, event.y_root)
            walk = widget
            while walk is not None:
                if walk in (self._canvas, self._cards):
                    return
                walk = getattr(walk, "master", None)
        if not self._wheel_armed:
            return
        self._wheel_armed = False
        self.root.unbind_all("<MouseWheel>")
        self.root.unbind_all("<Button-4>")
        self.root.unbind_all("<Button-5>")

    def _on_mousewheel(self, event) -> str:
        delta = int(getattr(event, "delta", 0) or 0)
        if delta:
            self._canvas.yview_scroll(int(-1 * (delta / 120)), "units")
        return "break"

    def _on_button_scroll(self, event) -> str:
        num = getattr(event, "num", 0)
        if num == 4:
            self._canvas.yview_scroll(-3, "units")
        elif num == 5:
            self._canvas.yview_scroll(3, "units")
        return "break"

    def _on_canvas_configure(self, event) -> None:
        width = int(self._canvas.winfo_width() or event.width or 0)
        if width <= 1:
            return
        self._canvas.itemconfigure(self._canvas_window, width=width)
        self._reflow_grids(width)
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_cards_configure(self, _event=None) -> None:
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _reflow_grids(self, width: int) -> None:
        inner = max(width - 8, 1)
        for grid in self._grids:
            grid.reflow(inner)

    def _create_game_card(self, game: SoccerGame) -> None:
        card = tk.Frame(self._cards, bg=CARD, highlightbackground=LINE, highlightthickness=1, padx=8, pady=6)
        card.pack(fill="x", pady=(0, 8), padx=2)
        if game.event_ticker:
            self._game_cards[game.event_ticker] = card
        label = None
        for ticker in game.get_tickers():
            try:
                label = self._labels.get(ticker)
            except Exception:  # noqa: BLE001
                label = None
            if label and label.matchup:
                break
        head = matchup_hero(game, label)
        kick = (game.occurrence_time or game.close_time or "")[:16].replace("T", " ")
        hero = tk.Label(card, text=head, font=DISPLAY_FONT, fg=INK, bg=CARD, anchor="w")
        hero.pack(fill="x")
        meta = tk.Label(
            card,
            text=f"{kick} UTC   -   24h vol {game.total_24h_volume:.0f}   -   {game.series}",
            font=("Segoe UI", 8),
            fg=MUTED,
            bg=CARD,
            anchor="w",
        )
        meta.pack(fill="x", pady=(0, 4))
        self._card_heroes[card] = hero
        self._card_chrome[card] = [card, hero, meta]
        grid = BookGrid(card)
        self._grids.append(grid)
        slots = [
            ("Home ML", game.home_ml_ticker),
            ("Away ML", game.away_ml_ticker),
        ]
        if game.tie_ml_ticker:
            slots.append(("TIE", game.tie_ml_ticker))
        slots.extend(
            [
                (game.total_atm_label or "ATM total", game.total_atm_ticker or game.over_05_ticker),
                (game.total_up_label or "ATM+1", game.total_up_ticker or game.over_15_ticker),
            ]
        )
        for title, ticker in slots:
            self._create_book_box(grid, ticker, title)
            if ticker:
                self._ticker_to_card[ticker] = card
        grid.reflow(max(self._canvas.winfo_width(), 1))

    def _create_loose_card(self, tickers: list[str]) -> None:
        card = tk.Frame(self._cards, bg=CARD, highlightbackground=LINE, highlightthickness=1, padx=8, pady=6)
        card.pack(fill="x", pady=(0, 8), padx=2)
        hero = tk.Label(card, text="Books", font=DISPLAY_FONT, fg=INK, bg=CARD)
        hero.pack(anchor="w")
        self._card_heroes[card] = hero
        self._card_chrome[card] = [card, hero]
        grid = BookGrid(card)
        self._grids.append(grid)
        for ticker in tickers:
            self._create_book_box(grid, ticker, slot_title_for_ticker(ticker, "Book"))
            self._ticker_to_card[ticker] = card
        grid.reflow(max(self._canvas.winfo_width(), 1))

    def _create_book_box(self, grid: BookGrid, ticker: str | None, title: str) -> None:
        box = tk.Frame(grid.host, bg=BG, highlightbackground=LINE, highlightthickness=1, padx=6, pady=4)
        if not ticker:
            tk.Label(box, text=f"{title}\n-", fg=MUTED, bg=BG, font=("Segoe UI", 9), justify="left").pack()
            grid.add(box)
            return
        name = tk.Label(box, text=ascii_text(title), font=LINE_FONT, fg=INK, bg=BG, anchor="w")
        name.pack(fill="x")
        sub = tk.Label(box, text=ticker_subtitle(ticker), font=TICKER_FONT, fg=MUTED, bg=BG, anchor="w")
        sub.pack(fill="x")
        caps = tk.Frame(box, bg=BG)
        caps.pack(fill="x", pady=(4, 0))
        tk.Label(caps, text="YES BID", font=("Segoe UI", 8), fg=MUTED, bg=BG).grid(
            row=0, column=0, sticky="w"
        )
        tk.Label(caps, text="YES ASK", font=("Segoe UI", 8), fg=MUTED, bg=BG).grid(
            row=0, column=1, sticky="w", padx=(12, 0)
        )
        bid = tk.Label(caps, text="-", font=PRICE_FONT, fg=INK, bg=BG, anchor="w")
        bid.grid(row=1, column=0, sticky="w")
        ask = tk.Label(caps, text="-", font=PRICE_FONT, fg=INK, bg=BG, anchor="w")
        ask.grid(row=1, column=1, sticky="w", padx=(12, 0))
        banner = tk.Label(box, text="", font=("Segoe UI", 8, "bold"), fg=INK, bg=BG, anchor="w")
        self._ticker_boxes[ticker] = {
            "box": box,
            "title": name,
            "subtitle": sub,
            "caps": caps,
            "bid": bid,
            "ask": ask,
            "banner": banner,
        }
        grid.add(box)

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
        new = [t for t in parts if t not in self._ticker_boxes]
        if not new:
            messagebox.showinfo("Add ticker", "Ticker already tracked or invalid.")
            return
        # Worker does REST/WS subscribe. Tk only queues.
        self.runtime.request_add_tickers(new)
        self._ticker_entry.delete(0, tk.END)

    def _paint_event(self, event: TapeEvent) -> None:
        tag = tape_kind_tag(event.kind)
        if show_on_tape(event.kind):
            label = None
            try:
                label = self._labels.get(event.ticker) if event.ticker else None
            except Exception:  # noqa: BLE001
                label = None
            line = format_tape_line(event, label)
            self.events_text.insert("1.0", line + "\n", tag)
            self.events_text.see("1.0")
        if tag in {"FILL", "EXIT"} or "paper make" in (event.detail or ""):
            label = None
            try:
                label = self._labels.get(event.ticker) if event.ticker else None
            except Exception:  # noqa: BLE001
                label = None
            bit = ascii_text((label.line if label and label.line else event.kind) or "fill")
            self._last_fill = f"{bit} {ascii_text(event.detail)[:40]}"
            self._refresh_scoreboard()
        box = self._ticker_boxes.get(event.ticker)
        if box:
            colors = {
                "GOAL": (GOAL_FLASH_FG, GOAL_FLASH),
                "VAR": (RED, VAR_BG),
                "SPOOF": (AMBER, SPOOF_BG),
                "SKIP": (MUTED, BG),
                "EXIT": (INK, BG),
                "FILL": (GREEN, GOAL_BG),
                "LIMIT": (AMBER, RATE_BG),
            }
            fg, bg = colors.get(tag, (INK, BG))
            box["banner"].config(text=ascii_text(f"{event.kind}: {event.detail[:80]}"), fg=fg, bg=bg)
            box["banner"].pack(fill="x", pady=(2, 0))
            box["box"].config(highlightbackground=fg, highlightthickness=2)
        if tag == "GOAL":
            self._flash_goal(event.ticker)

    def _flash_goal(self, ticker: str) -> None:
        until = time.monotonic() + FLASH_SECONDS
        card = self._ticker_to_card.get(ticker)
        targets: list[tk.Widget] = []
        if card is not None:
            targets.append(card)
            targets.extend(self._card_chrome.get(card, []))
        box = self._ticker_boxes.get(ticker)
        if box:
            targets.extend(
                [w for w in (box.get("box"), box.get("bid"), box.get("ask"), box.get("caps"), box.get("title"), box.get("subtitle"), box.get("banner")) if w]
            )
        for widget in targets:
            try:
                widget.configure(bg=GOAL_FLASH)
                if isinstance(widget, tk.Label):
                    widget.configure(fg=GOAL_FLASH_FG)
            except tk.TclError:
                continue
            self._flash_until[id(widget)] = until
        if card is not None:
            try:
                card.configure(highlightbackground=GREEN, highlightthickness=3)
            except tk.TclError:
                pass
        self.root.after(int(FLASH_SECONDS * 1000) + 50, self._clear_expired_flashes)

    def _clear_expired_flashes(self) -> None:
        now = time.monotonic()
        expired = [key for key, until in self._flash_until.items() if until <= now]
        if not expired:
            return
        for card, chrome in self._card_chrome.items():
            if id(card) in expired or any(id(w) in expired for w in chrome):
                try:
                    card.configure(bg=CARD, highlightbackground=LINE, highlightthickness=1)
                except tk.TclError:
                    pass
                for widget in chrome:
                    try:
                        widget.configure(bg=CARD, fg=INK if widget is self._card_heroes.get(card) else MUTED)
                    except tk.TclError:
                        pass
        for box in self._ticker_boxes.values():
            widgets = [box.get("box"), box.get("caps"), box.get("bid"), box.get("ask"), box.get("title"), box.get("subtitle"), box.get("banner")]
            if not any(id(w) in expired for w in widgets if w is not None):
                continue
            try:
                box["box"].configure(bg=BG, highlightbackground=LINE, highlightthickness=1)
            except tk.TclError:
                pass
            for key, fg in (("title", INK), ("subtitle", MUTED), ("bid", INK), ("ask", INK), ("banner", INK)):
                widget = box.get(key)
                if widget is None:
                    continue
                try:
                    widget.configure(bg=BG, fg=fg)
                except tk.TclError:
                    pass
            caps = box.get("caps")
            if caps is not None:
                try:
                    caps.configure(bg=BG)
                    for child in caps.winfo_children():
                        child.configure(bg=BG)
                except tk.TclError:
                    pass
        for key in expired:
            self._flash_until.pop(key, None)

    def _refresh_scoreboard(self) -> None:
        b = self.trader.scoreboard()
        session = int(b["would_have_pnl_cents"]) + int(b["burned_pnl_cents"])
        self._pnl_var.set(format_paper_pnl(session, int(b["open"]), self._last_fill))
        self._would_var.set(
            f"Would-have  {b['would_have_count']} - {b['would_have_pnl_cents']:+d}c  [paper]"
        )
        self._burn_var.set(f"Burned  {b['burned_count']} - {b['burned_pnl_cents']:+d}c")
        self._open_var.set(f"Open  {b['open']}")

    def _on_label_loaded(self, ticker: str, label: MarketLabel) -> None:
        self.root.after(0, lambda: self._apply_label(ticker, label))

    def _apply_label(self, ticker: str, label: MarketLabel) -> None:
        box = self._ticker_boxes.get(ticker)
        if box:
            box["title"].config(text=english_line(label, box["title"].cget("text")))
            box["subtitle"].config(text=ticker_subtitle(ticker))
        card = self._ticker_to_card.get(ticker)
        hero = self._card_heroes.get(card) if card is not None else None
        if hero is not None and label.matchup:
            current = hero.cget("text")
            if current != "Books":
                hero.config(text=ascii_text(label.matchup))

    def _paint_book(self, ticker: str, levels: dict) -> None:
        box = self._ticker_boxes.get(ticker)
        if not box:
            return
        box["bid"].config(text=format_yes_cents(levels.get("yes_bid")))
        box["ask"].config(text=format_yes_cents(levels.get("yes_ask")))

    def _refresh_display(self) -> None:
        for ticker, book in self.runtime.feed.books.items():
            self._paint_book(ticker, book.top_levels())
        self._refresh_scoreboard()
        self.root.after(250, self._refresh_display)

    def _refresh_heartbeat(self) -> None:
        # Clock ticks even when books freeze. If this label stops, Tk is wedged.
        self._clock_var.set(format_clock(datetime.now()))
        health, detail = self.runtime.heartbeat_text()
        self._apply_health(health, detail)
        self._clear_expired_flashes()
        self.root.after(HEARTBEAT_MS, self._refresh_heartbeat)

    def _apply_health(self, health: str, detail: str) -> None:
        self._health_var.set(health_badge_text(health))
        now = time.monotonic()
        last = getattr(self.runtime.feed, "last_book_monotonic", 0.0) or 0.0
        age = (now - last) if last else None
        self._health_detail.set(format_last_book(age) + "  " + ascii_text(detail))
        ws = bool(getattr(self.runtime.feed, "ws_connected", False))
        rest = bool(getattr(self.runtime.feed, "using_slow_rest", False))
        if health == "429":
            transport = "429"
        else:
            transport = transport_label(ws_connected=ws, using_slow_rest=rest)
        self._transport_var.set(transport)
        colors = {
            "LIVE": ("#0d1117", OK),
            "429": ("#fff5f5", DANGER),
            "STALE": ("#fff3c4", STALE_BG),
            "FROZEN": ("#ffd7d7", FROZEN_BG),
        }
        fg, bg = colors.get(health, (INK, RATE_BG))
        self._health_badge.config(fg=fg, bg=bg)
        tcolors = {
            "WS": (INK, OK),
            "REST": ("#0d1117", WARN),
            "429": ("#fff5f5", DANGER),
            "IDLE": (MUTED, CARD),
        }
        tfg, tbg = tcolors.get(transport, (INK, CARD))
        self._transport_badge.config(fg=tfg, bg=tbg)
        stale = health in {"STALE", "FROZEN"}
        if stale:
            self._stale_var.set(stale_banner_text(health, age))
            self._stale_banner.configure(bg=FROZEN_BG if health == "FROZEN" else STALE_BG)
            if not self._board_stale:
                self._stale_banner.pack(fill="x", pady=(4, 2))
                self._dim_board(True)
            self._board_stale = True
        elif self._board_stale:
            self._stale_banner.pack_forget()
            self._dim_board(False)
            self._board_stale = False

    def _dim_board(self, dim: bool) -> None:
        board_bg = "#0a0a0a" if dim else BG
        card_bg = "#10141a" if dim else CARD
        try:
            self._canvas.configure(bg=board_bg)
            self._cards.configure(bg=board_bg)
        except tk.TclError:
            return
        for card, chrome in self._card_chrome.items():
            if id(card) in self._flash_until:
                continue
            try:
                card.configure(bg=card_bg)
            except tk.TclError:
                continue
            for widget in chrome:
                try:
                    widget.configure(bg=card_bg)
                except tk.TclError:
                    pass

    def _drain_runtime(self) -> None:
        for item in self.runtime.drain_ui():
            if item.kind == "status":
                self.status_var.set(str(item.payload.get("text") or ""))
            elif item.kind == "event":
                event = item.payload.get("event")
                if isinstance(event, TapeEvent):
                    self._paint_event(event)
            elif item.kind == "book":
                ticker = item.payload.get("ticker")
                levels = item.payload.get("levels") or {}
                if ticker:
                    self._paint_book(str(ticker), levels)
            elif item.kind == "tickers_added":
                tickers = [str(t) for t in item.payload.get("tickers") or []]
                fresh = [t for t in tickers if t not in self._ticker_boxes]
                if fresh:
                    self._clear_idle()
                    self._create_loose_card(fresh)
                    self._active_tickers.extend(fresh)
                    for ticker in fresh:
                        self._labels.fetch_one_async(ticker, on_update=self._on_label_loaded)
            elif item.kind == "discover":
                self._absorb_discovery(item.payload)
            elif item.kind == "health":
                health = str(item.payload.get("health") or "LIVE")
                _, detail = self.runtime.heartbeat_text()
                self._apply_health(health, detail)
        self.root.after(150, self._drain_runtime)

    def _clear_idle(self) -> None:
        if self._idle_card is not None:
            try:
                self._idle_card.destroy()
            except tk.TclError:
                pass
            self._idle_card = None
        self._waiting_var.set("")

    def _drop_ticker_box(self, ticker: str) -> None:
        box = self._ticker_boxes.pop(ticker, None)
        self._ticker_to_card.pop(ticker, None)
        if box and box.get("box"):
            try:
                box["box"].destroy()
            except tk.TclError:
                pass
        if ticker in self._active_tickers:
            self._active_tickers.remove(ticker)

    def _drop_game_card(self, game: SoccerGame) -> None:
        for ticker in game.get_tickers():
            self._drop_ticker_box(ticker)
        card = self._game_cards.pop(game.event_ticker, None)
        if card is not None:
            self._card_heroes.pop(card, None)
            self._card_chrome.pop(card, None)
            try:
                card.destroy()
            except tk.TclError:
                pass

    def _absorb_discovery(self, payload: dict) -> None:
        kept = payload.get("kept") or []
        games = list(getattr(payload.get("result"), "games", None) or kept)
        drop = payload.get("drop") or []
        fund = payload.get("fund") or []
        if kept:
            kept_events = {g.event_ticker for g in kept if g.event_ticker}
            for old in list(self.engine.games):
                if old.event_ticker and old.event_ticker not in kept_events:
                    self.events_text.insert(tk.END, f"DROPPED  {old.title} (finished)\n", "SKIP")
                    self._drop_game_card(old)
        for ticker in drop:
            self._drop_ticker_box(ticker)
            self.events_text.insert(tk.END, f"DROP WING  {ticker}\n", "SKIP")

        new_games = [
            g
            for g in kept or games
            if g.event_ticker not in self._game_cards
            and not any(t in self._ticker_boxes for t in g.get_tickers())
        ]
        fund_set = set(fund or [])
        for game in new_games + [g for g in (kept or games) if g not in new_games]:
            added = []
            for ticker in game.get_tickers():
                if ticker in self._ticker_boxes:
                    continue
                if fund_set and ticker not in fund_set:
                    continue
                added.append(ticker)
            if added and game in new_games:
                self._clear_idle()
                self._create_game_card(game)
                self._active_tickers.extend(added)
                for ticker in added:
                    self._labels.fetch_one_async(ticker, on_update=self._on_label_loaded)
                self.events_text.insert(tk.END, f"AUTO-FUND  {matchup_hero(game)}\n", "PAPER")
            elif added:
                missing = [t for t in added if t not in self._ticker_boxes]
                if missing:
                    self._create_loose_card(missing)
                self._active_tickers.extend(added)
                for ticker in added:
                    self._labels.fetch_one_async(ticker, on_update=self._on_label_loaded)
                self.events_text.insert(
                    tk.END, f"TOTALS RE-PICK  {matchup_hero(game)} {game.totals_summary()}\n", "PAPER"
                )
        width = int(self._canvas.winfo_width() or 0)
        if width > 1:
            self._reflow_grids(width)
            self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def run(self) -> None:
        self.runtime.start()
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
        self.runtime.stop()
        if choice:
            self.logger.finalize(saved=True, notes_text=notes_preview)
            messagebox.showinfo("Session saved", f"Logs saved to:\n{self.logger.session_dir}")
        else:
            folder = self.logger.session_dir
            self.logger.delete_session()
            messagebox.showinfo("Session deleted", f"Removed:\n{folder}")
        self.root.destroy()


def run_app(config=None, runtime: LabRuntime | None = None) -> None:
    if runtime is None:
        if config is None:
            raise ValueError("run_app requires config or runtime")
        runtime = LabRuntime(config)
    app = SuspensionLabApp(runtime)
    app.run()
