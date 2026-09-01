# Suspension Edge Lab — Manual click logger for book suspensions vs Kalshi orderbooks

See **[WINDOWS_SETUP.md](../WINDOWS_SETUP.md)** for clone + one-click install on Windows.

Quick run (after `.env` is configured):

```bat
START_SUSPENSION_LAB.bat
```

## Switch to a new game

1. Close the lab (choose **No** to delete empty test sessions).
2. Edit `.env`:
   ```env
   LAB_TICKERS=NEW_TICKER_O35,NEW_TICKER_O45
   LAB_GAME=TeamA-TeamB
   ```
3. Run the launcher again. Each run creates a new session folder.

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
