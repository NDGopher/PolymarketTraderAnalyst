from __future__ import annotations

import threading
import time
import tkinter as tk
from datetime import datetime, timezone
from tkinter import messagebox, scrolledtext, ttk

from suspension_lab.config import BOND_MID_THRESHOLD, LabConfig
from suspension_lab.kalshi_client import KalshiBookFeed
from suspension_lab.session import SessionLogger


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

        self.root = tk.Tk()
        self.root.title("Suspension Edge Lab")
        self.root.geometry("980x720")
        self.root.configure(padx=8, pady=8)
        self._build_ui()
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.bind("<KeyPress-b>", lambda _e: self._toggle("b365"))
        self.root.bind("<KeyPress-B>", lambda _e: self._toggle("b365"))
        self.root.bind("<KeyPress-f>", lambda _e: self._toggle("fanduel"))
        self.root.bind("<KeyPress-F>", lambda _e: self._toggle("fanduel"))
        self.root.bind("<KeyPress-d>", lambda _e: self._toggle("draftkings"))
        self.root.bind("<KeyPress-D>", lambda _e: self._toggle("draftkings"))

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root)
        top.pack(fill="x", pady=(0, 8))
        ttk.Label(top, text=f"Game: {self.config.game_label or '(unnamed)'}").pack(side="left")
        ttk.Label(top, text=f"Session: {self.logger.session_dir.name}").pack(side="right")

        self.status_var = tk.StringVar(value="Starting…")
        ttk.Label(self.root, textvariable=self.status_var, foreground="#444").pack(anchor="w")

        books_frame = ttk.LabelFrame(self.root, text="Kalshi orderbooks (live)")
        books_frame.pack(fill="both", expand=True, pady=8)
        self.book_text = scrolledtext.ScrolledText(books_frame, height=16, font=("Consolas", 10))
        self.book_text.pack(fill="both", expand=True)

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
            "B = bet365 up/down toggle · F = FanDuel · D = DraftKings · "
            f"Bond filter threshold: {BOND_MID_THRESHOLD:.0%} mid"
        )
        ttk.Label(self.root, text=help_text, foreground="#666").pack(anchor="w", pady=(4, 0))

    def _books_for_log(self) -> dict[str, dict]:
        out: dict[str, dict] = {}
        for t, book in self.feed.books.items():
            levels = book.top_levels()
            levels["book_json"] = book.full_json()
            out[t] = levels
        return out

    def _on_book(self, _ticker: str, _book) -> None:
        self.root.after(0, self._refresh_display)

    def _on_status(self, msg: str) -> None:
        self.root.after(0, lambda: self.status_var.set(msg))

    def _refresh_display(self) -> None:
        lines: list[str] = []
        for ticker in self.config.tickers:
            book = self.feed.books.get(ticker)
            if not book:
                continue
            lv = book.top_levels()
            self._book_cache[ticker] = lv
            bond = " [BOND - skip]" if lv.get("is_bond") else ""
            wide = " [WIDE - no taker]" if lv.get("wide_spread") else ""
            tight = " [TIGHT - ok]" if lv.get("tight_spread") else ""
            lines.append(
                f"{ticker}{bond}{wide}{tight}\n"
                f"  bid {lv.get('yes_bid','?')} x {lv.get('yes_bid_qty','?')} (3lvl {lv.get('bid_depth_3','?')})  |  "
                f"ask {lv.get('yes_ask','?')} x {lv.get('yes_ask_qty','?')} (3lvl {lv.get('ask_depth_3','?')})\n"
                f"  spread {lv.get('spread_cents','?')}¢  mid {lv.get('yes_mid','?')}  "
                f"suggest bid {lv.get('suggested_bid_plus_2c','?')}\n"
            )
        self.book_text.delete("1.0", tk.END)
        self.book_text.insert(tk.END, "\n".join(lines) if lines else "Waiting for books…")

    def _sync_flag_labels(self) -> None:
        self.b365_var.set(self.logger.flags.b365)
        self.fd_var.set(self.logger.flags.fanduel)
        self.dk_var.set(self.logger.flags.draftkings)
        color = {"UP": "#1a7f37", "DOWN": "#cf222e"}
        # tk doesn't support per-label color easily; state text is enough

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
