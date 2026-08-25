# Strategy Dossier: polika72

- **Wallet:** `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`
- **History span:** 2026-03-12T17:59:13+00:00 → 2026-08-25T15:48:07+00:00 (165.91 days)
- **Trades:** 19,978 (buys 9,077 / sells 10,901)
- **Markets touched:** 5,422
- **Closed positions:** 5,035

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $58,204.98 |
| Core cashflow (ex-rebates) | $57,699.08 |
| Closed-positions realized sum | $61,909.37 |
| Win rate (closed) | 80.08% (4032W / 1003L) |
| Profit factor | 3.2979 |
| Gross wins / losses | $88,851.53 / -$26,942.16 |
| Equity max drawdown | -$2,214.97 |
| Polymarket leaderboard (ALL) | $57,338.72 PnL · vol $1,049,905.19 · rank 3244 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=57699.0816 ref=57338.716846567695 diff=360.3648
- **DRIFT** `polydata` realized_pnl: ours=57699.0816 ref=52640.69 diff=5058.3916
- **DRIFT** `polydata` n_trades: ours=19978 ref=24078 diff=-4100
- **DRIFT** `polydata` win_rate: ours=0.8008 ref=0.6567 diff=0.1441
- **MATCH** `internal` cashflow_vs_closed: ours=58204.9839 ref=61909.3681 diff=-3704.3842

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 65/100)

- Fast round-trips (<2h) in 100% of two-sided markets
- Avg sell > avg buy in 84% of markets (spread capture)
- High-frequency cadence (median gap 45s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.0068, fast round-trips: 0.9984, spread-capture rate: 0.8376.

## Exact edge thesis

polika72 looks like a **market maker on a scanner score**, but the fill tape says otherwise: they almost never warehouse both outcomes. The real edge is **one-sided live scalping** on sports (especially O/U Over) — buy a clip, sell the same outcome higher within seconds/minutes, maker-biased, rinse and repeat. Equity compounds from thousands of small positive markouts, not from predicting finals.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $40,877.63 across 3321 closed legs
- **sports_match**: $14,704.20 across 1135 closed legs
- **other**: $6,180.60 across 576 closed legs
- **crypto**: $146.94 across 3 closed legs

## Timing

- Peak UTC hours: 19, 18, 14, 0, 17
- Peak weekdays (0=Mon): [6, 5, 3]
- Median inter-trade gap: 45s

## Sizing

- Median ticket $10.57, mean $23.13, p90 $52.52, max $1,479.63
- Share size median 24.5, mean 49.1094

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
- Entries ≈ **0.370** · Exits ≈ **0.599** · Spread ≈ **0.229**
- Fills: 6 buys / 9 sells · hold 1h 12m · both-sides=False · realized $841.93

### FC Bayern München vs. Real Madrid CF: O/U 4.5
- Entries ≈ **0.544** · Exits ≈ **0.692** · Spread ≈ **0.148**
- Fills: 7 buys / 4 sells · hold 28m 48s · both-sides=False · realized $670.10

### FC Bayern München vs. Real Madrid CF: O/U 3.5
- Entries ≈ **0.651** · Exits ≈ **0.775** · Spread ≈ **0.124**
- Fills: 4 buys / 4 sells · hold 6m 2s · both-sides=False · realized $645.59

### FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
- Entries ≈ **0.188** · Exits ≈ **0.275** · Spread ≈ **0.087**
- Fills: 7 buys / 24 sells · hold 1h 18m · both-sides=False · realized $640.86

### Will Club Atlético de Madrid win on 2026-08-23?
- Entries ≈ **0.426** · Exits ≈ **0.748** · Spread ≈ **0.322**
- Fills: 2 buys / 3 sells · hold 2m 18s · both-sides=False · realized $629.26

### FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
- Entries ≈ **0.569** · Exits ≈ **0.889** · Spread ≈ **0.320**
- Fills: 5 buys / 6 sells · hold 1h 10m · both-sides=False · realized $544.83

### Paris Saint-Germain vs. Aston Villa: O/U 3.5
- Entries ≈ **0.360** · Exits ≈ **0.610** · Spread ≈ **0.250**
- Fills: 11 buys / 4 sells · hold 58s · both-sides=False · realized $508.06

### Will Paris Saint-Germain FC win on 2026-04-14?
- Entries ≈ **0.210** · Exits ≈ **0.650** · Spread ≈ **0.440**
- Fills: 3 buys / 9 sells · hold 44s · both-sides=False · realized $504.28

### Netherlands vs. Japan: O/U 4.5
- Entries ≈ **0.050** · Exits ≈ **0.136** · Spread ≈ **0.087**
- Fills: 3 buys / 4 sells · hold 9m 30s · both-sides=False · realized $502.30

### US Cremonese vs. Bologna FC 1909: O/U 2.5
- Entries ≈ **0.440** · Exits ≈ **0.670** · Spread ≈ **0.231**
- Fills: 3 buys / 17 sells · hold 1m 46s · both-sides=False · realized $463.71

## Top closed winners / losers

**Winners**
- FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5: $841.93 · bought $508.32 · sold $838.49 · hold 1h 12m
- FC Bayern München vs. Real Madrid CF: O/U 4.5: $670.10 · bought $811.14 · sold $1,043.98 · hold 28m 48s
- FC Bayern München vs. Real Madrid CF: O/U 3.5: $645.59 · bought $755.61 · sold $908.66 · hold 6m 2s
- FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5: $640.86 · bought $245.95 · sold $368.77 · hold 1h 18m
- Will Club Atlético de Madrid win on 2026-08-23?: $629.26 · bought $892.75 · sold $1,567.38 · hold 2m 18s
- Will Real Madrid CF win on 2026-03-17?: $564.47 · bought $44.59 · sold $609.06 · hold 13m 6s
- FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5: $544.83 · bought $417.14 · sold $660.50 · hold 1h 10m
- Paris Saint-Germain vs. Aston Villa: O/U 3.5: $508.06 · bought $731.95 · sold $930.01 · hold 58s
- Will Paris Saint-Germain FC win on 2026-04-14?: $504.28 · bought $286.21 · sold $907.85 · hold 44s
- Netherlands vs. Japan: O/U 4.5: $502.30 · bought $297.03 · sold $817.91 · hold 9m 30s

**Losers**
- RC Strasbourg Alsace vs. OGC Nice: O/U 3.5: -$515.82 · bought $284.54 · sold $230.58
- Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5: -$508.72 · bought $270.55 · sold $260.04
- Panama vs. England: Both Teams to Score: -$474.32 · bought $503.98 · sold $30.54
- Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5: -$471.20 · bought $289.76 · sold $399.53
- Will Paris Saint-Germain FC win on 2026-04-22?: -$427.80 · bought $58.50 · sold $150.60
- RC Strasbourg Alsace vs. OGC Nice: O/U 4.5: -$427.77 · bought $123.17 · sold $81.78
- Sporting CP vs. Arsenal FC: O/U 2.5: -$416.80 · bought $47.18 · sold $42.35
- UD Las Palmas vs. SD Huesca: O/U 3.5: -$414.38 · bought $152.34 · sold $130.84
- Real Madrid CF vs. Deportivo Alavés: O/U 3.5: -$388.13 · bought $359.04 · sold $313.15
- Cádiz CF vs. Córdoba CF: O/U 4.5: -$384.52 · bought $100.00 · sold $239.85

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$10.57) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $203,970.44
- Sells: $259,522.26
- Redeems: $2,147.26
- Maker rebates: $481.53
- Taker rebates: $24.37

_Generated 2026-08-25T16:46:52.153099+00:00_
