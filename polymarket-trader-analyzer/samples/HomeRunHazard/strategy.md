# Strategy Dossier: HomeRunHazard

- **Wallet:** `0x5268527977f700f9bf9b6d5cd843859e4e70135d`
- **History span:** 2026-04-24T14:39:18+00:00 → 2026-05-07T12:35:18+00:00 (12.91 days)
- **Trades:** 26,170 (buys 26,170 / sells 0)
- **Markets touched:** 1,097
- **Closed positions:** 42,624

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$2,419,854.53 |
| Core cashflow (ex-rebates) | -$2,438,366.83 |
| Closed-positions realized sum | $2,231,236.73 |
| Win rate (closed) | 54.02% (23021W / 19597L) |
| Profit factor | 1.0434 |
| Gross wins / losses | $53,634,448.68 / -$51,403,211.95 |
| Equity max drawdown | -$1,510,984.52 |
| Polymarket leaderboard (ALL) | $2,248,711.81 PnL · vol $264,797,406.19 · rank 67 |

## Source validation

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=2231236.7279 ref=2248711.8139243205 diff=-17475.086
- **MATCH** `polydata` realized_pnl: ours=2231236.7279 ref=2250300.68 diff=-19063.9521
- **DRIFT** `polydata` n_trades: ours=26170 ref=268747 diff=-242577
- **MATCH** `polydata` win_rate: ours=0.5402 ref=0.5418 diff=-0.0016
- **DRIFT** `internal` cashflow_vs_closed: ours=-2419854.5251 ref=2231236.7279 diff=-4651091.253

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 45/100)

- Trades both outcomes in 69% of markets (inventory/MM signature)
- High-frequency cadence (median gap 10s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.6864, fast round-trips: 0.0, spread-capture rate: 0.0.

## Exact edge thesis

HomeRunHazard primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_totals**: $1,509,899.51 across 18437 closed legs
- **sports_match**: $721,337.22 across 24187 closed legs

## Timing

- Peak UTC hours: 0, 23, 10, 11, 14
- Peak weekdays (0=Mon): [1, 2, 5]
- Median inter-trade gap: 10s

## Sizing

- Median ticket $8.17, mean $195.75, p90 $488.54, max $9,369.92
- Share size median 20.0, mean 401.4378

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- Madrid Open: Anastasia Potapova vs Elena Rybakina: $30,407.98 · bought $14,458.18 · sold $0.00 · hold 1h 50m
- Madrid Open: Alexander Bublik vs Stefanos Tsitsipas: $27,567.49 · bought $60,871.51 · sold $0.00 · hold 1h 8m
- Madrid Open: Thiago Agustin Tirante vs Tommy Paul: $24,774.18 · bought $65,721.63 · sold $0.00 · hold 1h 36m
- 76ers vs. Knicks: $21,400.73 · bought $13,351.34 · sold $0.00 · hold 1h 36m
- Madrid Open: Jessica Pegula vs Marta Kostyuk: $18,618.95 · bought $41,704.14 · sold $0.00 · hold 1h 1m
- Athletics vs. Philadelphia Phillies: O/U 8.5: $18,085.18 · bought $25,587.97 · sold $0.00 · hold 10h 49m
- Milwaukee Brewers vs. St. Louis Cardinals: O/U 8.5: $17,054.02 · bought $20,720.59 · sold $0.00 · hold 2h 9m
- Cincinnati Reds vs. Chicago Cubs: O/U 8.5: $16,281.38 · bought $1,424.67 · sold $0.00 · hold 2m 37s
- Athletics vs. Philadelphia Phillies: O/U 9.5: $15,666.68 · bought $16,713.55 · sold $0.00 · hold 5h 21m
- Toronto Blue Jays vs. Tampa Bay Rays: $12,770.80 · bought $5,049.06 · sold $0.00 · hold 1h 31m

**Losers**
- 76ers vs. Knicks: O/U 211.5: -$91,965.56 · bought $5,515.34 · sold $0.00
- Baltimore Orioles vs. New York Yankees: -$70,897.12 · bought $14,563.59 · sold $0.00
- Madrid Open: Stefanos Tsitsipas vs Casper Ruud: -$69,098.34 · bought $82,297.10 · sold $0.00
- 76ers vs. Knicks: O/U 212.5: -$59,416.63 · bought $6,154.03 · sold $0.00
- New York Mets vs. Colorado Rockies: O/U 10.5: -$57,746.38 · bought $8,714.96 · sold $0.00
- Madrid Open: Aryna Sabalenka vs Naomi Osaka: -$54,557.39 · bought $65,700.58 · sold $0.00
- Internazionali BNL d'Italia: Federico Cina vs Alexander Blockx: -$23,006.33 · bought $27,251.33 · sold $0.00
- Madrid Open: Daniil Medvedev vs Fabian Marozsan: -$21,487.41 · bought $10,570.16 · sold $0.00
- Madrid Open: Terence Atmane vs Alexander Zverev: -$19,436.44 · bought $14,107.74 · sold $0.00
- Colorado Rockies vs. New York Mets: -$16,346.11 · bought $25,739.19 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$8.17) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $5,131,498.83
- Sells: $0.00
- Redeems: $2,693,132.00
- Maker rebates: $8,822.87
- Taker rebates: $0.00

_Generated 2026-08-25T16:46:54.879231+00:00_
