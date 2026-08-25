# Strategy Dossier: Winnertraders

- **Wallet:** `0x13464aabec792c36b062316f474713e681330448`
- **History span:** 2026-01-16T07:37:14+00:00 → 2026-08-23T03:42:52+00:00 (218.84 days)
- **Trades:** 20,475 (buys 11,909 / sells 8,566)
- **Markets touched:** 2,750
- **Closed positions:** 3,001

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $16,661.90 |
| Core cashflow (ex-rebates) | $16,180.10 |
| Closed-positions realized sum | -$844.29 |
| Win rate (closed) | 65.11% (1952W / 1046L) |
| Profit factor | 0.9845 |
| Gross wins / losses | $53,716.10 / -$54,560.40 |
| Equity max drawdown | -$1,644.51 |
| Polymarket leaderboard (ALL) | $17,578.63 PnL · vol $2,032,708.12 · rank 9024 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=16661.9043 ref=17578.63221507959 diff=-916.7279
- **MATCH** `polydata` realized_pnl: ours=16661.9043 ref=17655.63 diff=-993.7257
- **DRIFT** `polydata` n_trades: ours=20475 ref=16162 diff=4313
- **DRIFT** `polydata` win_rate: ours=0.6511 ref=0.5926 diff=0.0585
- **DRIFT** `internal` cashflow_vs_closed: ours=16661.9043 ref=-844.295 diff=17506.1993

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 65/100)

- Fast round-trips (<2h) in 81% of two-sided markets
- Avg sell > avg buy in 77% of markets (spread capture)
- High-frequency cadence (median gap 100s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.0924, fast round-trips: 0.8133, spread-capture rate: 0.7712.

## Exact edge thesis

Winnertraders primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $9,253.28 across 1441 closed legs
- **other**: $994.88 across 152 closed legs
- **crypto**: -$294.95 across 33 closed legs
- **sports_match**: -$10,797.51 across 1375 closed legs

## Timing

- Peak UTC hours: 16, 17, 15, 20, 14
- Peak weekdays (0=Mon): [5, 6, 4]
- Median inter-trade gap: 1m 40s

## Sizing

- Median ticket $6.80, mean $22.67, p90 $62.50, max $2,575.00
- Share size median 29.04, mean 99.0755

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Mavericks vs. Bucks: O/U 218.5
- Entries ≈ **0.095** · Exits ≈ **0.484** · Spread ≈ **0.390**
- Fills: 14 buys / 3 sells · hold 11h 46m · both-sides=False · realized $2,507.61

### ODI Series Bangladesh vs New Zealand: Bangladesh vs New Zealand
- Entries ≈ **0.379** · Exits ≈ **0.399** · Spread ≈ **0.020**
- Fills: 26 buys / 15 sells · hold 18h 1m · both-sides=True · realized $1,681.83

### Atlanta Braves vs. Chicago White Sox: O/U 8.5
- Entries ≈ **0.103** · Exits ≈ **0.309** · Spread ≈ **0.206**
- Fills: 21 buys / 49 sells · hold 45d 11h · both-sides=True · realized $700.14

### Will India win?
- Entries ≈ **0.124** · Exits ≈ **0.426** · Spread ≈ **0.302**
- Fills: 11 buys / 10 sells · hold 15h 34m · both-sides=True · realized $607.74

### T20 World Cup: Namibia vs Netherlands (Game 1)
- Entries ≈ **0.056** · Exits ≈ **0.156** · Spread ≈ **0.101**
- Fills: 38 buys / 13 sells · hold 3h 0m · both-sides=True · realized $571.57

### ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa
- Entries ≈ **0.190** · Exits ≈ **0.250** · Spread ≈ **0.060**
- Fills: 19 buys / 10 sells · hold 6h 42m · both-sides=False · realized $551.84

### Switzerland vs. Colombia: O/U 8.5 Total Corners
- Entries ≈ **0.359** · Exits ≈ **0.999** · Spread ≈ **0.640**
- Fills: 2 buys / 2 sells · hold 5m 55s · both-sides=False · realized $448.30

### Team USA Stars vs. Team USA Stripes
- Entries ≈ **0.178** · Exits ≈ **0.536** · Spread ≈ **0.359**
- Fills: 10 buys / 15 sells · hold 28m 26s · both-sides=True · realized $434.89

### T20 World Cup: England vs Nepal (Game 1)
- Entries ≈ **0.024** · Exits ≈ **0.113** · Spread ≈ **0.089**
- Fills: 26 buys / 27 sells · hold 3h 2m · both-sides=True · realized $396.01

### T20 World Cup, Sub Regional Africa, Qualifier A: Kenya vs Rwanda
- Entries ≈ **0.170** · Exits ≈ **0.465** · Spread ≈ **0.294**
- Fills: 14 buys / 25 sells · hold 47m 1s · both-sides=True · realized $391.40

## Top closed winners / losers

**Winners**
- Mavericks vs. Bucks: O/U 218.5: $2,507.61 · bought $607.89 · sold $3,115.47 · hold 11h 46m
- ODI Series Bangladesh vs New Zealand: Bangladesh vs New Zealand: $1,681.83 · bought $467.72 · sold $490.84 · hold 18h 1m
- Germany vs. Latvia: O/U 5.5: $841.25 · bought $48.68 · sold $889.93 · hold 22m 2s
- Atlanta Braves vs. Chicago White Sox: O/U 8.5: $700.14 · bought $349.30 · sold $1,049.72 · hold 45d 11h
- Will India win?: $607.74 · bought $254.82 · sold $876.75 · hold 15h 34m
- Spread: Real Madrid CF (-1.5): $585.90 · bought $141.75 · sold $727.65 · hold 1m 36s
- T20 World Cup: Namibia vs Netherlands (Game 1): $571.57 · bought $316.95 · sold $888.52 · hold 3h 0m
- ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa: $551.84 · bought $345.05 · sold $446.27 · hold 6h 42m
- Switzerland vs. Colombia: O/U 8.5 Total Corners: $448.30 · bought $251.00 · sold $699.29 · hold 5m 55s
- Team USA Stars vs. Team USA Stripes: $434.89 · bought $215.24 · sold $650.13 · hold 28m 26s

**Losers**
- Indian Premier League: Kolkata Knight Riders vs Sunrisers Hyderabad: -$2,394.22 · bought $631.01 · sold $806.98
- Pakistan Super League: Peshawar Zalmi vs Multan Sultans: -$2,176.10 · bought $138.51 · sold $170.45
- T20 Series Namibia vs Scotland: Namibia vs Scotland: -$1,272.23 · bought $276.06 · sold $97.34
- Indian Premier League: Mumbai Indians vs Lucknow Super Giants: -$1,268.29 · bought $146.91 · sold $68.08
- T20 Challenge Trophy, Women: Rwanda vs Nepal: -$1,267.38 · bought $40.45 · sold $245.55
- T20 Series Indonesia vs Sweden: Indonesia vs Sweden: -$1,100.42 · bought $194.85 · sold $768.75
- Indian Premier League: Chennai Super Kings vs Delhi Capitals: -$881.33 · bought $241.53 · sold $153.92
- T20 Series Bangladesh vs Sri Lanka, Women: Bangladesh vs Sri Lanka: -$846.30 · bought $47.99 · sold $189.21
- Indian Premier League: Chennai Super Kings vs Kolkata Knight Riders: -$815.00 · bought $276.98 · sold $316.80
- T20 Series South Africa vs. India, Women: South Africa vs India: -$729.97 · bought $224.88 · sold $85.41

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$6.80) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $224,791.72
- Sells: $239,727.95
- Redeems: $1,243.87
- Maker rebates: $378.60
- Taker rebates: $15.58

_Generated 2026-08-25T21:55:36.206160+00:00_
