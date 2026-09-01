# Strategy Dossier: Mysaria

- **Wallet:** `0xe40aaa5ce1dac0b7dc24c9d0284f27e17c3fe4a2`
- **History span:** 2026-08-05T16:01:44+00:00 → 2026-09-01T14:30:16+00:00 (26.94 days)
- **Trades:** 266,027 (buys 239,470 / sells 26,557)
- **Markets touched:** 29,195
- **Closed positions:** 49,842

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$390,114.77 |
| Core cashflow (ex-rebates) | -$390,557.08 |
| Closed-positions realized sum | -$611,424.96 |
| Win rate (closed) | 28.34% (12022W / 30400L) |
| Profit factor | 0.6293 |
| Gross wins / losses | $1,037,938.05 / -$1,649,363.01 |
| Equity max drawdown | -$351,914.65 |
| Polymarket leaderboard (ALL) | $635,298.67 PnL · vol $7,379,689.24 · rank 323 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=-390114.7655 ref=635298.6729157614 diff=-1025413.4384
- **DRIFT** `polydata` realized_pnl: ours=-390114.7655 ref=497985.09 diff=-888099.8555
- **DRIFT** `polydata` n_trades: ours=266027 ref=95230 diff=170797
- **DRIFT** `polydata` win_rate: ours=0.2834 ref=0.7458 diff=-0.4624
- **DRIFT** `internal` cashflow_vs_closed: ours=-390114.7655 ref=-611424.9602 diff=221310.1947

## What kind of trader is this?

**Classification:** `hybrid_mm_directional` (score 35/100)

- Trades both outcomes in 37% of markets (inventory/MM signature)
- High-frequency cadence (median gap 12s)

Supporting rates — both-sides markets: 0.3678, fast round-trips: 0.0196, spread-capture rate: 0.0896.

## Exact edge thesis

Mysaria looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $457,055.21 across 1194 closed legs
- **politics**: $113,895.74 across 4707 closed legs
- **crypto**: -$16,376.75 across 635 closed legs
- **sports_match**: -$93,425.83 across 2357 closed legs
- **other**: -$1,072,573.33 across 40949 closed legs

## Timing

- Peak UTC hours: 23, 16, 15, 6, 22
- Peak weekdays (0=Mon): [0, 3, 4]
- Median inter-trade gap: 12s

## Sizing

- Median ticket $7.79, mean $19.34, p90 $41.50, max $991.00
- Share size median 10.0, mean 27.7726

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Will there be no change in Fed interest rates after the September 2026 meeting?
- Entries ≈ **0.342** · Exits ≈ **0.637** · Spread ≈ **0.295**
- Fills: 165 buys / 8 sells · hold 22d 12h · both-sides=True · realized $15,433.89

### Will Luiz Inácio Lula da Silva win the 2026 Brazilian presidential election?
- Entries ≈ **0.366** · Exits ≈ **0.610** · Spread ≈ **0.244**
- Fills: 379 buys / 2 sells · hold 19d 23h · both-sides=True · realized $9,349.81

### Will Elon Musk post 180-199 tweets from August 21 to August 28, 2026?
- Entries ≈ **0.361** · Exits ≈ **0.426** · Spread ≈ **0.065**
- Fills: 108 buys / 22 sells · hold 10d 5h · both-sides=True · realized $4,145.05

### Will Mike Mazzei win the 2026 Oklahoma Governor Republican primary election?
- Entries ≈ **0.158** · Exits ≈ **0.660** · Spread ≈ **0.502**
- Fills: 22 buys / 3 sells · hold 7d 14h · both-sides=True · realized $3,805.27

### Will Enzo Fernandez join Manchester City?
- Entries ≈ **0.354** · Exits ≈ **0.507** · Spread ≈ **0.154**
- Fills: 93 buys / 10 sells · hold 24d 19h · both-sides=True · realized $2,972.83

### Will Harry Kane win the 2026 Ballon d'Or?
- Entries ≈ **0.371** · Exits ≈ **0.627** · Spread ≈ **0.256**
- Fills: 120 buys / 3 sells · hold 19d 11h · both-sides=True · realized $2,231.88

### Will NVIDIA be the largest company in the world by market cap on September 30?
- Entries ≈ **0.103** · Exits ≈ **0.869** · Spread ≈ **0.765**
- Fills: 40 buys / 5 sells · hold 26d 17h · both-sides=True · realized $2,212.73

### Will Elon Musk post 160-179 tweets from August 25 to September 1, 2026?
- Entries ≈ **0.360** · Exits ≈ **0.527** · Spread ≈ **0.166**
- Fills: 88 buys / 21 sells · hold 10d 1h · both-sides=True · realized $2,206.75

### Will the highest temperature in New York City be between 78-79°F on August 25?
- Entries ≈ **0.380** · Exits ≈ **0.963** · Spread ≈ **0.584**
- Fills: 58 buys / 29 sells · hold 1d 20h · both-sides=True · realized $1,890.36

### Will United Russia (ER) gain the most seats in the next Russian parliamentary election?
- Entries ≈ **0.320** · Exits ≈ **0.702** · Spread ≈ **0.382**
- Fills: 82 buys / 4 sells · hold 24d 20h · both-sides=True · realized $1,866.36

## Top closed winners / losers

**Winners**
- Will there be no change in Fed interest rates after the September 2026 meeting?: $15,433.89 · bought $14,595.53 · sold $371.46 · hold 22d 12h
- Will Luiz Inácio Lula da Silva win the 2026 Brazilian presidential election?: $9,349.81 · bought $15,640.01 · sold $114.85 · hold 19d 23h
- Will Melissa Agard win the 2026 Wisconsin Governor Democratic primary election?: $6,371.80 · bought $0.00 · sold $0.73 · hold 0s
- Will Mandela Barnes win the 2026 Wisconsin Governor Democratic primary election?: $6,323.56 · bought $0.00 · sold $0.65 · hold 0s
- Will Brett Hulsey win the 2026 Wisconsin Governor Democratic primary election?: $6,182.84 · bought $0.00 · sold $0.93 · hold 0s
- Will Joel Brennan win the 2026 Wisconsin Governor Democratic primary election?: $6,171.30 · bought $0.00 · sold $0.61 · hold 0s
- Will Chris Larson win the 2026 Wisconsin Governor Democratic primary election?: $6,153.91 · bought $0.00 · sold $0.93 · hold 0s
- Will Missy Hughes win the 2026 Wisconsin Governor Democratic primary election?: $6,127.47 · bought $0.00 · sold $0.93 · hold 0s
- Will Tim Jacobson win the 2026 Wisconsin Governor Democratic primary election?: $6,126.22 · bought $0.00 · sold $0.93 · hold 0s
- Will Kelda Roys win the 2026 Wisconsin Governor Democratic primary election?: $6,012.09 · bought $0.00 · sold $1.00 · hold 4h 0m

**Losers**
- Will Augusto Cury win the 2026 Brazilian presidential election?: -$14,026.86 · bought $15,476.38 · sold $377.95
- Will Pablo Marçal win the 2026 Brazilian presidential election?: -$9,574.27 · bought $19,691.41 · sold $127.29
- Will the Fed decrease interest rates by 50+ bps after the September 2026 meeting?: -$8,319.64 · bought $41,889.75 · sold $2.43
- Will the Fed decrease interest rates by 25 bps after the September 2026 meeting?: -$7,267.07 · bought $41,969.60 · sold $8.29
- Will the Fed increase interest rates by 50+ bps after the September 2026 meeting?: -$6,766.96 · bought $42,436.81 · sold $2.36
- Will Camilo Santana win the 2026 Brazilian presidential election?: -$5,933.52 · bought $13,389.23 · sold $29.51
- Will Elon Musk post 240+ tweets from August 22 to August 24, 2026?: -$4,963.46 · bought $5.00 · sold $0.25
- Will Hull City win the 2026-27 English Premier League (EPL) Championship?: -$3,944.81 · bought $2,571.23 · sold $2.87
- Will Fulham win the 2026-27 English Premier League (EPL) Championship?: -$3,944.80 · bought $549.15 · sold $4.90
- Will Ipswich Town win the 2026-27 English Premier League (EPL) Championship?: -$3,944.80 · bought $549.15 · sold $4.90

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $394,979.02
- Sells: $4,202.42
- Redeems: $219.52
- Maker rebates: $121.93
- Taker rebates: $33.93

_Generated 2026-09-01T14:46:19.991525+00:00_
