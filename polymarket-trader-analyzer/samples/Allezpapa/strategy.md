# Strategy Dossier: Allezpapa

- **Wallet:** `0xe549581668a5751c1972d3ad2d1991d900bd2d54`
- **History span:** 2026-06-09T21:04:30+00:00 → 2026-07-19T18:40:30+00:00 (39.9 days)
- **Trades:** 57,355 (buys 57,355 / sells 0)
- **Markets touched:** 156
- **Closed positions:** 83

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $4,227,794.05 |
| Core cashflow (ex-rebates) | $4,141,946.90 |
| Closed-positions realized sum | $11,663,864.02 |
| Win rate (closed) | 98.80% (82W / 1L) |
| Profit factor | 51.2755 |
| Gross wins / losses | $11,895,862.92 / -$231,998.90 |
| Equity max drawdown | -$2,067,001.02 |
| Polymarket leaderboard (ALL) | $4,280,722.83 PnL · vol $54,987,532.65 · rank 29 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=4227794.0457 ref=4280722.833949986 diff=-52928.7882
- **MATCH** `polydata` realized_pnl: ours=4227794.0457 ref=4280722.83 diff=-52928.7843
- **DRIFT** `polydata` n_trades: ours=57355 ref=42825 diff=14530
- **DRIFT** `polydata` win_rate: ours=0.988 ref=0.5217 diff=0.4663
- **DRIFT** `internal` cashflow_vs_closed: ours=4227794.0457 ref=11663864.0191 diff=-7436069.9734

## What kind of trader is this?

**Classification:** `directional_or_unclear` (score 10/100)

- High-frequency cadence (median gap 13s)

Supporting rates — both-sides markets: 0.0064, fast round-trips: 0.0, spread-capture rate: 0.0.

## Exact edge thesis

Allezpapa looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **other**: $4,859,348.44 across 21 closed legs
- **sports_match**: $4,162,172.38 across 24 closed legs
- **sports_totals**: $2,103,666.27 across 35 closed legs
- **crypto**: $538,676.93 across 3 closed legs

## Timing

- Peak UTC hours: 18, 4, 5, 3, 23
- Peak weekdays (0=Mon): [6, 1, 3]
- Median inter-trade gap: 13s

## Sizing

- Median ticket $8.51, mean $322.93, p90 $132.56, max $260,000.00
- Share size median 22.79, mean 958.7179

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- Will Spain win the 2026 FIFA World Cup?: $2,253,608.68 · bought $420,154.19 · sold $0.00 · hold 31d 23h
- Will Norway vs. England end in a draw?: $738,506.19 · bought $256,744.79 · sold $0.00 · hold 4d 1h
- Will Spain vs. Argentina end in a draw?: $443,507.57 · bought $209,506.71 · sold $0.00 · hold 1h 11m
- Will Ecuador win on 2026-06-25?: $410,396.79 · bought $110,563.01 · sold $0.00 · hold 15h 49m
- Norway vs. England: Team to Advance: $279,483.60 · bought $522,997.75 · sold $0.00 · hold 1d 19h
- France vs. Morocco: O/U 2.5: $263,503.08 · bought $285,999.11 · sold $0.00 · hold 1d 4h
- Will Türkiye win on 2026-06-25?: $257,732.24 · bought $86,559.83 · sold $0.00 · hold 0s
- Will Portugal vs. DR Congo end in a draw?: $247,750.80 · bought $51,000.00 · sold $0.00 · hold 1s
- Spread: Bosnia and Herzegovina (-1.5): $244,958.40 · bought $203,000.00 · sold $0.00 · hold 3h 0m
- Will Switzerland vs. Colombia end in a draw?: $242,108.46 · bought $108,981.70 · sold $0.00 · hold 2d 22h

**Losers**
- Uruguay vs. Cabo Verde: O/U 2.5: -$84,067.62 · bought $512,863.60 · sold $0.00

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $18,646,768.05
- Sells: $0.00
- Redeems: $22,788,714.95
- Maker rebates: $40,082.56
- Taker rebates: $42,250.62

_Generated 2026-09-01T14:51:55.605168+00:00_
