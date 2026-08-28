# Strategy Dossier: DrPufferfish

- **Wallet:** `0xdb27bf2ac5d428a9c63dbc914611036855a6c56e`
- **History span:** 2025-05-29T20:52:43+00:00 → 2026-01-12T20:49:11+00:00 (228.0 days)
- **Trades:** 64,290 (buys 60,876 / sells 3,414)
- **Markets touched:** 719
- **Closed positions:** 881

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $4,176,633.54 |
| Core cashflow (ex-rebates) | $4,175,613.54 |
| Closed-positions realized sum | $46,297,730.97 |
| Win rate (closed) | 90.22% (793W / 86L) |
| Profit factor | 21.0256 |
| Gross wins / losses | $48,609,653.80 / -$2,311,922.83 |
| Equity max drawdown | -$1,608,581.77 |
| Polymarket leaderboard (ALL) | $4,055,413.26 PnL · vol $248,548,251.18 · rank 30 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=4175613.5447 ref=4055413.259574452 diff=120200.2851
- **MATCH** `polydata` realized_pnl: ours=4175613.5447 ref=4055413.26 diff=120200.2847
- **DRIFT** `polydata` n_trades: ours=64290 ref=272027 diff=-207737
- **DRIFT** `polydata` win_rate: ours=0.9022 ref=0.481 diff=0.4212
- **DRIFT** `internal` cashflow_vs_closed: ours=4176633.543 ref=46297730.9682 diff=-42121097.4252

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 55/100)

- Fast round-trips (<2h) in 30% of two-sided markets
- Avg sell > avg buy in 62% of markets (spread capture)
- High-frequency cadence (median gap 14s)

Supporting rates — both-sides markets: 0.1127, fast round-trips: 0.2976, spread-capture rate: 0.619.

## Exact edge thesis

DrPufferfish primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $43,141,219.15 across 701 closed legs
- **sports_totals**: $2,456,274.18 across 36 closed legs
- **other**: $647,948.05 across 133 closed legs
- **crypto**: $52,289.58 across 11 closed legs

## Timing

- Peak UTC hours: 19, 18, 0, 23, 21
- Peak weekdays (0=Mon): [5, 0, 6]
- Median inter-trade gap: 14s

## Sizing

- Median ticket $1.98, mean $415.51, p90 $108.42, max $248,000.00
- Share size median 27.0, mean 1043.8585

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Spurs vs. Lakers
- Entries ≈ **0.301** · Exits ≈ **0.710** · Spread ≈ **0.409**
- Fills: 334 buys / 104 sells · hold 22h 21m · both-sides=True · realized $255,573.09

### Bucks vs. Bulls
- Entries ≈ **0.441** · Exits ≈ **0.460** · Spread ≈ **0.019**
- Fills: 39 buys / 29 sells · hold 7h 26m · both-sides=False · realized $158,514.04

### Magic vs. Knicks
- Entries ≈ **0.480** · Exits ≈ **0.558** · Spread ≈ **0.078**
- Fills: 10 buys / 53 sells · hold 1h 50m · both-sides=True · realized $138,921.06

### Will Real Madrid win on 2025-11-23?
- Entries ≈ **0.303** · Exits ≈ **0.320** · Spread ≈ **0.017**
- Fills: 162 buys / 2 sells · hold 1h 27m · both-sides=False · realized $117,445.17

### Boxing: Canelo Álvarez vs. Terence Crawford 
- Entries ≈ **0.219** · Exits ≈ **0.445** · Spread ≈ **0.225**
- Fills: 87 buys / 4 sells · hold 9h 25m · both-sides=True · realized $114,649.29

### Pelicans vs. Nets
- Entries ≈ **0.592** · Exits ≈ **0.600** · Spread ≈ **0.009**
- Fills: 28 buys / 17 sells · hold 5h 38m · both-sides=False · realized $102,314.62

### Heat vs. Magic
- Entries ≈ **0.477** · Exits ≈ **0.520** · Spread ≈ **0.043**
- Fills: 360 buys / 7 sells · hold 1d 23h · both-sides=True · realized $90,919.01

### Cardinals vs. Cowboys
- Entries ≈ **0.333** · Exits ≈ **0.896** · Spread ≈ **0.563**
- Fills: 75 buys / 16 sells · hold 2h 44m · both-sides=True · realized $82,072.63

### Rockets vs. Lakers
- Entries ≈ **0.534** · Exits ≈ **0.560** · Spread ≈ **0.026**
- Fills: 195 buys / 79 sells · hold 23h 47m · both-sides=False · realized $75,885.11

### Cavaliers vs. Pacers
- Entries ≈ **0.610** · Exits ≈ **0.630** · Spread ≈ **0.020**
- Fills: 3 buys / 13 sells · hold 13m 0s · both-sides=False · realized $58,668.80

## Top closed winners / losers

**Winners**
- Will the New York Knicks win the 2026 NBA Finals?: $600,658.75 · bought $2,239.04 · sold $0.00 · hold 4d 8h
- Hawks vs. Knicks: $495,581.93 · bought $268,046.98 · sold $175.51 · hold 9h 51m
- Hornets vs. Thunder: $315,612.42 · bought $39,008.28 · sold $0.00 · hold 15m 12s
- Will Liverpool FC win on 2026-01-01?: $299,232.99 · bought $151,877.40 · sold $0.00 · hold 21m 16s
- Nuggets vs. Mavericks: $289,219.21 · bought $127,072.16 · sold $0.00 · hold 2h 52m
- Spread: Patriots (-3.5): $270,717.18 · bought $270,858.73 · sold $0.00 · hold 11h 53m
- Spread: Eagles (-4.5): $261,750.14 · bought $218,805.30 · sold $0.00 · hold 5h 49m
- Spurs vs. Lakers: $255,573.09 · bought $111,321.09 · sold $8,199.48 · hold 22h 21m
- Spread: Broncos (-13.5): $252,076.15 · bought $248,929.31 · sold $0.00 · hold 14m 0s
- Spread: Raptors (-2.5): $233,888.50 · bought $233,888.50 · sold $0.00 · hold 0s

**Losers**
- Pistons vs. Celtics: -$123,412.12 · bought $130,983.15 · sold $7,555.48
- Spread: Pistons (-9.5): -$108,248.05 · bought $108,715.92 · sold $0.00
- Chiefs vs. Broncos: -$87,922.18 · bought $93,485.12 · sold $0.00
- Spread: Thunder (-11.5): -$84,368.74 · bought $124,688.78 · sold $16,320.00
- Falcons vs. Vikings: -$67,653.93 · bought $76,706.61 · sold $0.00
- Eagles vs. Chargers: -$65,540.87 · bought $103,386.95 · sold $0.00
- Thunder vs. Jazz: -$39,793.93 · bought $50,169.65 · sold $0.00
- Champions League Final: 3+ goals?: -$32,532.08 · bought $32,532.08 · sold $0.00
- Will the Seattle Mariners win the 2025 World Series?: -$29,671.92 · bought $7,886.02 · sold $42,955.62
- UFC Fight Night: Muhammad vs. Machado Garry (Welterweight, Main Card): -$29,143.07 · bought $32,589.64 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$1.98) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $25,315,785.94
- Sells: $1,397,272.18
- Redeems: $28,094,127.30
- Maker rebates: $0.00
- Taker rebates: $0.00

_Generated 2026-08-28T14:18:31.630397+00:00_
