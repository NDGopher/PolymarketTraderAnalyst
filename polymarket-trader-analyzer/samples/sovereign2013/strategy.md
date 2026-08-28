# Strategy Dossier: sovereign2013

- **Wallet:** `0xee613b3fc183ee44f9da9c05f53e2da107e3debf`
- **History span:** 2025-08-07T14:54:45+00:00 → 2025-11-30T12:27:58+00:00 (114.9 days)
- **Trades:** 119,316 (buys 119,305 / sells 11)
- **Markets touched:** 8,938
- **Closed positions:** 71,299

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$4,392,612.28 |
| Core cashflow (ex-rebates) | -$4,392,657.34 |
| Closed-positions realized sum | $2,198,738.71 |
| Win rate (closed) | 51.15% (36470W / 34826L) |
| Profit factor | 1.0414 |
| Gross wins / losses | $55,310,486.44 / -$53,111,747.73 |
| Equity max drawdown | -$1,069,973.31 |
| Polymarket leaderboard (ALL) | $3,588,720.22 PnL · vol $402,071,822.94 · rank 38 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=2198738.7126 ref=3588720.2180176293 diff=-1389981.5054
- **DRIFT** `polydata` realized_pnl: ours=2198738.7126 ref=3588720.22 diff=-1389981.5074
- **DRIFT** `polydata` n_trades: ours=119316 ref=1047862 diff=-928546
- **MATCH** `polydata` win_rate: ours=0.5115 ref=0.5174 diff=-0.0059
- **DRIFT** `internal` cashflow_vs_closed: ours=-4392612.2757 ref=2198738.7126 diff=-6591350.9883

## What kind of trader is this?

**Classification:** `likely_market_maker` (score 65/100)

- Trades both outcomes in 62% of markets (inventory/MM signature)
- Fast round-trips (<2h) in 56% of two-sided markets
- High-frequency cadence (median gap 16s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.6171, fast round-trips: 0.5556, spread-capture rate: 0.3333.

## Exact edge thesis

sovereign2013 primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $1,451,954.61 across 39774 closed legs
- **sports_totals**: $722,608.02 across 31519 closed legs
- **other**: $24,172.77 across 1 closed legs
- **crypto**: $3.30 across 5 closed legs

## Timing

- Peak UTC hours: 15, 16, 14, 23, 17
- Peak weekdays (0=Mon): [5, 2, 4]
- Median inter-trade gap: 16s

## Sizing

- Median ticket $19.64, mean $254.96, p90 $655.00, max $7,212.70
- Share size median 42.9375, mean 515.6948

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- Spread: Utah State Aggies (-10.5): $113,953.16 · bought $77,395.51 · sold $0.00 · hold 11h 17m
- Tulane vs. Temple: $85,597.66 · bought $95,327.85 · sold $0.00 · hold 9h 35m
- Heat vs. Lakers: O/U 232.5: $71,389.74 · bought $65,817.70 · sold $0.00 · hold 5h 22m
- Nuggets vs. Trail Blazers: $64,009.54 · bought $35,456.91 · sold $0.00 · hold 20h 46m
- Spread: Broncos (-8.5): $54,499.31 · bought $82,727.50 · sold $0.00 · hold 16h 44m
- Spread: Knicks (-8.5): $45,994.41 · bought $43,423.12 · sold $0.00 · hold 6h 37m
- Buccaneers vs. Rams: O/U 49.5: $45,108.24 · bought $39,814.99 · sold $0.00 · hold 18h 58m
- Texas State vs. Southern Miss: $43,701.95 · bought $28,673.72 · sold $0.00 · hold 8h 22m
- Hawks vs. Cavaliers: O/U 231.5: $38,261.32 · bought $39,404.98 · sold $0.00 · hold 11h 3m
- Spread: Central Michigan (-9.5): $37,996.97 · bought $32,551.07 · sold $0.00 · hold 17h 23m

**Losers**
- Spread: Virginia Cavaliers (-3.5): -$98,306.11 · bought $112,210.33 · sold $0.00
- Spread: Thunder (-8.5): -$70,992.09 · bought $100,087.15 · sold $0.00
- Spread: Florida State (-6.5): -$70,979.38 · bought $126,011.56 · sold $0.00
- Spread: Rockets (-7.5): -$55,520.54 · bought $61,039.67 · sold $0.00
- Bills vs. Texans: O/U 44.5: -$55,214.96 · bought $59,207.38 · sold $0.00
- Army vs. Air Force: -$51,257.30 · bought $51,257.99 · sold $0.00
- Chiefs vs. Bills: O/U 50.5: -$37,034.38 · bought $39,260.72 · sold $0.00
- Missouri vs. Oklahoma: -$36,894.01 · bought $73,553.95 · sold $0.00
- Nets vs. Celtics: -$36,742.02 · bought $48,757.89 · sold $0.00
- UAB Blazers vs. Rice: -$30,622.12 · bought $52,247.43 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$19.64) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $30,420,194.16
- Sells: $124.31
- Redeems: $26,027,412.51
- Maker rebates: $0.00
- Taker rebates: $0.00

_Generated 2026-08-28T15:08:28.306606+00:00_
