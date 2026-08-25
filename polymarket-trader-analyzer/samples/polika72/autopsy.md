# Deep Trader Autopsy — polika72

- Wallet: `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`
- Identity: **`one_sided_informed_scalper`**
- Primary focus: **sports_totals**
- Span: 2026-03-12T17:59:13+00:00 → 2026-08-25T15:48:07+00:00 (165.91 days)
- Generated: 2026-08-25T16:46:52.152804+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $58,204.98 | trades=19,978 |
| Our core cashflow | $57,699.08 | buys=9,077 sells=10,901 |
| Our closed-legs sum | $61,909.37 | closed=5,035 WR=80.1% |
| Polymarket leaderboard ALL | $57,338.72 | vol=$1,049,905.19 rank=3244 |
| PolyData | $52,640.69 | trades=24078 WR=0.6567 |

- **MATCH** `polymarket_leaderboard_ALL` pnl: ours=57699.0816 ref=57338.716846567695 diff=360.3648
- **DRIFT** `polydata` realized_pnl: ours=57699.0816 ref=52640.69 diff=5058.3916
- **DRIFT** `polydata` n_trades: ours=19978 ref=24078 diff=-4100
- **DRIFT** `polydata` win_rate: ours=0.8008 ref=0.6567 diff=0.1441
- **MATCH** `internal` cashflow_vs_closed: ours=58204.9839 ref=61909.3681 diff=-3704.3842

## B. Core identity

- Scanner MM label: `likely_market_maker` (score 65)
- Fast round-trips (<2h) in 100% of two-sided markets
- Avg sell > avg buy in 84% of markets (spread capture)
- High-frequency cadence (median gap 45s)
- Heavy concentration in Over/Under sports totals (sports MM niche)
- Both-sides inventory: 37 markets (0.68%)
- Clip USDC median/p90/max: $10.57 / $52.52 / $1,479.63
- Sport categories: `{'sports_totals': 40877.63, 'sports_match': 14704.2, 'other': 6180.6, 'crypto': 146.94}`
- Slug tokens: [('ucl', 136), ('lal', 122), ('bun', 91), ('ten', 63), ('mma', 29)]

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 38.38% | 61.62% | 3,899 | 5,178 |
| Exit | 49.09% | 50.91% | 6,935 | 3,966 |

- `enter_taker_exit_maker`: 1723
- `enter_taker_exit_taker`: 1468
- `enter_maker_exit_maker`: 1062
- `enter_maker_exit_taker`: 680

### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 0-20¢ | 909 | 71.0% | $4,517.97 | $4.97 |
| 20-40¢ | 1285 | 77.2% | $15,230.70 | $11.85 |
| 40-60¢ | 1494 | 82.1% | $22,820.93 | $15.28 |
| 60-80¢ | 1463 | 86.4% | $17,974.32 | $12.29 |
| 80-100¢ | 271 | 78.4% | $1,365.45 | $5.04 |

## C. Equity & risk

- Final cashflow equity: $58,204.98
- Max drawdown: -$601.18 (-1.3% of peak)
- Longest drawdown: 0 days
- Daily Sharpe (ann.): 14.692
- Profit factor: 3.2979
- Top 10 winners: $6,051.67 (6.82% of win PnL)
- Top 10 losers: -$4,429.46 (16.48% of loss PnL)
- Max inventory shares: 6000.0

### Top winners
- $841.93 · 1h12m · FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
- $670.10 · 28m48s · FC Bayern München vs. Real Madrid CF: O/U 4.5
- $645.59 · 6m02s · FC Bayern München vs. Real Madrid CF: O/U 3.5
- $640.86 · 1h18m · FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
- $629.26 · 2m18s · Will Club Atlético de Madrid win on 2026-08-23?
- $564.47 · 13m06s · Will Real Madrid CF win on 2026-03-17?
- $544.83 · 1h10m · FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
- $508.06 · 58s · Paris Saint-Germain vs. Aston Villa: O/U 3.5
- $504.28 · 44s · Will Paris Saint-Germain FC win on 2026-04-14?
- $502.30 · 9m30s · Netherlands vs. Japan: O/U 4.5

### Top losers
- -$384.52 · 23m30s · Cádiz CF vs. Córdoba CF: O/U 4.5
- -$388.13 · 2m16s · Real Madrid CF vs. Deportivo Alavés: O/U 3.5
- -$414.38 · 8m10s · UD Las Palmas vs. SD Huesca: O/U 3.5
- -$416.80 · 1m14s · Sporting CP vs. Arsenal FC: O/U 2.5
- -$427.77 · 8m10s · RC Strasbourg Alsace vs. OGC Nice: O/U 4.5
- -$427.80 · 46s · Will Paris Saint-Germain FC win on 2026-04-22?
- -$471.20 · 1h16m · Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5
- -$474.32 · 3m46s · Panama vs. England: Both Teams to Score
- -$508.72 · 1h27m · Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5
- -$515.82 · 6m46s · RC Strasbourg Alsace vs. OGC Nice: O/U 3.5

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 717 | 74.9% | $2,351.19 | $3.28 |
| 30s-2m | 3234 | 86.7% | $42,763.37 | $13.22 |
| 2-5m | 731 | 64.5% | $2,609.46 | $3.57 |
| 5-15m | 291 | 59.5% | $442.89 | $1.52 |
| 15m+ | 449 | 75.4% | $13,742.46 | $30.61 |

- After early adverse (>2¢ vs entry within 2m): n=400, avg PnL -$12.86, median first-sell 56s, median hold 1m23s
- After favorable first sell (+2¢): n=4058, avg PnL $18.13, median MFE capture 1.0
- Campaigns (re-entry after flat): 317 (5.85%), avg entries 2.09, PnL $9,675.13, avg $30.52, WR 82.0%
- Single-entry: n=5105, PnL $52,234.23, avg $10.23
- Flatten-before-resolution flag rate: 0.9035; hold-to-resolution style n=489; redeems $2,147.26; merges $0.00
- Avg-down while MTM-red on losers: 15/993 (1.51%); Δ if skipped on those $62.53; global never-red-buy Δ -$58.20

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Over/Under | 3543 | 77.9% | $40,676.84 | $11.48 |
| Yes/No moneyline | 1743 | 84.3% | $21,062.80 | $12.08 |
| Other | 136 | 87.2% | $169.73 | $1.25 |

## E. Edge diagnosis

- Time to MFE (winners): median 1m04s, p25 44s, p75 1m39s, p90 6m29s
- Big MFE ≥10¢: n=3256; within 30s=222; within 60s=1624 (49.88% of big moves)

**Edge thesis:** Joins short-horizon informed / impulse flow — taker-heavy entries, exits into strength. Money from markout seconds–minutes after entry, not two-sided spreads.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | one_sided_informed_scalper | one_sided_informed_scalper |
| trades | 19978 | 19978 |
| cashflow_pnl | 58204.9839 | 58204.9839 |
| win_rate | 0.8008 | 0.8008 |
| entry_taker_pct | 61.62 | 61.6 |
| both_sides_rate | 0.0068 | 0.008 |
| median_clip | 10.567 | 11.29 |
| campaign_pct | 5.85 | 5.85 |
| max_dd | -601.1817 | -2214.9721 |
| time_to_mfe_med | 64 | 64 |

### Steal / avoid

- **Steal:** impulse entry timing / live-event reaction if transferable.
- **Avoid:** copying one-sided Over bias blindly onto Kalshi without feed parity.

## G. Kalshi two-sided informed MM relevance

Partial relevance: the *informed impulse* leg maps to an aggressive/taker overlay on Kalshi, but this is NOT the core two-sided MM. Use as a signal/overlay module, not the whole bot.
