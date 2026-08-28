# Strategy Dossier: kch123

- **Wallet:** `0x6a72f61820b26b1fe4d956e17b6dc2a1ea3033ee`
- **History span:** 2025-06-25T19:14:46+00:00 → 2026-01-27T20:53:31+00:00 (216.07 days)
- **Trades:** 106,103 (buys 106,005 / sells 98)
- **Markets touched:** 1,755
- **Closed positions:** 4,033

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $3,628,200.69 |
| Core cashflow (ex-rebates) | $3,628,142.05 |
| Closed-positions realized sum | $13,390,318.52 |
| Win rate (closed) | 52.67% (2122W / 1907L) |
| Profit factor | 1.2366 |
| Gross wins / losses | $69,995,176.54 / -$56,604,858.01 |
| Equity max drawdown | -$2,929,265.95 |
| Polymarket leaderboard (ALL) | $11,386,690.88 PnL · vol $298,637,138.56 · rank 5 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=13390318.5232 ref=11386690.875513867 diff=2003627.6477
- **DRIFT** `polydata` realized_pnl: ours=13390318.5232 ref=11386690.88 diff=2003627.6432
- **DRIFT** `polydata` n_trades: ours=106103 ref=171115 diff=-65012
- **MATCH** `polydata` win_rate: ours=0.5267 ref=0.5467 diff=-0.02
- **DRIFT** `internal` cashflow_vs_closed: ours=3628200.6939 ref=13390318.5232 diff=-9762117.8293

## What kind of trader is this?

**Classification:** `strong_market_maker` (score 70/100)

- Trades both outcomes in 57% of markets (inventory/MM signature)
- Avg sell > avg buy in 91% of markets (spread capture)
- High-frequency cadence (median gap 12s)
- Heavy concentration in Over/Under sports totals (sports MM niche)

Supporting rates — both-sides markets: 0.5664, fast round-trips: 0.0625, spread-capture rate: 0.9062.

## Exact edge thesis

kch123 primarily monetizes **liquidity / short-horizon mean reversion on sports markets**, not long-shot directional political bets. The tape shows repeated buy-then-sell with average exit price above average entry — the classic scalper / spread fingerprint.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $11,368,340.52 across 3569 closed legs
- **sports_totals**: $1,718,753.74 across 447 closed legs
- **other**: $365,327.45 across 16 closed legs
- **politics**: -$62,103.19 across 1 closed legs

## Timing

- Peak UTC hours: 1, 2, 0, 19, 3
- Peak weekdays (0=Mon): [6, 1, 4]
- Median inter-trade gap: 12s

## Sizing

- Median ticket $15.09, mean $1,009.05, p90 $1,078.00, max $729,628.77
- Share size median 30.0, mean 1988.3305

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Will Aston Villa FC win on 2026-01-18?
- Entries ≈ **0.487** · Exits ≈ **0.999** · Spread ≈ **0.512**
- Fills: 7 buys / 38 sells · hold 4h 36m · both-sides=True · realized $164,044.15

## Top closed winners / losers

**Winners**
- Will Villarreal CF win on 2026-01-20?: $1,095,000.00 · bought $405,000.00 · sold $0.00 · hold 0s
- Spread: Seahawks (-4.5): $986,792.15 · bought $262,924.50 · sold $0.00 · hold 3h 33m
- Will Paris Saint-Germain FC win on 2026-01-20?: $580,000.00 · bought $420,000.00 · sold $0.00 · hold 22m 18s
- Stars vs. Oilers: $481,040.39 · bought $425,738.07 · sold $0.00 · hold 19h 11m
- Texas State vs. Southern Miss: $417,465.14 · bought $265,539.89 · sold $0.00 · hold 2h 8m
- Wild vs. Penguins: $375,013.18 · bought $336,415.83 · sold $0.00 · hold 11h 36m
- Will Stade Rennais FC 1901 win on 2026-01-18?: $371,663.82 · bought $228,000.00 · sold $335,844.73 · hold 6h 2m
- Capitals vs. Blackhawks: $357,255.70 · bought $472,223.85 · sold $0.00 · hold 2h 9m
- Clemson vs. Louisville: $345,950.63 · bought $271,818.35 · sold $0.00 · hold 38m 4s
- Flames vs. Sharks: $345,772.30 · bought $305,245.36 · sold $0.00 · hold 2h 25m

**Losers**
- Will FC Barcelona win on 2026-01-18?: -$713,998.80 · bought $714,000.00 · sold $0.00
- Blue Jays vs. Mariners: -$665,499.98 · bought $665,499.98 · sold $0.00
- Bills vs. Jaguars: -$549,430.45 · bought $567,079.59 · sold $0.00
- Chiefs vs. Cowboys: -$533,797.48 · bought $768,946.31 · sold $0.00
- Blue Jays vs. Dodgers: -$519,406.04 · bought $519,409.92 · sold $0.00
- Will Olympiakós SFP win on 2026-01-20?: -$510,999.30 · bought $511,000.00 · sold $0.00
- Spread: Lions (-3.5): -$456,849.98 · bought $456,850.68 · sold $0.00
- Patriots vs. Ravens: -$430,358.49 · bought $482,210.29 · sold $0.00
- Ravens vs. Packers: -$430,296.71 · bought $452,587.52 · sold $0.00
- Alabama vs. Oklahoma: -$412,300.01 · bought $412,318.71 · sold $0.00

## Replication playbook (how to copy the edge)

1. **Universe:** Focus on liquid sports match + totals (O/U) markets with tight books.
2. **Role:** Quote or take both sides near mid; prioritize markets you can exit before resolution.
3. **Sizing:** Start near their median ticket (~$15.09) and scale only with inventory limits.
4. **Inventory:** Cap net Yes/No (or Over/Under) imbalance; flatten when mid moves through you.
5. **Hold time:** Target minutes–hours, not overnight directional risk, unless hedged via opposite outcome.
6. **Edge source:** Capture spread + mean reversion after flow, not oracle forecasting alpha.
7. **Ops:** Automate via CLOB maker orders; track maker rebates; kill-switch on drawdown.
8. **Do not blindly copy:** Their edge depends on latency, fee tier, and bankroll. Replicate *mechanics*, not wallet follows.

## Cashflow anatomy

- Buys: $105,598,225.60
- Sells: $1,464,956.80
- Redeems: $107,761,410.85
- Maker rebates: $0.00
- Taker rebates: $0.00

_Generated 2026-08-28T15:23:19.763924+00:00_
