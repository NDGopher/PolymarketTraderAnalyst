# Suspension Edge Lab — Manual click logger for book suspensions vs Kalshi orderbooks

See **[WINDOWS_SETUP.md](../WINDOWS_SETUP.md)** for clone + one-click install on Windows.

Quick run (after `.env` is configured):

```bat
START_SUSPENSION_LAB.bat
```

## Auto-discovery (NEW)

When you launch the lab **without** `--tickers`, it automatically discovers in-play or imminent soccer games from Kalshi. `.env LAB_TICKERS` is ignored (it is not a pin list):

```bash
# No tickers needed — auto-discover soccer games with volume
python -m suspension_lab.cli
```

The auto-discovery:
- Queries Kalshi's public API for open soccer markets
- Groups markets by game and funds:
  - **Home ML** / **Away ML** (liquid TIE is funded)
  - The **total nearest 50¢ YES from live prices** (ATM). A 0-1 / 1-0 grind with O1.5 at ~50¢ funds **O1.5**, not leftover O3.5/O4.5. 1-1 / ≥3 goals → O3.5+O4.5 is that ATM special case, not a hard pin.
  - The **next strike up** if liquid (skip ~90¢ O0.5 bonds). Dead wings (untradeable, bid missing, YES < ~10¢) are dropped on the rediscover timer. If O4.5 drifts far from 50¢ with no more goals, swap to the cheaper adjacent (O2.5 or O1.5).
- Rank: **in-play first**, then kickoff-soon, then 24h volume. No team-name bias.
- Fingerprint discovery (Egypt, TFF, Coppa, cups, second divisions) — prefix list is a boost, not a closed set
- Finished / yesterday books are dropped. Empty start stays REST-idle (no empty WS subscribe) and rescans
- Totals **rediscover on a timer** while the session runs (no restart). Dead wings leave the fund list.
- Logs which tickers were added and why

### Auto-discovery options

```bash
# Discover up to 3 games with higher volume threshold
python -m suspension_lab.cli --max-games 3 --min-volume 100

# Disable auto-discovery (start with empty tickers)
python -m suspension_lab.cli --no-auto-discover
```

### Supported leagues

Auto-discovery picks **today / tonight** by `occurrence_datetime` (not Saturday volume). Supported series include:
- **EPL**, **La Liga**, **Bundesliga**, **Serie A**, **Ligue 1**
- **Champions League**, **Europa League**, **Conference League**
- **Coppa Italia**, **EFL Championship**
- **MLS**, **USL**, **NWSL**, **World Cup**
- **Brasileirão** A/B, **Liga MX**
- **Peru Liga 1**, **Argentina Primera**, **Chile**, **Colombia (DIMAYOR)**
- **Ecuador LigaPro**, **Venezuela**, **Libertadores / Sudamericana**
- **Super League Greece**, **Greek Cup**
- **Egypt Premier League**, **Turkish TFF 1. Lig**
- Plus any other open Kalshi soccer GAME/TOTAL (fingerprint, not a whitelist)

Unattended paper logger (no UI, no live bets):

```bash
python -m suspension_lab.paper_logger
python -m suspension_lab.cli --digest-only
python -m suspension_lab.cli --headless
```

GOAL is detected from the **order book** (bid jump or spread blowout), not a score feed. Paper scalp makes around the jump (bid+1¢) — never mid-only. Fees peak at 50¢ so near-50 prints with a tight spread are skipped. VAR / delayed / red-card-like grinds flatten or skip.

## Switch to a new game (manual)

1. Close the lab (choose **No** to delete empty test sessions).
2. Paste extra tickers in the UI after launch, or pass an explicit CLI `--tickers KX…` (real Kalshi ticker only). Do not pin yesterday in `.env`.
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

## Session analysis digest (NEW)

After a session, run the digest to get a complete summary:

```powershell
python -m suspension_lab.analyze_digest data/suspension_lab/sessions/YOUR_SESSION
```

The digest includes:
- **Signal summary:** total goal signals, spoof bids, VAR events
- **Fill verification:** which signals would have filled (FILL/PARTIAL/NO_FILL)
- **P&L analysis:** gross vs adjusted (FILL/PARTIAL only)
- **Per-line performance:** ML vs O0.5 vs O1.5 breakdown
- **Conclusions:** whether paper edge looks real

Output: `analysis.md` in the session folder.

## Replay & backtest (after a session)

```powershell
python -m suspension_lab.replay_goal_signals data/suspension_lab/sessions/YOUR_SESSION
python -m suspension_lab.backtest_exits data/suspension_lab/sessions/YOUR_SESSION 0    # join bid
python -m suspension_lab.backtest_exits data/suspension_lab/sessions/YOUR_SESSION 1    # bid+1¢
python -m suspension_lab.analyze_fills data/suspension_lab/sessions/YOUR_SESSION 100
python -m suspension_lab.fill_verifier data/suspension_lab/sessions/YOUR_SESSION 50    # fill check
python -m suspension_lab.lead_lag data/suspension_lab/sessions/YOUR_SESSION            # lead/lag
python -m suspension_lab.analyze_digest data/suspension_lab/sessions/YOUR_SESSION      # full digest
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
