# Suspension Edge Lab — Manual click logger for book suspensions vs Kalshi orderbooks

See **[WINDOWS_SETUP.md](../WINDOWS_SETUP.md)** for clone + one-click install on Windows.

Quick run (after `.env` is configured):

```bat
START_SUSPENSION_LAB.bat
```

## Switch to a new game

1. Close the lab (choose **No** to delete empty test sessions).
2. Either edit `.env` **or** paste tickers in the UI after launch:
   ```env
   LAB_TICKERS=NEW_TICKER_O35,NEW_TICKER_O45   # optional — can add in UI instead
   LAB_GAME=TeamA-TeamB
   ```
3. Run the launcher again. Each run creates a new session folder.

**Runtime tickers:** Use the text box at the top of the UI to add Kalshi tickers while the session runs. Late adds log to `books_long.csv` (wide `books.csv` stays frozen to session-start tickers).

## Close session

| Button | Action |
|--------|--------|
| **Yes** | Save logs under `data/suspension_lab/sessions/` |
| **No** | Delete this session folder |
| **Cancel** | Keep running |

## Live goal signal (green box)

When a ticker’s **bid jumps ≥10¢ in one update** with **≥100 contracts** and the **ask confirms** (full book reprice, not ask-only scares), that market panel gets a **green border** and a goal banner.

- Human-readable title from Kalshi API (e.g. `EFL Championship — Swansea vs Watford — Over 3.5`)
- Ticker still shown underneath
- Signals logged to `goal_signals.csv` in the session folder
- 45s cooldown per ticker to avoid repeat flashes

Tape-only sessions work — no B/F clicking required.

## Replay & backtest (after a session)

```powershell
# Re-run goal-signal detector on saved tape
python -m suspension_lab.replay_goal_signals data/suspension_lab/sessions/YOUR_SESSION

# Simulate exit strategies (limit +7¢, hold bond, 20s time collar, recommended)
python -m suspension_lab.backtest_exits data/suspension_lab/sessions/YOUR_SESSION
```

Exit modes on the green banner:
- **hold_bond** — line crossing / near-won; hold toward 99¢
- **scalp** — open line (e.g. 1-1 → 2-1 on O2.5); take +7¢, don't need 95¢
- **var_watch** — suspicious spike; 25s limbo check + trailing stop
