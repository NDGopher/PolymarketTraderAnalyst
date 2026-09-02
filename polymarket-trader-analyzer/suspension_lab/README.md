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
python -m suspension_lab.fill_verifier data/suspension_lab/sessions/YOUR_SESSION 50    # fill check
python -m suspension_lab.lead_lag data/suspension_lab/sessions/YOUR_SESSION            # lead/lag
```

Exit modes: **hold_bond** (near-won), **scalp** (+7¢), **var_watch** (VAR protection).

## Per-line exit policy

Different ticker types have different exit behaviors after a goal signal:

| Ticker type | Description | Exit policy |
|-------------|-------------|-------------|
| **ML** (moneyline) | Home/away win markets | scalp +7¢ or var_watch |
| **O0.5** (TOTAL-x-1) | Over 0.5 goals | hold_bond when bonded, never scalp +7 |
| **O1.5+** (TOTAL-x-2, etc.) | Over 1.5+ goals | scalp +7¢ or var_watch |

**Why O0.5 is different:** After a goal, O0.5 instantly bonds to 99¢ (certainty). Taking a +7¢ scalp exit makes no sense — hold for resolution at 99¢ or watch for spoof bids.

### Spoof bid detection

A **spoof bid** appears on bonded O0.5 markets:

- Peak was ≥95¢ (bonded)
- Bid drops significantly (e.g. to 75¢)
- Ask stays high (≥95¢)
- Bid qty is thin (<100 contracts)
- Wide spread (24¢+)

This is NOT a VAR revert. The spoof filter:
- Shows amber **SPOOF** banner instead of red **VAR** alert
- Does **not** trigger paper trader exit
- Dedupes to once per episode

Real VAR (goal cancelled) looks different:
- Both bid AND ask collapse together
- Spread stays tight
- Book returns to pre-goal levels

## Fill verification

After running a session, verify whether orders would have filled:

```powershell
python -m suspension_lab.fill_verifier data/suspension_lab/sessions/YOUR_SESSION 50
```

Outputs:
- `fill_would_have.csv` — raw verdicts per signal/strategy
- `fill_would_have.md` — markdown summary

Verdicts:
- **FILL** — bid lifted past target or queue consumed
- **PARTIAL** — some queue consumed, partial fill likely
- **NO_FILL** — deep queue, no lift

Backtest P&L should only count FILL or conservative PARTIAL.

## Lead/lag analysis

Track which ticker moves first on goal episodes:

```powershell
python -m suspension_lab.lead_lag data/suspension_lab/sessions/YOUR_SESSION
```

Outputs:
- `lead_lag.csv` — timing data per episode/ticker
- `lead_lag.md` — summary with leader counts

Shows first timestamp for bid jump ≥10¢ and ask jump ≥3¢ per tracked ticker.

## Books CSV formats

The lab saves two orderbook formats:

| File | Format | Contents |
|------|--------|----------|
| `books.csv` | Wide | Original tickers only (columns per ticker) |
| `books_long.csv` | Long | All tickers including runtime-added (one row per ticker per sample) |

Replay, backtest, and fill tools **prefer `books_long.csv`** when present, falling back to `books.csv`.
