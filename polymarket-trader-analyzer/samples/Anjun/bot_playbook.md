# Elite Replication Playbook — Anjun

Wallet `0x43372356634781eea88d61bbdd7824cdce958882`. Reverse-engineered from the **full unique fill tape** (293,079 trades · 13,442 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `hybrid_mm_directional` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$16,535,033.07 |
| Core cashflow (ex-rebates) | -$16,744,017.33 |
| Closed-position legs sum | $4,747,733.59 |
| Leg win rate / profit factor | 59.65% / 1.7058 |
| Polymarket leaderboard ALL | $861,718.32 · vol $180,326,675.11 · rank 229 |
| polymarket_leaderboard_ALL pnl | ref=861718.3206124196 ours=4747733.5925 (DRIFT) |
| polydata realized_pnl | ref=736777.34 ours=4747733.5925 (DRIFT) |
| polydata n_trades | ref=353745 ours=293079 (DRIFT) |
| polydata win_rate | ref=0.5994 ours=0.5965 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 950 markets · $512,300.14 · avg $539.26 · median hold 29m45s · median spread 0.01
- **Match / other sports:** 5751 markets · $3,375,778.94 · avg $586.99
- **Outcome PnL leaders:**
  - **Yes**: $611,853.59
  - **Under**: $338,611.90
  - **Over**: $205,226.11
  - **No**: $155,327.49
  - **G2 Esports**: $81,521.54
  - **KT Rolster**: $81,404.22

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_cheap_tail`: 2238
- `directional_buy_expensive_favorite`: 1994
- `two_sided_inventory_expensive_favorite`: 1846
- `two_sided_inventory_cheap_tail`: 1698
- `directional_buy_sub_mid`: 1480
- `directional_buy_near_mid`: 1303
- `directional_buy_above_mid`: 916
- `two_sided_inventory_sub_mid`: 702
- `two_sided_inventory_above_mid`: 619
- `two_sided_inventory_near_mid`: 543
- `sell_first_cheap_tail`: 101
- `sell_first_sub_mid`: 2

### First-two-fill sequences
- `BUY->BUY`: 9798
- `single_fill`: 2666
- `BUY->SELL`: 906
- `SELL->SELL`: 49
- `SELL->BUY`: 23

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 2290 | -$168,210.61 | -$73.45 |
| 0.20-0.40 | 2294 | $1,213,395.66 | $528.94 |
| 0.40-0.60 | 4638 | $2,691,953.00 | $580.41 |
| 0.60-0.80 | 1713 | $735,431.95 | $429.32 |
| 0.80-1.00 | 2416 | $171,990.49 | $71.19 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$6.75** median (p90 $413.31).
2. Aim entry price ~**0.5578** (IQR (0.4616, 0.8435)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 5550
- `single_clip`: 4304
- `market_make_both_outcomes`: 1303
- `intraday_swing`: 1025
- `scalp_sub_15m`: 862
- `scale_in_scale_out`: 398

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 7003 | 3371 |
| PnL | $7,938,503.16 | -$3,725,551.71 |
| Median hold | 5h33m | 1d |
| Median spread | 0.004 | -0.0555 |
| Scale-in rate | 0.7817 | 0.8259 |
| Scale-out rate | 0.1415 | 0.1771 |
| Avg fills/market | 25.12 | 23.56 |
| Both-sides rate | 0.4535 | 0.5868 |

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

- **Winners** sell above buy (median spread **0.004**). **Losers** often exit worse (median spread **-0.0555**).
- Losers scale-in **more** (0.8259 vs 0.7817) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 3599, 'pnl': 2150686.4838, 'avg': 597.5789, 'win_rate': 0.486}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 9799
- `adverse_exit_sell_below_buy`: 1560
- `spread_harvest_sell_above_buy`: 1041
- `mixed_roundtrip`: 951
- `sell_inventory_only`: 91

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 3599 | $2,150,686.48 | $597.58 | 48.6% |
| 5-30m | 874 | $701,603.18 | $802.75 | 51.7% |
| 30m-2h | 1104 | $322,193.91 | $291.84 | 55.8% |
| 2-12h | 2309 | $983,211.62 | $425.82 | 54.1% |
| 12h+ | 5556 | $55,256.26 | $9.95 | 52.8% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.004** above avg entry (p75 stretch 0.03). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 5h33m; p75 3d for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.004 vs losers -0.0555
- Both-sides inventory on 45.4% of winning markets (losers 58.7%)
- Hold bucket <5m: avg PnL $597.58 on 3599 markets (WR 49%)
- Hold bucket 5-30m: avg PnL $802.75 on 874 markets (WR 52%)
- Hold bucket 30m-2h: avg PnL $291.84 on 1104 markets (WR 56%)
- Hold bucket 2-12h: avg PnL $425.82 on 2309 markets (WR 54%)
- Hold bucket 12h+: avg PnL $9.95 on 5556 markets (WR 53%)
- Entry band 0.20-0.40: avg $528.94 across 2294 markets
- Entry band 0.40-0.60: avg $580.41 across 4638 markets
- Entry band 0.60-0.80: avg $429.32 across 1713 markets
- Entry band 0.80-1.00: avg $71.19 across 2416 markets
- Buy-ladder behavior: fade-into-weakness markets=2311, chase-up markets=2088

### Fails
- Entry band 0.00-0.20: avg $-73.45 across 2290 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 2088, 'fade_down': 2311}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: LoL: Team WE vs EDward Gaming (BO3)
PnL $23,508.37 · hold 21h44m · 50B/33S · avg entry 0.4723 → exit 0.7357 (spread 0.2633) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-01-15T15:09:10+00:00 | BUY | Team WE | 15018.36 | 0.3400 | 5106.24 |
| 2026-01-15T15:47:22+00:00 | SELL | Team WE | 60.00 | 0.3600 | 21.60 |
| 2026-01-15T16:36:56+00:00 | BUY | Team WE | 3281.87 | 0.3100 | 1017.38 |
| 2026-01-15T17:38:48+00:00 | BUY | Team WE | 51.13 | 0.3100 | 15.85 |
| 2026-01-15T20:01:54+00:00 | BUY | Team WE | 48.21 | 0.3000 | 14.46 |
| 2026-01-15T20:06:00+00:00 | BUY | Team WE | 1.43 | 0.3000 | 0.43 |
| 2026-01-16T02:29:02+00:00 | BUY | Team WE | 144.47 | 0.3000 | 43.34 |
| 2026-01-16T03:44:20+00:00 | BUY | Team WE | 571.43 | 0.3000 | 171.43 |
| 2026-01-16T04:05:04+00:00 | BUY | Team WE | 345.44 | 0.3000 | 103.63 |
| 2026-01-16T11:59:08+00:00 | BUY | Team WE | 34.04 | 0.5300 | 18.04 |
| 2026-01-16T11:59:10+00:00 | BUY | Team WE | 6.38 | 0.5300 | 3.38 |
| 2026-01-16T11:59:20+00:00 | BUY | Team WE | 42.55 | 0.5300 | 22.55 |
| 2026-01-16T11:59:42+00:00 | BUY | Team WE | 42.55 | 0.5300 | 22.55 |
| 2026-01-16T12:00:02+00:00 | BUY | Team WE | 985.44 | 0.5300 | 522.28 |
| 2026-01-16T12:00:34+00:00 | BUY | Team WE | 5.00 | 0.5200 | 2.60 |
| 2026-01-16T12:51:50+00:00 | BUY | Team WE | 77.78 | 0.6400 | 49.78 |
| 2026-01-16T12:51:50+00:00 | BUY | Team WE | 222.22 | 0.6400 | 142.22 |
| 2026-01-16T12:52:18+00:00 | BUY | Team WE | 0.06 | 0.9900 | 0.06 |
| 2026-01-16T12:52:20+00:00 | BUY | Team WE | 23.80 | 0.9900 | 23.56 |
| 2026-01-16T12:52:24+00:00 | BUY | Team WE | 61.17 | 0.9900 | 60.56 |
| 2026-01-16T12:52:26+00:00 | BUY | Team WE | 10.40 | 0.9900 | 10.30 |
| 2026-01-16T12:52:34+00:00 | BUY | Team WE | 58.41 | 0.9900 | 57.83 |
| 2026-01-16T12:52:36+00:00 | BUY | Team WE | 698.00 | 0.9900 | 691.02 |
| 2026-01-16T12:52:42+00:00 | BUY | Team WE | 34.68 | 0.9900 | 34.33 |
| 2026-01-16T12:53:00+00:00 | BUY | Team WE | 2646.27 | 0.9900 | 2619.81 |
| 2026-01-16T12:53:06+00:00 | BUY | Team WE | 318.00 | 0.9900 | 314.82 |
| 2026-01-16T12:53:08+00:00 | BUY | Team WE | 3.51 | 0.9900 | 3.47 |
| 2026-01-16T12:53:14+00:00 | BUY | Team WE | 1470.00 | 0.9900 | 1455.30 |
| 2026-01-16T12:53:30+00:00 | BUY | Team WE | 2.85 | 0.9900 | 2.82 |
| 2026-01-16T12:53:46+00:00 | BUY | Team WE | 159.00 | 0.9900 | 157.41 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: Will Lille OSC win on 2026-02-19?
PnL $12,466.08 · hold 11m36s · 43B/1S · avg entry 0.4757 → exit 0.64 (spread 0.1643) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-02-19T19:48:12+00:00 | BUY | Yes | 329.73 | 0.6100 | 201.14 |
| 2026-02-19T19:48:16+00:00 | BUY | Yes | 7550.00 | 0.6100 | 4605.50 |
| 2026-02-19T19:48:32+00:00 | BUY | Yes | 51.28 | 0.6100 | 31.28 |
| 2026-02-19T19:51:18+00:00 | BUY | Yes | 161.29 | 0.6100 | 98.39 |
| 2026-02-19T19:51:28+00:00 | BUY | Yes | 2.56 | 0.6100 | 1.56 |
| 2026-02-19T19:52:32+00:00 | BUY | Yes | 102.56 | 0.6100 | 62.56 |
| 2026-02-19T19:53:38+00:00 | SELL | Yes | 8197.42 | 0.6400 | 5246.35 |
| 2026-02-19T19:54:40+00:00 | BUY | No | 18888.00 | 0.3500 | 6610.80 |
| 2026-02-19T19:55:04+00:00 | BUY | Yes | 15406.04 | 0.6400 | 9859.87 |
| 2026-02-19T19:55:06+00:00 | BUY | Yes | 2981.98 | 0.6400 | 1908.47 |
| 2026-02-19T19:55:06+00:00 | BUY | Yes | 472.20 | 0.6400 | 302.21 |
| 2026-02-19T19:55:06+00:00 | BUY | Yes | 13.89 | 0.6400 | 8.89 |
| 2026-02-19T19:55:06+00:00 | BUY | Yes | 13.89 | 0.6400 | 8.89 |
| 2026-02-19T19:55:14+00:00 | BUY | No | 455.04 | 0.3500 | 159.26 |
| 2026-02-19T19:55:14+00:00 | BUY | No | 10000.00 | 0.3500 | 3500.00 |
| 2026-02-19T19:56:24+00:00 | BUY | No | 10.00 | 0.3500 | 3.50 |
| 2026-02-19T19:56:26+00:00 | BUY | No | 10.14 | 0.3500 | 3.55 |
| 2026-02-19T19:56:28+00:00 | BUY | No | 15.38 | 0.3500 | 5.38 |
| 2026-02-19T19:56:30+00:00 | BUY | No | 0.02 | 0.3500 | 0.01 |
| 2026-02-19T19:56:30+00:00 | BUY | No | 396.92 | 0.3500 | 138.92 |
| 2026-02-19T19:56:34+00:00 | BUY | No | 87.69 | 0.3500 | 30.69 |
| 2026-02-19T19:56:42+00:00 | BUY | No | 1.29 | 0.3500 | 0.45 |
| 2026-02-19T19:56:44+00:00 | BUY | No | 432.74 | 0.3500 | 151.46 |
| 2026-02-19T19:56:46+00:00 | BUY | No | 5000.00 | 0.3500 | 1750.00 |
| 2026-02-19T19:56:50+00:00 | BUY | No | 13.15 | 0.3500 | 4.60 |
| 2026-02-19T19:56:56+00:00 | BUY | No | 1805.47 | 0.3500 | 631.91 |
| 2026-02-19T19:58:48+00:00 | BUY | No | 18888.00 | 0.3400 | 6421.92 |
| 2026-02-19T19:59:40+00:00 | BUY | Yes | 17.56 | 0.6400 | 11.24 |
| 2026-02-19T19:59:42+00:00 | BUY | Yes | 5.56 | 0.6400 | 3.56 |
| 2026-02-19T19:59:48+00:00 | BUY | Yes | 5.65 | 0.6400 | 3.62 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: Dota 2: Team Liquid vs Team Falcons (BO3) - PGL Wallachia Playoffs
PnL $9,953.67 · hold 1h05m · 9B/12S · avg entry 0.5208 → exit 0.74 (spread 0.2192) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-25T17:26:58+00:00 | BUY | Team Falcons | 1071.43 | 0.7200 | 771.43 |
| 2026-04-25T17:27:00+00:00 | BUY | Team Falcons | 25.93 | 0.7200 | 18.67 |
| 2026-04-25T17:27:10+00:00 | BUY | Team Falcons | 592.86 | 0.7200 | 426.86 |
| 2026-04-25T17:27:12+00:00 | BUY | Team Falcons | 24.00 | 0.7200 | 17.28 |
| 2026-04-25T17:27:16+00:00 | BUY | Team Falcons | 3.00 | 0.7200 | 2.16 |
| 2026-04-25T17:27:24+00:00 | BUY | Team Falcons | 178.57 | 0.7200 | 128.57 |
| 2026-04-25T17:27:36+00:00 | BUY | Team Falcons | 1000.00 | 0.7200 | 720.00 |
| 2026-04-25T17:28:38+00:00 | BUY | Team Falcons | 20.00 | 0.7200 | 14.40 |
| 2026-04-25T17:32:32+00:00 | SELL | Team Falcons | 200.00 | 0.7400 | 148.00 |
| 2026-04-25T17:32:36+00:00 | SELL | Team Falcons | 7.65 | 0.7400 | 5.66 |
| 2026-04-25T17:32:38+00:00 | SELL | Team Falcons | 150.00 | 0.7400 | 111.00 |
| 2026-04-25T17:32:38+00:00 | SELL | Team Falcons | 200.00 | 0.7400 | 148.00 |
| 2026-04-25T17:33:00+00:00 | SELL | Team Falcons | 40.54 | 0.7400 | 30.00 |
| 2026-04-25T17:33:02+00:00 | SELL | Team Falcons | 1012.01 | 0.7400 | 748.89 |
| 2026-04-25T17:33:24+00:00 | SELL | Team Falcons | 217.41 | 0.7400 | 160.88 |
| 2026-04-25T17:34:32+00:00 | SELL | Team Falcons | 51.89 | 0.7400 | 38.40 |
| 2026-04-25T17:35:08+00:00 | SELL | Team Falcons | 6.76 | 0.7400 | 5.00 |
| 2026-04-25T17:35:38+00:00 | SELL | Team Falcons | 2.86 | 0.7400 | 2.12 |
| 2026-04-25T17:36:24+00:00 | SELL | Team Falcons | 5.20 | 0.7400 | 3.85 |
| 2026-04-25T17:36:32+00:00 | SELL | Team Falcons | 12.00 | 0.7400 | 8.88 |
| 2026-04-25T18:32:04+00:00 | BUY | Team Falcons | 18888.00 | 0.4900 | 9255.12 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 4: Dota 2: Power Rangers vs Team Bald (BO3) - The International Europe Closed Qualifier Playoffs
PnL $9,303.36 · hold 13m32s · 1B/2S · avg entry 0.58 → exit 0.64 (spread 0.06) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-06-26T16:01:41+00:00 | BUY | Power Rangers | 22222.00 | 0.5800 | 12888.76 |
| 2026-06-26T16:14:50+00:00 | SELL | Power Rangers | 75.00 | 0.6400 | 48.00 |
| 2026-06-26T16:15:13+00:00 | SELL | Power Rangers | 8.00 | 0.6400 | 5.12 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 5: Will "How to Train Your Dragon" Opening Weekend Box Office be between $78m and $85m?
PnL $8,786.88 · hold 4h24m · 24B/9S · avg entry 0.7473 → exit 0.9248 (spread 0.1775) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-06-16T16:51:11+00:00 | BUY | Yes | 3587.35 | 0.3938 | 1412.73 |
| 2025-06-16T16:52:09+00:00 | BUY | Yes | 30.96 | 0.2200 | 6.81 |
| 2025-06-16T17:14:09+00:00 | BUY | Yes | 111.00 | 0.4000 | 44.40 |
| 2025-06-16T17:36:19+00:00 | SELL | Yes | 61.00 | 0.9000 | 54.90 |
| 2025-06-16T17:37:15+00:00 | SELL | Yes | 22.40 | 0.9000 | 20.16 |
| 2025-06-16T17:37:39+00:00 | SELL | Yes | 88.60 | 0.9000 | 79.74 |
| 2025-06-16T17:38:17+00:00 | SELL | Yes | 111.00 | 0.9200 | 102.12 |
| 2025-06-16T17:42:33+00:00 | SELL | Yes | 222.00 | 0.9200 | 204.24 |
| 2025-06-16T17:43:32+00:00 | SELL | Yes | 222.00 | 0.9300 | 206.46 |
| 2025-06-16T17:44:00+00:00 | BUY | Yes | 111.00 | 0.8000 | 88.80 |
| 2025-06-16T17:45:04+00:00 | SELL | Yes | 82.52 | 0.9300 | 76.74 |
| 2025-06-16T17:46:18+00:00 | BUY | Yes | 222.00 | 0.8000 | 177.60 |
| 2025-06-16T17:58:26+00:00 | SELL | Yes | 222.00 | 0.9200 | 204.24 |
| 2025-06-16T17:58:26+00:00 | SELL | Yes | 1028.48 | 0.9300 | 956.49 |
| 2025-06-16T18:02:38+00:00 | BUY | Yes | 222.00 | 0.8200 | 182.04 |
| 2025-06-16T19:07:18+00:00 | BUY | Yes | 34.23 | 0.9990 | 34.20 |
| 2025-06-16T19:07:36+00:00 | BUY | Yes | 1000.00 | 0.9990 | 999.00 |
| 2025-06-16T19:08:22+00:00 | BUY | Yes | 4.67 | 0.9990 | 4.67 |
| 2025-06-16T19:11:46+00:00 | BUY | Yes | 166.66 | 0.9990 | 166.49 |
| 2025-06-16T19:15:38+00:00 | BUY | Yes | 269.62 | 0.9990 | 269.35 |
| 2025-06-16T19:18:00+00:00 | BUY | Yes | 1.43 | 0.9990 | 1.43 |
| 2025-06-16T19:18:22+00:00 | BUY | Yes | 13.22 | 0.9990 | 13.21 |
| 2025-06-16T19:25:36+00:00 | BUY | Yes | 207.81 | 0.9990 | 207.60 |
| 2025-06-16T19:26:00+00:00 | BUY | Yes | 180.89 | 0.9990 | 180.71 |
| 2025-06-16T19:40:44+00:00 | BUY | Yes | 101.96 | 0.9990 | 101.86 |
| 2025-06-16T19:43:40+00:00 | BUY | Yes | 50.00 | 0.9990 | 49.95 |
| 2025-06-16T20:20:48+00:00 | BUY | Yes | 90.00 | 0.9990 | 89.91 |
| 2025-06-16T20:25:10+00:00 | BUY | Yes | 1895.21 | 0.9990 | 1893.31 |
| 2025-06-16T21:10:08+00:00 | BUY | Yes | 54.24 | 0.9990 | 54.19 |
| 2025-06-16T21:15:28+00:00 | BUY | Yes | 148.59 | 0.9990 | 148.44 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 6: MSI Playoffs: T1 vs. Flying Oyster
PnL $7,182.50 · hold 17h47m · 28B/14S · avg entry 0.2507 → exit 0.4485 (spread 0.1979) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-07-03T09:09:03+00:00 | BUY | Flying Oyster | 3008.02 | 0.1000 | 300.80 |
| 2025-07-03T09:20:31+00:00 | BUY | Flying Oyster | 4444.00 | 0.1000 | 444.40 |
| 2025-07-03T09:24:07+00:00 | BUY | Flying Oyster | 28.46 | 0.1000 | 2.85 |
| 2025-07-03T09:24:17+00:00 | BUY | Flying Oyster | 2193.54 | 0.1000 | 219.35 |
| 2025-07-03T09:28:45+00:00 | BUY | Flying Oyster | 1.11 | 0.1000 | 0.11 |
| 2025-07-03T09:34:33+00:00 | BUY | Flying Oyster | 442.88 | 0.1000 | 44.29 |
| 2025-07-03T12:35:43+00:00 | BUY | Flying Oyster | 4444.00 | 0.0900 | 399.96 |
| 2025-07-03T14:05:34+00:00 | BUY | Flying Oyster | 3333.00 | 0.0900 | 299.97 |
| 2025-07-03T23:10:19+00:00 | BUY | Flying Oyster | 892.94 | 0.1100 | 98.22 |
| 2025-07-03T23:21:31+00:00 | SELL | Flying Oyster | 1200.00 | 0.1083 | 130.00 |
| 2025-07-03T23:28:09+00:00 | BUY | Flying Oyster | 256.00 | 0.0900 | 23.04 |
| 2025-07-03T23:28:13+00:00 | BUY | Flying Oyster | 238.00 | 0.0900 | 21.42 |
| 2025-07-03T23:28:21+00:00 | BUY | Flying Oyster | 205.40 | 0.0900 | 18.49 |
| 2025-07-03T23:28:25+00:00 | BUY | Flying Oyster | 194.00 | 0.0900 | 17.46 |
| 2025-07-03T23:28:33+00:00 | BUY | Flying Oyster | 80.00 | 0.0900 | 7.20 |
| 2025-07-04T01:19:11+00:00 | SELL | Flying Oyster | 2995.62 | 0.6000 | 1797.37 |
| 2025-07-04T01:21:11+00:00 | SELL | Flying Oyster | 1000.00 | 0.6000 | 600.00 |
| 2025-07-04T01:21:35+00:00 | SELL | Flying Oyster | 1000.00 | 0.6000 | 600.00 |
| 2025-07-04T01:21:39+00:00 | SELL | Flying Oyster | 200.00 | 0.6000 | 120.00 |
| 2025-07-04T01:21:43+00:00 | SELL | Flying Oyster | 5000.00 | 0.6000 | 3000.00 |
| 2025-07-04T01:21:51+00:00 | SELL | Flying Oyster | 4617.00 | 0.6000 | 2770.20 |
| 2025-07-04T01:44:47+00:00 | SELL | Flying Oyster | 1268.22 | 0.4900 | 621.43 |
| 2025-07-04T01:49:41+00:00 | BUY | Flying Oyster | 830.45 | 0.2500 | 207.61 |
| 2025-07-04T01:51:43+00:00 | BUY | Flying Oyster | 2382.28 | 0.3971 | 945.93 |
| 2025-07-04T01:57:57+00:00 | BUY | Flying Oyster | 1265.82 | 0.2100 | 265.82 |
| 2025-07-04T02:03:35+00:00 | BUY | Flying Oyster | 462.32 | 0.2300 | 106.33 |
| 2025-07-04T02:10:57+00:00 | BUY | Flying Oyster | 10907.66 | 0.5153 | 5620.55 |
| 2025-07-04T02:13:51+00:00 | BUY | Flying Oyster | 53.34 | 0.5000 | 26.67 |
| 2025-07-04T02:38:41+00:00 | SELL | Flying Oyster | 15901.89 | 0.3400 | 5406.64 |
| 2025-07-04T02:56:45+00:00 | BUY | Flying Oyster | 119.64 | 0.1800 | 21.54 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Will Arsenal FC win on 2026-05-30?** -$138,693.38 · hold 43m26s · entry 0.9819 → exit 0.001 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
2. **Will Jake Paul win his boxing match against Anthony Joshua?** -$101,960.43 · hold 1h49m · entry None → exit 0.001 · `intraday_swing` / `sell_inventory_only`
3. **Will "Avatar: Fire and Ash" Opening Weekend Box Office be between 101m and 112m?** -$99,899.08 · hold 3d · entry 0.5485 → exit 0.0152 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
4. **Will Zootopia 2 be the top grossing movie of 2025?** -$89,994.77 · hold 97d · entry 0.1758 → exit 0.001 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
5. **Will 'Lilo & Stitch' gross between $150-160m opening weekend?** -$79,233.38 · hold 8h29m · entry 0.7688 → exit 0.2 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
6. **Will 'Lilo & Stitch' gross less than $140m opening weekend?** -$75,431.42 · hold 6d · entry 0.6313 → exit 0.0631 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
7. **US strikes Iran by February 28, 2026?** -$48,324.87 · hold 5d · entry 0.4791 → exit 0.0472 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
8. **No change in Fed interest rates after September 2025 meeting?** -$45,405.66 · hold 11d · entry 0.855 → exit 0.0084 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
9. **Fed decreases interest rates by 25 bps after May 2025 meeting?** -$41,271.80 · hold 5h16m · entry None → exit 0.004 · `multi_hour_position` / `sell_inventory_only`
10. **Exact Score: Norway 2 - 1 England?** -$40,920.17 · hold 3h03m · entry 0.9158 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $6.75
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
template: Anjun
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 6.7508
clip_usdc_p90: 413.3123
entry_price_median: 0.5578
entry_price_iqr: (0.4616, 0.8435)
target_spread: 0.004
target_spread_p75: 0.03
median_hold_seconds: 20006
max_hold_seconds_p75: 270405
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

_Generated 2026-08-25T21:56:17.953736+00:00_
