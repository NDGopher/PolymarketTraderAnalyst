from __future__ import annotations

import threading
import time
import tkinter as tk
from datetime import datetime, timezone
from tkinter import messagebox, scrolledtext, ttk

from suspension_lab.auto_trader import PaperAutoTrader, TraderConfig
from suspension_lab.config import BOND_MID_THRESHOLD, GOAL_HIGHLIGHT_SECONDS, LabConfig
from suspension_lab.goal_signal import GoalSignal, GoalSignalDetector, SpoofBidNotice, VarRevertAlert
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.market_labels import MarketLabel, MarketLabelCache
from suspension_lab.session import SessionLogger

GOAL_BORDER = "#16a34a"
GOAL_BORDER_WIDTH = 6
VAR_BORDER = "#dc2626"
VAR_BORDER_WIDTH = 6
IDLE_BORDER = "#d1d5db"
IDLE_BORDER_WIDTH = 2


class SuspensionLabApp:
    def __init__(self, config: LabConfig) -> None:
        self.config = config
        ts = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
        slug = config.game_label.replace(" ", "_")[:40] if config.game_label else "session"
        session_dir = config.output_dir / f"{ts}_{slug}"
        self.logger = SessionLogger(session_dir, config.tickers, game_label=config.game_label)
        self.trader = PaperAutoTrader(session_dir, TraderConfig.from_env())
        self.feed = KalshiBookFeed(config, on_book=self._on_book, on_status=self._on_status)
        self.logger.bind_book_provider(self._books_for_log)
        self._book_cache: dict[str, dict] = {}
        self._sample_stop = threading.Event()
        self._sample_thread: threading.Thread | None = None
        self._goal_detector = GoalSignalDetector()
        self._labels = MarketLabelCache(config.tickers, rest_base=config.rest_base)
        self._highlight_until: dict[str, float] = {}
        self._var_until: dict[str, float] = {}
        self._ticker_panels: dict[str, dict] = {}
        self._active_tickers: list[str] = list(config.tickers)

        self.root = tk.Tk()
        self.root.title("Suspension Edge Lab")
        self.root.geometry("1100x860")
        self.root.configure(padx=8, pady=8)
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._labels.load_all_async(on_update=self._on_label_loaded)

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root)
        top.pack(fill="x", pady=(0, 4))
        ttk.Label(top, text=f"Game: {self.config.game_label or '(unnamed)'}").pack(side="left")
        ttk.Label(top, text=f"Session: {self.logger.session_dir.name}").pack(side="right")

        self.status_var = tk.StringVar(value="Starting…")
        ttk.Label(self.root, textvariable=self.status_var, foreground="#444").pack(anchor="w")

        trader_row = ttk.Frame(self.root)
        trader_row.pack(fill="x", pady=(2, 4))
        self._trader_var = tk.StringVar(value=f"Auto-trader: {self.trader.mode_label}")
        ttk.Label(trader_row, textvariable=self._trader_var, font=("Segoe UI", 9)).pack(side="left")
        self._trader_enabled = tk.BooleanVar(value=self.trader.config.enabled)
        ttk.Checkbutton(
            trader_row,
            text="Paper trade on signals (no live orders)",
            variable=self._trader_enabled,
            command=self._sync_trader_toggle,
        ).pack(side="left", padx=12)

        ticker_frame = ttk.LabelFrame(self.root, text="Tickers — add while running")
        ticker_frame.pack(fill="x", pady=(4, 4))
        ticker_row = ttk.Frame(ticker_frame)
        ticker_row.pack(fill="x", padx=4, pady=4)
        self._ticker_entry = ttk.Entry(ticker_row)
        self._ticker_entry.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self._ticker_entry.insert(0, "Paste Kalshi ticker(s), comma-separated")
        self._ticker_entry.bind("<FocusIn>", self._clear_ticker_placeholder)
        ttk.Button(ticker_row, text="Add ticker", command=self._add_ticker_from_ui).pack(side="left")
        self._active_ticker_var = tk.StringVar(value=self._ticker_summary())
        ttk.Label(ticker_frame, textvariable=self._active_ticker_var, font=("Consolas", 8)).pack(
            anchor="w", padx=4, pady=(0, 4)
        )

        books_frame = ttk.LabelFrame(self.root, text="Kalshi orderbooks — YES and NO sides")
        books_frame.pack(fill="both", expand=True, pady=6)

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

        notes_frame = ttk.LabelFrame(self.root, text="Notes — scratch pad for what you see (saved on close)")
        notes_frame.pack(fill="both", expand=False, pady=4)

        note_input_row = ttk.Frame(notes_frame)
        note_input_row.pack(fill="x", padx=4, pady=(4, 2))
        self._note_entry = ttk.Entry(note_input_row)
        self._note_entry.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self._note_entry.bind("<Return>", lambda _e: self._add_note())
        ttk.Button(note_input_row, text="Add note", command=self._add_note).pack(side="left")

        self.notes_text = scrolledtext.ScrolledText(notes_frame, height=7, font=("Consolas", 10))
        self.notes_text.pack(fill="both", expand=True, padx=4, pady=(0, 4))

        help_text = (
            f"Green = goal signal · Red = VAR alert · "
            f"Paper trader: bid+1¢, mode-aware exits, VAR protection · "
            f"Bond skip: {BOND_MID_THRESHOLD:.0%}"
        )
        ttk.Label(self.root, text=help_text, foreground="#666", wraplength=1050).pack(anchor="w", pady=(4, 0))

    def _sync_trader_toggle(self) -> None:
        self.trader.config.enabled = self._trader_enabled.get()
        self._trader_var.set(f"Auto-trader: {self.trader.mode_label}")

    def _clear_ticker_placeholder(self, _event=None) -> None:
        if self._ticker_entry.get() == "Paste Kalshi ticker(s), comma-separated":
            self._ticker_entry.delete(0, tk.END)

    def _ticker_summary(self) -> str:
        if not self._active_tickers:
            return "Tracking: (none yet — add tickers above)"
        return f"Tracking {len(self._active_tickers)}: " + ", ".join(
            t.rsplit("-", 1)[-1] if "-" in t else t for t in self._active_tickers
        )

    def _add_ticker_from_ui(self) -> None:
        raw = self._ticker_entry.get().strip()
        if not raw or raw == "Paste Kalshi ticker(s), comma-separated":
            return
        parts = [p.strip() for p in raw.replace("\n", ",").split(",") if p.strip()]
        added = 0
        for ticker in parts:
            if ticker in self._ticker_panels:
                continue
            if not self.feed.add_ticker(ticker):
                continue
            self.logger.register_ticker(ticker)
            self._labels.register_ticker(ticker)
            self._active_tickers.append(ticker)
            self._create_ticker_panel(ticker)
            self._labels.fetch_one_async(ticker, on_update=self._on_label_loaded)
            added += 1
        if added:
            self._ticker_entry.delete(0, tk.END)
            self._active_ticker_var.set(self._ticker_summary())
        else:
            messagebox.showinfo("Add ticker", "Ticker already tracked or invalid.")

    def _add_note(self) -> None:
        text = self._note_entry.get().strip()
        if not text:
            return
        line = self.logger.append_note(text)
        if line:
            self.notes_text.insert(tk.END, line + "\n")
            self.notes_text.see(tk.END)
        self._note_entry.delete(0, tk.END)

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

        title = tk.Label(border, text=label.display, font=("Segoe UI", 11, "bold"), anchor="w", justify="left")
        title.pack(fill="x")
        subtitle = tk.Label(border, text=ticker, font=("Segoe UI", 8), fg="#666", anchor="w")
        subtitle.pack(fill="x")

        body = tk.Label(
            border, text="Waiting for book…", font=("Consolas", 9), anchor="w", justify="left"
        )
        body.pack(fill="x", pady=(4, 0))

        signal_banner = tk.Label(
            border, text="", font=("Segoe UI", 10, "bold"), fg="#166534", bg="#dcfce7",
            anchor="w", padx=6, pady=4,
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
        if panel:
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
        result = self._goal_detector.evaluate(ticker, book)
        if isinstance(result, GoalSignal):
            self.root.after(0, lambda s=result: self._on_goal_signal(s))
        elif isinstance(result, VarRevertAlert):
            self.root.after(0, lambda v=result: self._on_var_alert(v))
        elif isinstance(result, SpoofBidNotice):
            self.root.after(0, lambda s=result: self._on_spoof_notice(s))

        lv = book.top_levels()
        bid_s = lv.get("yes_bid", "")
        if bid_s and self.trader.config.enabled:
            bid_cents = int(round(float(bid_s) * 100))
            ask_s = lv.get("yes_ask", "")
            ask_cents = int(round(float(ask_s) * 100)) if ask_s else None
            bid_qty = float(lv.get("yes_bid_qty") or 0)
            closed = self.trader.on_book(ticker, bid_cents, ask_cents=ask_cents, bid_qty=bid_qty)
            if closed:
                self.root.after(0, lambda c=closed: self._on_paper_exit(c))

        self.root.after(0, self._refresh_display)

    def _on_goal_signal(self, signal: GoalSignal) -> None:
        label = self._labels.get(signal.ticker)
        self._highlight_until[signal.ticker] = time.time() + GOAL_HIGHLIGHT_SECONDS
        self._var_until.pop(signal.ticker, None)
        panel = self._ticker_panels.get(signal.ticker)
        mode_hint = {
            "hold_bond": "HOLD to 99¢ / resolution",
            "scalp": "scalp +7¢ limit",
            "var_watch": "VAR protection — exit on limbo/revert",
        }.get(signal.exit_mode, signal.exit_mode)
        if panel:
            banner: tk.Label = panel["signal_banner"]
            banner.config(
                text=f"⚽ GOAL SIGNAL — {signal.summary}\n→ {mode_hint}",
                fg="#166534",
                bg="#dcfce7",
            )
            banner.pack(fill="x", pady=(6, 0))
            panel["border"].config(highlightbackground=GOAL_BORDER, highlightthickness=GOAL_BORDER_WIDTH)

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
            exit_mode=signal.exit_mode,
            ts_ms=signal.ts_ms,
        )

        pos = self.trader.on_goal_signal(signal, label.display)
        if pos:
            self.notes_text.insert(
                tk.END,
                f"[AUTO PAPER] {self.trader.summary_line(pos)}\n",
            )
            self.notes_text.see(tk.END)

        try:
            self.root.bell()
        except tk.TclError:
            pass

    def _on_paper_exit(self, pos) -> None:
        pnl = (pos.exit_cents or 0) - pos.entry_cents
        self.notes_text.insert(
            tk.END,
            f"[AUTO EXIT] #{pos.trade_id} {pos.exit_reason} @ {pos.exit_cents}¢ "
            f"({pnl:+d}¢/ct)\n",
        )
        self.notes_text.see(tk.END)

    def _on_var_alert(self, alert: VarRevertAlert) -> None:
        label = self._labels.get(alert.ticker)
        self._var_until[alert.ticker] = time.time() + GOAL_HIGHLIGHT_SECONDS
        self._highlight_until.pop(alert.ticker, None)
        panel = self._ticker_panels.get(alert.ticker)
        if panel:
            banner: tk.Label = panel["signal_banner"]
            banner.config(
                text=(
                    f"⚠️ VAR / CANCELLED? — bid fell {alert.drop_cents}¢ from peak "
                    f"({alert.peak_bid:.2f}→{alert.current_bid:.2f}) in {alert.seconds_since_signal:.0f}s"
                ),
                fg="#991b1b",
                bg="#fee2e2",
            )
            banner.pack(fill="x", pady=(6, 0))
            panel["border"].config(highlightbackground=VAR_BORDER, highlightthickness=VAR_BORDER_WIDTH)

        bid_cents = int(round(float(alert.current_bid) * 100))
        if self.trader.config.enabled:
            closed = self.trader.on_book(alert.ticker, bid_cents)
            if closed:
                self._on_paper_exit(closed)

        self.notes_text.insert(
            tk.END,
            f"[VAR ALERT] {label.display} -{alert.drop_cents}c from peak\n",
        )
        self.notes_text.see(tk.END)

    def _on_spoof_notice(self, notice: SpoofBidNotice) -> None:
        label = self._labels.get(notice.ticker)
        panel = self._ticker_panels.get(notice.ticker)
        if panel:
            banner: tk.Label = panel["signal_banner"]
            banner.config(
                text=(
                    f"ℹ️ SPOOF BID? — {notice.current_bid:.2f} x {notice.bid_qty:.0f} "
                    f"but ask still {notice.current_ask:.2f} (bonded market, not VAR)"
                ),
                fg="#92400e",
                bg="#fef3c7",
            )
            banner.pack(fill="x", pady=(6, 0))
        self.notes_text.insert(
            tk.END,
            f"[SPOOF BID] {label.display if label else notice.ticker} "
            f"bid {notice.current_bid:.2f} ask {notice.current_ask:.2f} — hold, not VAR\n",
        )
        self.notes_text.see(tk.END)

    def _on_status(self, msg: str) -> None:
        self.root.after(0, lambda: self.status_var.set(msg))

    def _format_book(self, lv: dict) -> str:
        bond = " [BOND]" if lv.get("is_bond") else ""
        wide = " [WIDE]" if lv.get("wide_spread") else ""
        tight = " [TIGHT]" if lv.get("tight_spread") else ""
        return (
            f"YES  bid {lv.get('yes_bid', '?')} x {lv.get('yes_bid_qty', '?')}  "
            f"ask {lv.get('yes_ask', '?')} x {lv.get('yes_ask_qty', '?')}  "
            f"(3lvl bid {lv.get('bid_depth_3', '?')})\n"
            f"NO   bid {lv.get('no_bid', '?')} x {lv.get('no_bid_qty', '?')}  "
            f"ask {lv.get('no_ask', '?')} x {lv.get('no_ask_qty', '?')}  "
            f"(3lvl ask {lv.get('ask_depth_3', '?')})\n"
            f"spread {lv.get('spread_cents', '?')}¢  mid {lv.get('yes_mid', '?')}  "
            f"entry bid+1¢ → {lv.get('suggested_bid_plus_1c', '?')}"
            f"{bond}{wide}{tight}"
        )

    def _refresh_display(self) -> None:
        now = time.time()
        for ticker in list(self.feed.books.keys()):
            book = self.feed.books.get(ticker)
            panel = self._ticker_panels.get(ticker)
            if not book or not panel:
                continue
            lv = book.top_levels()
            self._book_cache[ticker] = lv
            panel["body"].config(text=self._format_book(lv))

            until = self._highlight_until.get(ticker, 0)
            var_until = self._var_until.get(ticker, 0)
            if var_until > now:
                continue
            if until <= now:
                panel["border"].config(
                    highlightbackground=IDLE_BORDER,
                    highlightthickness=IDLE_BORDER_WIDTH,
                )
                banner: tk.Label = panel["signal_banner"]
                if banner.winfo_ismapped():
                    banner.pack_forget()

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
        note_lines = len([ln for ln in notes_preview.splitlines() if ln.strip()])
        choice = messagebox.askyesnocancel(
            "End session",
            f"Session: {self.logger.session_dir.name}\n"
            f"Notes: {note_lines} line(s)\n"
            f"Folder: {self.logger.session_dir}\n\n"
            "Yes = Save logs + notes\n"
            "No = Delete this session folder\n"
            "Cancel = Keep running",
        )
        if choice is None:
            return

        self._sample_stop.set()
        self.feed.stop()

        if choice:
            self.logger.finalize(saved=True, notes_text=self.notes_text.get("1.0", tk.END))
            messagebox.showinfo("Session saved", f"Logs saved to:\n{self.logger.session_dir}")
        else:
            folder = self.logger.session_dir
            self.logger.delete_session()
            messagebox.showinfo("Session deleted", f"Removed:\n{folder}")

        self.root.destroy()


def run_app(config: LabConfig) -> None:
    app = SuspensionLabApp(config)
    app.run()
