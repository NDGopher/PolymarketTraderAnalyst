# Strategy Dossier: 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465

- **Wallet:** `0x2c335066fe58fe9237c3d3dc7b275c2a034a0563`
- **History span:** 2025-10-08T15:39:18+00:00 → 2026-07-04T21:39:07+00:00 (269.25 days)
- **Trades:** 351,490 (buys 349,844 / sells 1,646)
- **Markets touched:** 4,314
- **Closed positions:** 9,489

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$29,849,472.90 |
| Core cashflow (ex-rebates) | -$29,957,480.73 |
| Closed-positions realized sum | $17,071,768.04 |
| Win rate (closed) | 60.52% (5720W / 3732L) |
| Profit factor | 1.1572 |
| Gross wins / losses | $125,677,974.10 / -$108,606,206.06 |
| Equity max drawdown | -$6,396,385.56 |
| Polymarket leaderboard (ALL) | $7,374,604.84 PnL · vol $1,000,345,735.50 · rank 16 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=17071768.0427 ref=7374604.843242512 diff=9697163.1995
- **DRIFT** `polydata` realized_pnl: ours=17071768.0427 ref=7387346.99 diff=9684421.0527
- **DRIFT** `polydata` n_trades: ours=351490 ref=324009 diff=27481
- **DRIFT** `polydata` win_rate: ours=0.6052 ref=0.5548 diff=0.0504
- **DRIFT** `internal` cashflow_vs_closed: ours=-29849472.9006 ref=17071768.0427 diff=-46921240.9433

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 55/100)

- Fast round-trips (<2h) in 28% of two-sided markets
- Avg sell > avg buy in 55% of markets (spread capture)
- High-frequency cadence (median gap 3s)

Supporting rates — both-sides markets: 0.2432, fast round-trips: 0.2833, spread-capture rate: 0.55.

## Exact edge thesis

0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465 primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $15,036,155.22 across 6285 closed legs
- **sports_totals**: $1,514,760.20 across 992 closed legs
- **crypto**: $946,750.60 across 597 closed legs
- **politics**: $19,932.05 across 2 closed legs
- **other**: -$445,830.02 across 1613 closed legs

## Timing

- Peak UTC hours: 0, 21, 19, 1, 18
- Peak weekdays (0=Mon): [5, 2, 4]
- Median inter-trade gap: 3s

## Sizing

- Median ticket $21.75, mean $915.00, p90 $415.86, max $1,357,531.15
- Share size median 35.6905, mean 1602.0682

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Will Manchester City FC win on 2026-05-16?
- Entries ≈ **0.521** · Exits ≈ **0.540** · Spread ≈ **0.019**
- Fills: 131 buys / 163 sells · hold 31m 10s · both-sides=True · realized $166,618.79

### Capitals vs. Rangers
- Entries ≈ **0.494** · Exits ≈ **0.500** · Spread ≈ **0.006**
- Fills: 11 buys / 9 sells · hold 2h 3m · both-sides=True · realized $47,972.71

### Swiss Indoors Basel: Jenson Brooksby vs Alejandro Davidovich Fokina
- Entries ≈ **0.548** · Exits ≈ **0.560** · Spread ≈ **0.013**
- Fills: 15 buys / 4 sells · hold 2h 17m · both-sides=False · realized $23,946.14

### Western Illinois Leathernecks vs. Southern Indiana Screaming Eagles: O/U 134.5
- Entries ≈ **0.550** · Exits ≈ **0.560** · Spread ≈ **0.010**
- Fills: 2 buys / 2 sells · hold 52s · both-sides=False · realized $22,761.00

### Will Arsenal win on 2025-10-18?
- Entries ≈ **0.608** · Exits ≈ **0.650** · Spread ≈ **0.042**
- Fills: 12 buys / 14 sells · hold 2h 27m · both-sides=True · realized $12,068.96

### Oilers vs. Rangers
- Entries ≈ **0.534** · Exits ≈ **0.550** · Spread ≈ **0.016**
- Fills: 4 buys / 4 sells · hold 12h 16m · both-sides=True · realized $5,195.19

### Will USA win the 2026 FIFA World Cup?
- Entries ≈ **0.024** · Exits ≈ **0.031** · Spread ≈ **0.007**
- Fills: 157 buys / 24 sells · hold 13d 21h · both-sides=False · realized $4,670.55

### Bengals vs. Packers
- Entries ≈ **0.846** · Exits ≈ **0.890** · Spread ≈ **0.044**
- Fills: 98 buys / 42 sells · hold 4d 0h · both-sides=True · realized $4,571.24

### Will Denmark win on 2026-06-07?
- Entries ≈ **0.624** · Exits ≈ **0.722** · Spread ≈ **0.099**
- Fills: 23 buys / 5 sells · hold 6h 20m · both-sides=True · realized $2,224.27

### LoL: T1 vs Invictus Gaming (BO5)
- Entries ≈ **0.541** · Exits ≈ **0.636** · Spread ≈ **0.095**
- Fills: 67 buys / 28 sells · hold 1h 54m · both-sides=True · realized $1,228.49

## Top closed winners / losers

**Winners**
- Will Belgium vs. Senegal end in a draw?: $1,927,053.10 · bought $601,142.60 · sold $0.00 · hold 2h 50m
- Will Morocco win on 2026-07-04?: $890,726.59 · bought $3,867,711.44 · sold $0.00 · hold 4h 21m
- Will Arsenal win the 2025–26 Champions League?: $718,775.55 · bought $1,055,955.12 · sold $0.00 · hold 11h 19m
- Will Belgium win on 2026-06-15?: $697,453.49 · bought $1,047,056.90 · sold $0.00 · hold 3h 26m
- Will Canada win on 2026-06-28?: $618,572.17 · bought $3,438,214.49 · sold $0.00 · hold 4h 49m
- Will Spain win the 2026 FIFA World Cup?: $556,597.78 · bought $0.00 · sold $10,988.48 · hold 3h 34m
- Will Scotland win on 2026-06-13?: $552,367.56 · bought $1,343,156.68 · sold $0.00 · hold 12h 1m
- Will Netherlands win on 2026-06-14?: $542,620.70 · bought $1,026,087.31 · sold $0.00 · hold 2h 36m
- Will Sweden win on 2026-06-14?: $515,409.83 · bought $1,043,026.52 · sold $0.00 · hold 5h 50m
- Will Portugal win on 2026-06-17?: $504,387.67 · bought $632,445.79 · sold $0.00 · hold 2h 1m

**Losers**
- Will Senegal win on 2026-07-01?: -$1,115,645.73 · bought $4,322,105.25 · sold $0.00
- Will IR Iran win on 2026-06-15?: -$737,895.80 · bought $3,274,303.46 · sold $0.00
- Will Spain win on 2026-06-15?: -$697,262.45 · bought $1,533,594.09 · sold $0.00
- Will Germany vs. Paraguay end in a draw?: -$654,131.80 · bought $2,485,888.37 · sold $0.00
- Senegal vs. Iraq: O/U 3.5: -$603,052.97 · bought $742,360.14 · sold $0.00
- Will Türkiye win on 2026-06-19?: -$566,280.13 · bought $1,090,489.94 · sold $0.00
- Will Paris Saint-Germain FC win on 2026-05-30?: -$557,671.52 · bought $3,324,638.89 · sold $979.90
- Germany vs. Paraguay: Team to Advance: -$548,641.04 · bought $970,893.63 · sold $0.00
- Will Portugal vs. DR Congo end in a draw?: -$454,895.55 · bought $453,536.20 · sold $0.00
- Will Ecuador win on 2026-06-25?: -$441,171.71 · bought $1,690,865.72 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$21.75) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $88,923,118.76
- Sells: $762,960.30
- Redeems: $58,202,677.73
- Maker rebates: $98,401.17
- Taker rebates: $0.00

_Generated 2026-09-01T15:13:18.425000+00:00_
