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

**Runtime tickers:** Use the text box at the top of the UI to add Kalshi tickers while the session runs.

## Notes (replaces book flags)

- Type observations in the **Notes** pad at the bottom
- Click **Add note** (or press Enter in the note field) to append a timestamped line
- You can also type freely in the notes area — everything saves to `notes.txt` on close

## Paper auto-trader (no live orders yet)

Enable the checkbox in the UI, or set in `.env`:

```env
LAB_TRADER_ENABLED=1
LAB_TRADER_CONTRACTS=50
LAB_TRADER_BID_OFFSET_CENTS=1
```

- Enters at **signal bid + 1¢** (queue priority)
- **Mode-aware exits:** hold_bond / scalp / var_watch
- **VAR protection:** exits on revert, limbo, trailing stop
- Logs to `paper_trades.csv` in the session folder

## Close session

| Button | Action |
|--------|--------|
| **Yes** | Save logs + notes under `data/suspension_lab/sessions/` |
| **No** | Delete this session folder |
| **Cancel** | Keep running |

## Live goal signal (green box)

When a ticker’s **bid jumps ≥10¢** with **≥100 contracts** and **ask confirms**, the panel gets a green border.

- Shows **YES and NO** sides of the book
- Signals logged to `goal_signals.csv`
- VAR revert → red border

## Replay & backtest (after a session)

```powershell
python -m suspension_lab.replay_goal_signals data/suspension_lab/sessions/YOUR_SESSION
python -m suspension_lab.backtest_exits data/suspension_lab/sessions/YOUR_SESSION 0    # join bid
python -m suspension_lab.backtest_exits data/suspension_lab/sessions/YOUR_SESSION 1    # bid+1¢
python -m suspension_lab.analyze_fills data/suspension_lab/sessions/YOUR_SESSION 100
```

Exit modes: **hold_bond** (near-won), **scalp** (+7¢), **var_watch** (VAR protection).
