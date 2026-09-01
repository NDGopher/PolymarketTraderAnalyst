# Strategy Dossier: gmpm

- **Wallet:** `0x14964aefa2cd7caff7878b3820a690a03c5aa429`
- **History span:** 2025-09-12T20:54:51+00:00 → 2026-05-20T21:39:09+00:00 (250.03 days)
- **Trades:** 47,326 (buys 43,929 / sells 3,397)
- **Markets touched:** 845
- **Closed positions:** 1,063

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$5,400,173.37 |
| Core cashflow (ex-rebates) | -$5,401,057.55 |
| Closed-positions realized sum | $3,075,155.76 |
| Win rate (closed) | 54.61% (569W / 473L) |
| Profit factor | 1.2494 |
| Gross wins / losses | $15,403,396.51 / -$12,328,240.75 |
| Equity max drawdown | -$3,311,999.81 |
| Polymarket leaderboard (ALL) | $3,530,847.58 PnL · vol $87,349,857.86 · rank 42 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=3075155.7644 ref=3530847.5828185184 diff=-455691.8184
- **DRIFT** `polydata` realized_pnl: ours=3075155.7644 ref=3530847.58 diff=-455691.8156
- **MATCH** `polydata` n_trades: ours=47326 ref=45978 diff=1348
- **MATCH** `polydata` win_rate: ours=0.5461 ref=0.5448 diff=0.0013
- **DRIFT** `internal` cashflow_vs_closed: ours=-5400173.3742 ref=3075155.7644 diff=-8475329.1386

## What kind of trader is this?

**Classification:** `hybrid_mm_directional` (score 40/100)

- Fast round-trips (<2h) in 42% of two-sided markets
- High-frequency cadence (median gap 18s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.2592, fast round-trips: 0.4222, spread-capture rate: 0.4167.

## Exact edge thesis

gmpm looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $2,352,474.34 across 940 closed legs
- **sports_totals**: $509,347.32 across 108 closed legs
- **other**: $213,334.10 across 15 closed legs

## Timing

- Peak UTC hours: 20, 0, 17, 21, 19
- Peak weekdays (0=Mon): [6, 5, 4]
- Median inter-trade gap: 18s

## Sizing

- Median ticket $12.24, mean $941.62, p90 $662.79, max $394,800.00
- Share size median 24.76, mean 1797.2278

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Spread: Seahawks (-4.5)
- Entries ≈ **0.498** · Exits ≈ **0.510** · Spread ≈ **0.012**
- Fills: 935 buys / 91 sells · hold 13d 6h · both-sides=True · realized $201,964.31

### Texas State vs. Southern Miss
- Entries ≈ **0.399** · Exits ≈ **0.405** · Spread ≈ **0.006**
- Fills: 218 buys / 27 sells · hold 5h 24m · both-sides=False · realized $171,874.33

### Spread: Seahawks (-5.5)
- Entries ≈ **0.492** · Exits ≈ **0.520** · Spread ≈ **0.027**
- Fills: 1208 buys / 79 sells · hold 13d 7h · both-sides=True · realized $161,113.41

### North Carolina vs. Syracuse
- Entries ≈ **0.473** · Exits ≈ **0.479** · Spread ≈ **0.006**
- Fills: 17 buys / 7 sells · hold 2h 23m · both-sides=False · realized $133,817.35

### Spread: Patriots (-13.5)
- Entries ≈ **0.485** · Exits ≈ **0.490** · Spread ≈ **0.004**
- Fills: 610 buys / 3 sells · hold 3h 59m · both-sides=True · realized $107,620.72

### Spread: Patriots (-3.5)
- Entries ≈ **0.490** · Exits ≈ **0.510** · Spread ≈ **0.020**
- Fills: 536 buys / 7 sells · hold 8h 16m · both-sides=True · realized $69,862.80

### Will USA win the 2025 Ryder Cup?
- Entries ≈ **0.420** · Exits ≈ **0.690** · Spread ≈ **0.270**
- Fills: 240 buys / 79 sells · hold 1d 14h · both-sides=False · realized $63,670.07

### Will Arsenal win on 2025-09-21?
- Entries ≈ **0.506** · Exits ≈ **0.520** · Spread ≈ **0.014**
- Fills: 6 buys / 2 sells · hold 55m 0s · both-sides=False · realized $55,885.68

### Spread: 49ers (-3.5)
- Entries ≈ **0.501** · Exits ≈ **0.510** · Spread ≈ **0.009**
- Fills: 24 buys / 2 sells · hold 6h 24m · both-sides=True · realized $44,677.65

### Patriots vs. Broncos
- Entries ≈ **0.516** · Exits ≈ **0.660** · Spread ≈ **0.143**
- Fills: 428 buys / 3 sells · hold 6d 5h · both-sides=True · realized $37,956.82

## Top closed winners / losers

**Winners**
- Seahawks vs. Patriots: $862,149.49 · bought $2,150,359.45 · sold $344,905.47 · hold 13d 6h
- Boxing: Canelo Álvarez vs. Terence Crawford : $598,139.47 · bought $366,811.01 · sold $0.00 · hold 1d 7h
- Spread: Lions (-3.5): $332,851.08 · bought $361,754.06 · sold $0.00 · hold 1h 52m
- Chiefs vs. Bills: $318,948.00 · bought $255,046.00 · sold $4,444.00 · hold 1h 9m
- Chargers vs. Cowboys: $310,451.50 · bought $569,146.52 · sold $51,174.32 · hold 3h 40m
- Spread: Indiana (-7.5): $302,855.91 · bought $292,880.75 · sold $47.56 · hold 1d 4h
- Oregon vs. Texas Tech Red Raiders: $277,765.37 · bought $287,388.78 · sold $0.00 · hold 1h 49m
- Spread: Seahawks (-1.5): $270,996.20 · bought $269,414.10 · sold $0.00 · hold 1h 58m
- Spread: Seahawks (-6.5): $262,355.65 · bought $256,852.06 · sold $0.00 · hold 1h 53m
- Spread: Indiana (-3.5): $245,267.76 · bought $296,633.04 · sold $0.00 · hold 9h 40m

**Losers**
- Spread: Seahawks (-2.5): -$777,467.85 · bought $789,100.46 · sold $0.00
- Spread: Spurs (-9.5): -$690,130.98 · bought $30,906.00 · sold $0.00
- Spread: Rams (-10.5): -$666,476.23 · bought $666,866.47 · sold $375.97
- Miami vs. Ohio State: -$534,296.99 · bought $534,308.67 · sold $0.00
- Spread: Texas A&M (-3.5): -$288,363.77 · bought $288,366.97 · sold $0.00
- Ole Miss vs. Georgia: -$261,192.22 · bought $319,211.21 · sold $0.00
- Houston vs. UCF: -$248,787.29 · bought $248,804.04 · sold $0.00
- Packers vs. Lions: -$247,101.79 · bought $313,024.65 · sold $0.00
- Spread: Eagles (-6.5): -$241,870.20 · bought $245,062.04 · sold $0.00
- Spread: Oregon (-21.5): -$203,674.37 · bought $203,699.48 · sold $0.00

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $42,125,386.60
- Sells: $2,452,503.58
- Redeems: $34,271,825.47
- Maker rebates: $773.21
- Taker rebates: $0.00

_Generated 2026-09-01T15:10:23.658207+00:00_
