# Strategy Dossier: WTSA

- **Wallet:** `0x04d5524a0a5af2eca6e39e03defc261d42fe66d8`
- **History span:** 2026-07-16T05:26:52+00:00 → 2026-07-29T16:12:36+00:00 (13.45 days)
- **Trades:** 17,934 (buys 17,934 / sells 0)
- **Markets touched:** 61
- **Closed positions:** 77

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $169,030.34 |
| Core cashflow (ex-rebates) | $160,372.00 |
| Closed-positions realized sum | $3,581,052.07 |
| Win rate (closed) | 98.70% (76W / 1L) |
| Profit factor | 122.4517 |
| Gross wins / losses | $3,610,537.47 / -$29,485.40 |
| Equity max drawdown | -$834,196.15 |
| Polymarket leaderboard (ALL) | $442,550.51 PnL · vol $14,224,366.92 · rank 471 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=169030.3377 ref=442550.5051193265 diff=-273520.1674
- **DRIFT** `polydata` realized_pnl: ours=169030.3377 ref=519173.09 diff=-350142.7523
- **DRIFT** `polydata` n_trades: ours=17934 ref=29173 diff=-11239
- **DRIFT** `polydata` win_rate: ours=0.987 ref=0.5402 diff=0.4468
- **DRIFT** `internal` cashflow_vs_closed: ours=169030.3377 ref=3581052.072 diff=-3412021.7343

## What kind of trader is this?

**Classification:** `directional_or_unclear` (score 10/100)

- High-frequency cadence (median gap 2s)

Supporting rates — both-sides markets: 0.0164, fast round-trips: 0.0, spread-capture rate: 0.0.

## Exact edge thesis

WTSA looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **other**: $2,275,393.46 across 39 closed legs
- **sports_match**: $693,866.15 across 16 closed legs
- **sports_totals**: $611,792.46 across 22 closed legs

## Timing

- Peak UTC hours: 21, 22, 18, 17, 23
- Peak weekdays (0=Mon): [1, 5, 2]
- Median inter-trade gap: 2s

## Sizing

- Median ticket $4.81, mean $132.86, p90 $93.19, max $45,780.00
- Share size median 10.0216, mean 275.3503

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- Will Inter Miami CF win on 2026-07-25?: $157,319.67 · bought $141,195.14 · sold $0.00 · hold 8m 27s
- CD Guadalajara vs. FC Juárez: O/U 2.5: $100,914.54 · bought $67,167.85 · sold $0.00 · hold 39m 7s
- Will Colorado Rapids SC win on 2026-07-22?: $94,438.28 · bought $96,250.24 · sold $0.00 · hold 4h 31m
- Club Tijuana vs. Club León FC: O/U 2.5: $85,702.47 · bought $74,974.03 · sold $0.00 · hold 45m 42s
- Will CR Flamengo win on 2026-07-29?: $85,019.66 · bought $29,902.40 · sold $0.00 · hold 3h 44m
- Will CF Montréal win on 2026-07-16?: $80,881.53 · bought $113,526.78 · sold $0.00 · hold 18h 2m
- Will Philadelphia Union win on 2026-07-25?: $71,898.79 · bought $85,435.62 · sold $0.00 · hold 5h 36m
- Will Fluminense FC win on 2026-07-17?: $55,072.39 · bought $52,638.14 · sold $0.00 · hold 51m 6s
- Will Athletic Club win on 2026-07-28?: $53,117.48 · bought $129,562.36 · sold $0.00 · hold 3h 58m
- Will CA San Lorenzo de Almagro win on 2026-07-28?: $49,617.10 · bought $49,618.59 · sold $0.00 · hold 1m 39s

**Losers**

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $2,409,822.91
- Sells: $0.00
- Redeems: $2,570,194.92
- Maker rebates: $4,798.42
- Taker rebates: $3,859.92

_Generated 2026-08-25T16:47:02.752373+00:00_
