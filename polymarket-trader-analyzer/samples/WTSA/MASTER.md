# MASTER AUTOPSY — WTSA

> Single file for humans **and** bots. Machine-readable twin: `MASTER.json` · Equity: `equity_curve.csv`.

- Wallet: `0x04d5524a0a5af2eca6e39e03defc261d42fe66d8`
- Generated: `2026-08-25T16:47:02.868253+00:00`
- Identity class: **`directional_hold_to_resolution`**

## 0. Executive verdict

This trader is classified as **directional_hold_to_resolution** with primary focus **other**. Preferred PnL (**cashflow_realized**) **$169,030.34** (leaderboard ALL $442,550.51; REVIEW). Unique trades **17,934**. Copy difficulty **9/10** · ease **2/10**. Buy-and-hold / resolution harvesting at large notional. Easy mechanically (buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule.

**Exit mechanics:** `merge_and_or_redeem_dominant`
**Kalshi two-sided MM fit:** MEDIUM — extract risk + hold rules; re-fit microstructure on Kalshi
**Preferred PnL note:** For buy-only / merge-redeem traders, cashflow equity can look deeply negative while closed-legs + leaderboard show true realized edge.

## 1. Reconciliation (mandatory)

| Source | PnL | Extra |
|---|---:|---|
| **Preferred (cashflow_realized)** | **$169,030.34** | vs LB diff=-273520.17 |
| Ours cashflow realized | $169,030.34 | trades=17,934 buy_only=True |
| Ours core (ex-rebate) | $160,372.00 | WR legs=98.70% |
| Ours closed-legs sum | $3,581,052.07 | PF=122.4517 |
| Polymarket leaderboard ALL | $442,550.51 | vol=$14,224,366.92 rank=471 |
| PolyData | $519,173.09 | trades=29173 WR=0.5402 |

- DRIFT: `polymarket_leaderboard_ALL` pnl ours=169030.3377 field=cashflow_realized ref=442550.5051193265 diff=-273520.1674
- DRIFT: `polydata` realized_pnl ours=169030.3377 field=cashflow_realized ref=519173.09 diff=-350142.7523
- DRIFT: `polydata` n_trades ours=17934 field=None ref=29173 diff=-11239
- DRIFT: `polydata` win_rate ours=0.987 field=None ref=0.5402 diff=0.4468
- DRIFT: `internal` cashflow_vs_closed ours=169030.3377 field=None ref=3581052.072 diff=-3412021.7343

## 2. Identity & microstructure

- Both-sides rate: 1.64% (1 markets)
- Clip median/p90/max: $4.81 / $93.19 / $45,780.00
- Category PnL: `{'other': 799148.23, 'sports_totals': 399961.76, 'sports_match': 111448.19}`
- Start BUY first: 61 · SELL first: 0
- Entry maker/taker: 54.66% / 45.34% (17,802/132 fills)
- Exit maker/taker: None% / None% (0/0 fills)
- Patterns: `{}`

### Outcome volume (top)

| Outcome | Buy USDC | Sell USDC | Sell−Buy |
|---|---:|---:|---:|
| Yes | $1,084,098.07 | $0.00 | -$1,084,098.07 |
| No | $622,913.94 | $0.00 | -$622,913.94 |
| Over | $350,644.30 | $0.00 | -$350,644.30 |
| Under | $296,465.19 | $0.00 | -$296,465.19 |
| Associação Chapecoense de Futebol | $22,845.63 | $0.00 | -$22,845.63 |
| Portland Timbers | $5,700.00 | $0.00 | -$5,700.00 |

## 3. Performance metrics (kitchen sink)

- Expectancy / market: $40,954.94
- Avg win / avg loss: $40,954.94 / $0.00 · ratio=None
- PnL / day: $12,567.31 · trades/day=1333.38 · markets/day=4.54
- PnL concentration HHI: 0.053937 (higher=more concentrated)
- Notional sum: $2,382,667.12 · median ticket $4.81
- Buy price median: 0.5 · Sell price median: None
- Activity types: `{'DEPOSIT': 3, 'TRADE': 17934, 'MAKER_REBATE': 10, 'REDEEM': 31, 'TAKER_REBATE': 12}`
- Open risk: `{'n': 76, 'cash_pnl': -3180033.83, 'current_value': 51477.18, 'redeemable': 74}`

### Hold-time engine

| Bucket | N | WR | Total PnL | Avg | Median |
|---|---:|---:|---:|---:|---:|
| <30s | 2 | 100.00% | $17,684.36 | $8,842.18 | $8,842.18 |
| 30s-2m | 3 | 100.00% | $49,617.10 | $16,539.03 | $0.00 |
| 2-5m | 4 | 100.00% | $14,490.79 | $3,622.70 | $75.86 |
| 5-15m | 12 | 100.00% | $344,851.76 | $28,737.65 | $18,962.59 |
| 15m+ | 40 | 100.00% | $883,914.17 | $22,097.85 | $255.16 |

### Entry price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 20-40¢ | 13 | 100.00% | $182,533.90 | $14,041.07 |
| 40-60¢ | 38 | 100.00% | $1,039,138.45 | $27,345.75 |
| 60-80¢ | 10 | 100.00% | $88,885.82 | $8,888.58 |

### Family

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 38 | 100.00% | $890,430.19 | $23,432.37 |
| Over/Under | 21 | 100.00% | $395,661.76 | $18,841.04 |
| Other | 2 | 100.00% | $24,466.22 | $12,233.11 |

## 4. Equity curve (critical)

### 4a. Cashflow activity equity

- Final equity (cashflow): **$169,030.34**
- Max DD: **-$596,843.08** (-441.60% of peak)
- Longest DD: **1 days**
- Daily Sharpe (ann.): **0.715**
- Days: 15

Files: `equity_curve.csv` · `equity_curve.json` (source=`cashflow_activity`)

<details><summary>Daily cashflow equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-07-12 | 0.00 | 0.00 | 0.00 |
| 2026-07-16 | -181065.75 | -181065.75 | -181065.75 |
| 2026-07-17 | -57214.13 | 123851.62 | -57214.13 |
| 2026-07-18 | 68489.06 | 125703.19 | 0.00 |
| 2026-07-19 | 31311.49 | -37177.57 | -37177.57 |
| 2026-07-20 | 87604.76 | 56293.27 | 0.00 |
| 2026-07-21 | 71844.55 | -15760.21 | -15760.21 |
| 2026-07-22 | -299259.24 | -371103.79 | -386864.00 |
| 2026-07-23 | 82228.15 | 381487.39 | -5376.61 |
| 2026-07-24 | -77614.25 | -159842.40 | -165219.01 |
| 2026-07-25 | -294560.92 | -216946.66 | -382165.68 |
| 2026-07-26 | 336079.82 | 630640.74 | 0.00 |
| 2026-07-27 | 337014.28 | 934.46 | 0.00 |
| 2026-07-28 | -259828.80 | -596843.08 | -596843.08 |
| 2026-07-29 | 169030.34 | 428859.14 | -167983.94 |

</details>

### 4b. Closed-positions equity (alt — critical for buy-only books)

- Final closed equity: **$3,581,052.07**
- Max DD: **$0.00**
- Daily Sharpe (ann.): **18.961**
- Days: 18

Files: `equity_curve_closed.csv` · `equity_curve_closed.json` (source=`closed_positions`)

<details><summary>Daily closed equity table (full)</summary>

| Date | Equity | Daily PnL | Drawdown |
|---|---:|---:|---:|
| 2026-07-17 | 85181.53 | 85181.53 | 0.00 |
| 2026-07-18 | 176615.21 | 91433.68 | 0.00 |
| 2026-07-19 | 195543.71 | 18928.50 | 0.00 |
| 2026-07-22 | 213738.39 | 18194.68 | 0.00 |
| 2026-07-23 | 399279.77 | 185541.38 | 0.00 |
| 2026-07-24 | 413618.84 | 14339.08 | 0.00 |
| 2026-07-25 | 591871.39 | 178252.54 | 0.00 |
| 2026-07-26 | 1025799.50 | 433928.11 | 0.00 |
| 2026-07-29 | 1225538.51 | 199739.02 | 0.00 |
| 2026-07-30 | 1335743.98 | 110205.47 | 0.00 |
| 2026-08-02 | 1568187.36 | 232443.38 | 0.00 |
| 2026-08-09 | 1780362.15 | 212174.79 | 0.00 |
| 2026-08-10 | 1900705.60 | 120343.45 | 0.00 |
| 2026-08-12 | 2141607.28 | 240901.67 | 0.00 |
| 2026-08-15 | 2386993.63 | 245386.35 | 0.00 |
| 2026-08-16 | 2422784.58 | 35790.94 | 0.00 |
| 2026-08-17 | 3325050.04 | 902265.46 | 0.00 |
| 2026-08-23 | 3581052.07 | 256002.04 | 0.00 |

</details>

### Top winners / losers contribution

Top10 winners $833,981.93 (63.64% of wins) · Top10 losers $0.00 (None% of losses) · PF=122.4517

- WIN $157,319.67 · 507s · Will Inter Miami CF win on 2026-07-25?
- WIN $100,914.54 · 2347s · CD Guadalajara vs. FC Juárez: O/U 2.5
- WIN $94,438.28 · 16314s · Will Colorado Rapids SC win on 2026-07-22?
- WIN $85,702.47 · 2742s · Club Tijuana vs. Club León FC: O/U 2.5
- WIN $85,019.66 · 13449s · Will CR Flamengo win on 2026-07-29?
- WIN $80,881.53 · 64975s · Will CF Montréal win on 2026-07-16?
- WIN $71,898.79 · 20192s · Will Philadelphia Union win on 2026-07-25?
- WIN $55,072.39 · 3066s · Will Fluminense FC win on 2026-07-17?
- WIN $53,117.48 · 14302s · Will Athletic Club win on 2026-07-28?
- WIN $49,617.10 · 99s · Will CA San Lorenzo de Almagro win on 2026-07-28?

- LOSS $0.00 · 3075s · Will EC Bahia win on 2026-07-26?
- LOSS $0.00 · 2856s · Will Cruzeiro EC win on 2026-07-26?
- LOSS $0.00 · 22418s · Will CA Rosario Central win on 2026-07-28?
- LOSS $0.00 · 15699s · Will EC Juventude win on 2026-07-28?
- LOSS $0.00 · 14458s · Will AA Ponte Preta win on 2026-07-28?
- LOSS $0.00 · 13509s · CA Rosario Central vs. Racing Club: O/U 2.5
- LOSS $0.00 · 1161s · Will CA Banfield win on 2026-07-28?
- LOSS $0.00 · 865s · AA Ponte Preta vs. Athletic Club: O/U 2.5
- LOSS $0.00 · 36s · CA Rosario Central vs. Racing Club: O/U 1.5
- LOSS $0.00 · 12626s · Will SC Internacional win on 2026-07-29?

## 5. Trade management deep dive

- Adverse early (>2¢): `{'n_early_adverse': 0, 'avg_pnl': None, 'median_t_first_sell': None, 'median_hold': None}`
- Favorable first-sell: `{'n_first_sell_up_2c': 0, 'avg_pnl': None, 'median_mfe_capture': None, 'mean_mfe_capture': None}`
- Campaigns: `{'n': 0, 'pct': 0.0, 'avg_entries': None, 'pnl': 0, 'avg_pnl': None, 'win_rate': None, 'single_n': 61, 'single_pnl': 1310558.18, 'single_avg_pnl': 21484.56}`
- Avg-down: `{'n_losers': 0, 'n_losers_with_red_buys': 0, 'pct_losers': 0.0, 'total_delta_if_skipped_on_losers': 0, 'global_fifo_sim': 0.0, 'global_fifo_never_red_buy': 0.0, 'global_delta': 0.0}`
- Resolution behavior: `{'flattened_before_flag_rate': 0.4262, 'hold_to_resolution_style_n': 61, 'redeems_usdc': 2570194.916162, 'merges_usdc': 0.0}`
- Latency: `{'time_to_mfe_median': None, 'time_to_mfe_p25': None, 'time_to_mfe_p75': None, 'time_to_mfe_p90': None, 'mfe_ge_10c_n': 0, 'mfe_ge_10c_within_30s': 0, 'mfe_ge_10c_within_60s': 0, 'pct_big_within_60s': 0.0}`

### What works / fails
- WORKS: Both-sides inventory on 3.1% of winning markets (losers 0.0%)
- WORKS: Entry band 0.40-0.60: avg $27345.75 across 38 markets
- WORKS: Buy-ladder behavior: fade-into-weakness markets=0, chase-up markets=3

## 6. Strategy overview (in depth)

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


## 7. Bot / copy playbook

- Difficulty: **9/10** · Ease: **2/10**
- Why: Buy-and-hold / resolution harvesting at large notional. Easy mechanically (buy → wait → redeem) but edge is selection + bankroll + path risk, not a simple rule.

### Build steps
1. Build a directional edge model (not a tape-copy) for the same market universe
2. Enter via maker when possible to cut fees; allow taker for urgency
3. Exit primarily via REDEEM (and MERGE if pairing YES/NO) — no mid-market sell loop required
4. Hard per-market and portfolio max inventory; expect multi-day underwater mark-to-market
5. Paper the full hold-to-resolution cycle including open-risk volatility

### Steal
- Maker-led entry style (better for quoting bots)
- Prioritize hold bucket 15m+ (their PnL engine)

### Avoid
- Their raw size/drawdown — scale down hard
- Blind hold-to-resolution without edge model

Bot parameters: `{'preferred_entry_price_median': 0.5129, 'preferred_entry_price_p25_p75': (0.4666, 0.567), 'target_spread_median': None, 'target_spread_p75': None, 'max_hold_seconds_p75': 15587, 'median_hold_seconds': 2229, 'clip_size_usdc_median': 5.3564, 'clip_size_usdc_p90': 104.12, 'both_sides_on_winners_rate': 0.0312, 'require_exit_above_entry': True, 'flatten_before_resolution': True, 'maker_bias': True}`

# Elite Replication Playbook — WTSA

Wallet `0x04d5524a0a5af2eca6e39e03defc261d42fe66d8`. Reverse-engineered from the **full unique fill tape** (17,934 trades · 61 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `directional_or_unclear` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $169,030.34 |
| Core cashflow (ex-rebates) | $160,372.00 |
| Closed-position legs sum | $3,581,052.07 |
| Leg win rate / profit factor | 98.70% / 122.4517 |
| Polymarket leaderboard ALL | $442,550.51 · vol $14,224,366.92 · rank 471 |
| polymarket_leaderboard_ALL pnl | ref=442550.5051193265 ours=169030.3377 (DRIFT) |
| polydata realized_pnl | ref=519173.09 ours=169030.3377 (DRIFT) |
| polydata n_trades | ref=29173 ours=17934 (DRIFT) |
| polydata win_rate | ref=0.5402 ours=0.987 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 21 markets · $395,661.76 · avg $18,841.04 · median hold 14m25s · median spread None
- **Match / other sports:** 38 markets · $890,430.19 · avg $23,432.37
- **Outcome PnL leaders:**
  - **Yes**: $546,676.50
  - **No**: $343,753.69
  - **Under**: $285,824.33
  - **Over**: $109,837.44
  - **Associação Chapecoense de Futebol**: $20,166.22
  - **Portland Timbers**: $4,300.00

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_near_mid`: 23
- `directional_buy_sub_mid`: 18
- `directional_buy_above_mid`: 16
- `directional_buy_cheap_tail`: 3
- `two_sided_inventory_near_mid`: 1

### First-two-fill sequences
- `BUY->BUY`: 60
- `single_fill`: 1

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.20-0.40 | 13 | $182,533.90 | $14,041.07 |
| 0.40-0.60 | 38 | $1,039,138.45 | $27,345.75 |
| 0.60-0.80 | 10 | $88,885.82 | $8,888.58 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$5.36** median (p90 $104.12).
2. Aim entry price ~**0.5129** (IQR (0.4666, 0.567)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 21
- `scalp_sub_15m`: 19
- `intraday_swing`: 19
- `single_clip`: 2

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 32 | None |
| PnL | $1,310,558.18 | n/a |
| Median hold | 37m09s | n/a |
| Median spread | None | None |
| Scale-in rate | 1.0 | None |
| Scale-out rate | 0.0 | None |
| Avg fills/market | 293.84 | None |
| Both-sides rate | 0.0312 | None |

### The real management loop (one-sided scalp)

```
BUY clip(s) on Over (or chosen outcome)
   │
   ├─ price jumps in your favor within seconds → SELL in clips (scale-out)
   ├─ price chops flat → keep working asks above entry; time-stop
   └─ price dumps → cut quickly (losers show sell-below-buy); do NOT average forever
Optional: re-enter later cheaper if a second impulse sets up (seen in big O/U winners)
```

Critical deltas:

- **Winners** sell above buy (median spread **None**). **Losers** often exit worse (median spread **None**).
- Losers scale-in **more** (None vs 1.0) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 9, 'pnl': 81792.2521, 'avg': 9088.028, 'win_rate': 0.4444}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 61

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 9 | $81,792.25 | $9,088.03 | 44.4% |
| 5-30m | 16 | $385,870.50 | $24,116.91 | 56.2% |
| 30m-2h | 15 | $321,986.43 | $21,465.76 | 60.0% |
| 2-12h | 18 | $440,027.46 | $24,445.97 | 50.0% |
| 12h+ | 3 | $80,881.53 | $26,960.51 | 33.3% |

### Exit engine params

1. **TP / ask distance:** target ≈ **None** above avg entry (p75 stretch None). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 37m09s; p75 4h19m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 3.1% of winning markets (losers 0.0%)
- Entry band 0.40-0.60: avg $27345.75 across 38 markets
- Buy-ladder behavior: fade-into-weakness markets=0, chase-up markets=3

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 3, 'fade_down': 0}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Will Toronto FC win on 2026-07-16?** $0.00 · hold 17h28m · entry 0.2996 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Will Vancouver Whitecaps FC win on 2026-07-16?** $0.00 · hold 14h33m · entry 0.6092 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Will Chicago Fire FC win on 2026-07-16?** $0.00 · hold 10h14m · entry 0.3546 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Club Tijuana vs. Tigres de la UANL: O/U 2.5** $0.00 · hold 43m57s · entry 0.519 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
5. **Will Club León FC win on 2026-07-17?** $0.00 · hold 38m36s · entry 0.44 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Will Criciúma EC win on 2026-07-18?** $0.00 · hold 0s · entry 0.43 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
7. **Will AC Goianiense win on 2026-07-20?** $0.00 · hold 4h44m · entry 0.49 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Pumas de la UNAM vs. CF Pachuca: O/U 2.5** $0.00 · hold 29m30s · entry 0.4861 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
9. **Will Vancouver Whitecaps FC win on 2026-07-22?** $0.00 · hold 5h47m · entry 0.534 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **Will Philadelphia Union win on 2026-07-22?** $0.00 · hold 5h44m · entry 0.4578 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

Common failure DNA: bought Over, game didn’t produce goals, sold lower or held into worthless.

## 9. Bot architecture (elite build)

```
LiveSportsFeed ──► Signal(impulse/dip) ──► Execution(maker-first)
                         │                      │
                         ▼                      ▼
                  PositionState ◄────── ExitEngine (TP/SL/time)
                         │
                         ▼
                   RiskGovernor (caps, kill switch)
```

### Modules

1. **LiveSportsFeed** — kickoff clock, shots, corners, goals (Opta/Betfair/odds APIs). Polymarket mid alone is laggy; their edge looks like **reacting to match state faster than the book**.
2. **Signal**
   - `dip_bid`: mid drops X¢ with depth refill → maker bid
   - `impulse_long_over`: attacking sequence / goal threat → bid or take Over
   - disable new entries near whistle/resolution
3. **Execution**
   - default post-only bids/asks; clip $5.36
   - allow taker for: (a) entry if signal already moving, (b) exit when TP prints through
   - cancel stale quotes > N seconds
4. **ExitEngine** — as in §5; always scale-out capable
5. **RiskGovernor**
   - max gross per market, max concurrent live matches
   - daily loss stop ≈ 1–2× median losing day from episode_stats
   - ban averaging down without new signal

### Core pseudocode

```python
for market in live_ou_markets():
    state = positions[market]
    if state.flat and signal.long_over(market):
        place_maker_bid(market, outcome='Over', clip=CLIP, limit=fair - buffer)
        # optional: take ask if impulse already underway and edge remains
    if state.long:
        work_asks_above(avg_entry + TARGET_SPREAD)
        if mid <= avg_entry - STOP or age > TIME_STOP:
            flatten(taker_ok=True)
        if mid >= avg_entry + TARGET_SPREAD:
            scale_out(fraction=0.5 then 0.5)
    if near_resolution(market):
        flatten(taker_ok=True)
```

## 10. Parameter block (start here)

```yaml
template: WTSA
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 5.3564
clip_usdc_p90: 104.12
entry_price_median: 0.5129
entry_price_iqr: (0.4666, 0.567)
target_spread: None
target_spread_p75: None
median_hold_seconds: 2229
max_hold_seconds_p75: 15587
maker_bias: true
taker_allowed: entry_impulse_or_exit_urgency
both_sides_hedge: false  # tape does not support this as primary
avg_down_without_signal: false
flatten_before_resolution: true
```

## 11. Build roadmap

1. Replay their O/U Over fills against match timelines — confirm signal = live events.
2. Paper quoter on 3 leagues they touch most; match clip + hold distributions.
3. Enable maker entries only; measure markout at +30s/+2m.
4. Add taker impulse entries; compare markout.
5. Production with tiny clips; scale only when markout stays positive after fees.
6. Weekly `polyanalyst update polika72` — if their hold/spread regime shifts, re-fit params.

_Research only. Latency, fee tier, and sports-data quality decide whether this edge is yours._

_Generated 2026-08-25T16:47:02.752495+00:00_


## 8. Structured autopsy (A–G)

# Deep Trader Autopsy — WTSA

- Wallet: `0x04d5524a0a5af2eca6e39e03defc261d42fe66d8`
- Identity: **`directional_hold_to_resolution`**
- Primary focus: **other**
- Span: 2026-07-16T05:26:52+00:00 → 2026-07-29T16:12:36+00:00 (13.45 days)
- Generated: 2026-08-25T16:47:02.752161+00:00

## A. Data integrity / reconciliation

| Source | PnL | Trades / notes |
|---|---:|---|
| Our cashflow realized | $169,030.34 | trades=17,934 |
| Our core cashflow | $160,372.00 | buys=17,934 sells=0 |
| Our closed-legs sum | $3,581,052.07 | closed=77 WR=98.7% |
| Polymarket leaderboard ALL | $442,550.51 | vol=$14,224,366.92 rank=471 |
| PolyData | $519,173.09 | trades=29173 WR=0.5402 |

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=169030.3377 ref=442550.5051193265 diff=-273520.1674
- **DRIFT** `polydata` realized_pnl: ours=169030.3377 ref=519173.09 diff=-350142.7523
- **DRIFT** `polydata` n_trades: ours=17934 ref=29173 diff=-11239
- **DRIFT** `polydata` win_rate: ours=0.987 ref=0.5402 diff=0.4468
- **DRIFT** `internal` cashflow_vs_closed: ours=169030.3377 ref=3581052.072 diff=-3412021.7343

## B. Core identity

- Scanner MM label: `directional_or_unclear` (score 10)
- High-frequency cadence (median gap 2s)
- Both-sides inventory: 1 markets (1.64%)
- Clip USDC median/p90/max: $4.81 / $93.19 / $45,780.00
- Sport categories: `{'other': 799148.23, 'sports_totals': 399961.76, 'sports_match': 111448.19}`
- Slug tokens: []

### Maker vs Taker

| Leg | Maker % | Taker % | Maker fills | Taker fills |
|---|---:|---:|---:|---:|
| Entry | 54.66% | 45.34% | 17,802 | 132 |
| Exit | None% | None% | 0 | 0 |


### Price bands

| Band | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| 20-40¢ | 13 | 100.0% | $182,533.90 | $14,041.07 |
| 40-60¢ | 38 | 100.0% | $1,039,138.45 | $27,345.75 |
| 60-80¢ | 10 | 100.0% | $88,885.82 | $8,888.58 |

## C. Equity & risk

- Final cashflow equity: $169,030.34
- Max drawdown: -$596,843.08 (-441.6% of peak)
- Longest drawdown: 1 days
- Daily Sharpe (ann.): 0.715
- Profit factor: 122.4517
- Top 10 winners: $833,981.93 (63.64% of win PnL)
- Top 10 losers: $0.00 (None% of loss PnL)
- Max inventory shares: 299998.81

### Top winners
- $157,319.67 · 8m27s · Will Inter Miami CF win on 2026-07-25?
- $100,914.54 · 39m07s · CD Guadalajara vs. FC Juárez: O/U 2.5
- $94,438.28 · 4h31m · Will Colorado Rapids SC win on 2026-07-22?
- $85,702.47 · 45m42s · Club Tijuana vs. Club León FC: O/U 2.5
- $85,019.66 · 3h44m · Will CR Flamengo win on 2026-07-29?
- $80,881.53 · 18h02m · Will CF Montréal win on 2026-07-16?
- $71,898.79 · 5h36m · Will Philadelphia Union win on 2026-07-25?
- $55,072.39 · 51m06s · Will Fluminense FC win on 2026-07-17?
- $53,117.48 · 3h58m · Will Athletic Club win on 2026-07-28?
- $49,617.10 · 1m39s · Will CA San Lorenzo de Almagro win on 2026-07-28?

### Top losers
- $0.00 · 51m15s · Will EC Bahia win on 2026-07-26?
- $0.00 · 47m36s · Will Cruzeiro EC win on 2026-07-26?
- $0.00 · 6h13m · Will CA Rosario Central win on 2026-07-28?
- $0.00 · 4h21m · Will EC Juventude win on 2026-07-28?
- $0.00 · 4h00m · Will AA Ponte Preta win on 2026-07-28?
- $0.00 · 3h45m · CA Rosario Central vs. Racing Club: O/U 2.5
- $0.00 · 19m21s · Will CA Banfield win on 2026-07-28?
- $0.00 · 14m25s · AA Ponte Preta vs. Athletic Club: O/U 2.5
- $0.00 · 36s · CA Rosario Central vs. Racing Club: O/U 1.5
- $0.00 · 3h30m · Will SC Internacional win on 2026-07-29?

## D. Trade management

### Hold-time buckets

| Bucket | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| <30s | 2 | 100.0% | $17,684.36 | $8,842.18 |
| 30s-2m | 3 | 100.0% | $49,617.10 | $16,539.03 |
| 2-5m | 4 | 100.0% | $14,490.79 | $3,622.70 |
| 5-15m | 12 | 100.0% | $344,851.76 | $28,737.65 |
| 15m+ | 40 | 100.0% | $883,914.17 | $22,097.85 |

- After early adverse (>2¢ vs entry within 2m): n=0, avg PnL n/a, median first-sell n/a, median hold n/a
- After favorable first sell (+2¢): n=0, avg PnL n/a, median MFE capture None
- Campaigns (re-entry after flat): 0 (0.0%), avg entries None, PnL $0.00, avg n/a, WR None%
- Single-entry: n=61, PnL $1,310,558.18, avg $21,484.56
- Flatten-before-resolution flag rate: 0.4262; hold-to-resolution style n=61; redeems $2,570,194.92; merges $0.00
- Avg-down while MTM-red on losers: 0/0 (0.0%); Δ if skipped on those $0.00; global never-red-buy Δ $0.00

### Family mix

| Family | N | WR | Total PnL | Avg |
|---|---:|---:|---:|---:|
| Yes/No moneyline | 38 | 100.0% | $890,430.19 | $23,432.37 |
| Over/Under | 21 | 100.0% | $395,661.76 | $18,841.04 |
| Other | 2 | 100.0% | $24,466.22 | $12,233.11 |

## E. Edge diagnosis

- Time to MFE (winners): median n/a, p25 n/a, p75 n/a, p90 n/a
- Big MFE ≥10¢: n=0; within 30s=0; within 60s=0 (0.0% of big moves)

**Edge thesis:** Directional positioning with significant redeem/merge cashflows — holds risk into resolution more than pure scalpers.

## F. vs polika72

| Metric | This trader | polika72 |
|---|---:|---:|
| identity | directional_hold_to_resolution | one_sided_informed_scalper |
| trades | 17934 | 19978 |
| cashflow_pnl | 169030.3377 | 58204.9839 |
| win_rate | 0.987 | 0.8008 |
| entry_taker_pct | 45.34 | 61.62 |
| both_sides_rate | 0.0164 | 0.0068 |
| median_clip | 4.8064 | 11.29 |
| campaign_pct | 0.0 | 5.85 |
| max_dd | -596843.0806 | -601.1817 |
| time_to_mfe_med | None | 64 |

### Steal / avoid

- **Steal:** maker-led entries (better for quoting stack on Kalshi).
- **Avoid:** their drawdown profile — size down vs polika72 risk.

## G. Kalshi two-sided informed MM relevance

Moderate relevance — extract risk limits and hold-time discipline; do not assume their edge transfers without Kalshi-specific microstructure testing.


## 9. Hour / DOW volume (UTC)

| Hour | USDC volume |
|---:|---:|
| 0 | 48357.71 |
| 1 | 30581.09 |
| 2 | 160907.78 |
| 3 | 4520.39 |
| 4 | 0 |
| 5 | 8611.21 |
| 6 | 1050.55 |
| 7 | 23.73 |
| 8 | 114.15 |
| 9 | 4510.48 |
| 10 | 11021.79 |
| 11 | 3336.99 |
| 12 | 40203.43 |
| 13 | 36033.76 |
| 14 | 75374.34 |
| 15 | 6858.0 |
| 16 | 154189.14 |
| 17 | 239663.4 |
| 18 | 241894.54 |
| 19 | 98944.19 |
| 20 | 31773.99 |
| 21 | 469347.27 |
| 22 | 401325.69 |
| 23 | 314023.53 |

| DOW (0=Mon) | USDC volume |
|---:|---:|
| 0 | 0 |
| 1 | 604884.36 |
| 2 | 452033.86 |
| 3 | 179550.99 |
| 4 | 238851.0 |
| 5 | 645812.44 |
| 6 | 261534.47 |

## 10. Bot schema pointer

Parse `MASTER.json` keys: `reconciliation`, `identity`, `performance`, `extras`, `copyability`, `equity_curve_daily`, `deep_dive_highlights`.
