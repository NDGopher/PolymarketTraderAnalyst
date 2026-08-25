# Elite Replication Playbook — polika72

Wallet `0x13997bdbf1b291b7ba65afaf1f0d8e4719ee48c8`. Reverse-engineered from the **full unique fill tape** (19,978 trades · 5,422 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

**polika72 is NOT a classic two-sided market maker.** Both-sides inventory is ~0–1% of winning markets. The real craft is:

> **Live / short-horizon one-sided scalping on sports markets (especially O/U Over)** — BUY a clip, then SELL the *same* outcome higher within seconds to a few minutes. Maker-biased. Repeat.

Evidence: BUY→SELL opens 3478/5422 episodes; median winner hold 1m06s; winner median spread (exit−entry) 0.2; Over PnL $40,676.84 vs Under $0.00; maker rebates $481.53 >> taker $24.37.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $58,204.98 |
| Core cashflow (ex-rebates) | $57,699.08 |
| Closed-position legs sum | $61,909.37 |
| Leg win rate / profit factor | 80.08% / 3.2979 |
| Polymarket leaderboard ALL | $57,338.72 · vol $1,049,905.19 · rank 3244 |
| polymarket_leaderboard_ALL pnl | ref=57338.716846567695 ours=57699.0816 (MATCH) |
| polydata realized_pnl | ref=52640.69 ours=57699.0816 (DRIFT) |
| polydata n_trades | ref=24078 ours=19978 (DRIFT) |
| polydata win_rate | ref=0.6567 ours=0.8008 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 3543 markets · $40,676.84 · avg $11.48 · median hold 1m17s · median spread 0.14
- **Match / other sports:** 1407 markets · $19,244.14 · avg $13.68
- **Outcome PnL leaders:**
  - **Over**: $40,676.84
  - **Yes**: $15,710.24
  - **No**: $5,352.56
  - **United States**: $66.79
  - **CA Talleres**: $15.39
  - **Club Nacional de Football**: $11.05

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_above_mid`: 1563
- `directional_buy_sub_mid`: 1371
- `directional_buy_cheap_tail`: 1264
- `directional_buy_near_mid`: 824
- `directional_buy_expensive_favorite`: 363
- `two_sided_inventory_near_mid`: 12
- `two_sided_inventory_sub_mid`: 10
- `two_sided_inventory_cheap_tail`: 7
- `two_sided_inventory_expensive_favorite`: 4
- `two_sided_inventory_above_mid`: 4

### First-two-fill sequences
- `BUY->SELL`: 3478
- `BUY->BUY`: 1570
- `single_fill`: 374

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 911 | $4,534.27 | $4.98 |
| 0.20-0.40 | 1287 | $15,243.27 | $11.84 |
| 0.40-0.60 | 1490 | $22,792.05 | $15.30 |
| 0.60-0.80 | 1464 | $17,941.96 | $12.26 |
| 0.80-1.00 | 270 | $1,397.81 | $5.18 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$11.29** median (p90 $53.32).
2. Aim entry price ~**0.4836** (IQR (0.3, 0.66)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 2720
- `scalp_sub_15m`: 1964
- `scale_in_scale_out`: 423
- `intraday_swing`: 281
- `market_make_both_outcomes`: 28
- `multi_hour_position`: 6

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 4012 | 993 |
| PnL | $88,793.58 | -$26,884.21 |
| Median hold | 1m06s | 1m50s |
| Median spread | 0.2 | -0.04 |
| Scale-in rate | 0.2804 | 0.3897 |
| Scale-out rate | 0.4045 | 0.5186 |
| Avg fills/market | 3.71 | 4.15 |
| Both-sides rate | 0.0082 | 0.004 |

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

- **Winners** sell above buy (median spread **0.2**). **Losers** often exit worse (median spread **-0.04**).
- Losers scale-in **more** (0.3897 vs 0.2804) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 4682, 'pnl': 47724.0203, 'avg': 10.1931, 'win_rate': 0.754}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `spread_harvest_sell_above_buy`: 4099
- `adverse_exit_sell_below_buy`: 734
- `hold_to_resolution_or_redeem`: 489
- `mixed_roundtrip`: 100

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 4682 | $47,724.02 | $10.19 | 75.4% |
| 5-30m | 440 | $3,334.56 | $7.58 | 59.6% |
| 30m-2h | 292 | $10,450.79 | $35.79 | 73.0% |
| 2-12h | 7 | $374.86 | $53.55 | 85.7% |
| 12h+ | 1 | $25.14 | $25.14 | 100.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.2** above avg entry (p75 stretch 0.3137). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 1m06s; p75 1m52s for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.2 vs losers -0.04
- Both-sides inventory on 0.8% of winning markets (losers 0.4%)
- Hold bucket <5m: avg PnL $10.19 on 4682 markets (WR 75%)
- Hold bucket 5-30m: avg PnL $7.58 on 440 markets (WR 60%)
- Hold bucket 30m-2h: avg PnL $35.79 on 292 markets (WR 73%)
- Entry band 0.20-0.40: avg $11.84 across 1287 markets
- Entry band 0.40-0.60: avg $15.30 across 1490 markets
- Entry band 0.60-0.80: avg $12.26 across 1464 markets
- Buy-ladder behavior: fade-into-weakness markets=64, chase-up markets=253

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 253, 'fade_down': 64}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: FC St. Pauli 1910 vs. FC Bayern München: O/U 3.5
PnL $841.93 · hold 1h12m · 6B/9S · avg entry 0.3703 → exit 0.5992 (spread 0.2289) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-11T16:40:15+00:00 | BUY | Over | 256.45 | 0.4500 | 115.40 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 256.40 | 0.4470 | 114.61 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 256.45 | 0.4500 | 115.40 |
| 2026-04-11T16:41:37+00:00 | SELL | Over | 17.20 | 0.5900 | 10.15 |
| 2026-04-11T16:42:13+00:00 | SELL | Over | 3.02 | 0.5700 | 1.72 |
| 2026-04-11T16:42:15+00:00 | SELL | Over | 231.78 | 0.5700 | 132.11 |
| 2026-04-11T16:42:21+00:00 | SELL | Over | 265.00 | 0.5800 | 153.70 |
| 2026-04-11T16:42:21+00:00 | SELL | Over | 265.00 | 0.5800 | 153.70 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 201.13 | 0.2700 | 54.30 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 201.12 | 0.2700 | 54.30 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 201.12 | 0.2700 | 54.30 |
| 2026-04-11T17:48:01+00:00 | SELL | Over | 210.20 | 0.4371 | 91.89 |
| 2026-04-11T17:52:23+00:00 | SELL | Over | 39.00 | 0.7549 | 29.44 |
| 2026-04-11T17:52:25+00:00 | SELL | Over | 19.00 | 0.7500 | 14.25 |
| 2026-04-11T17:52:39+00:00 | SELL | Over | 349.10 | 0.7205 | 251.53 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: FC Bayern München vs. Real Madrid CF: O/U 3.5
PnL $645.59 · hold 6m02s · 4B/4S · avg entry 0.6513 → exit 0.775 (spread 0.1238) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-15T19:02:40+00:00 | BUY | Over | 351.06 | 0.6407 | 224.93 |
| 2026-04-15T19:02:40+00:00 | BUY | Over | 351.05 | 0.6400 | 224.67 |
| 2026-04-15T19:02:40+00:00 | BUY | Over | 351.05 | 0.6400 | 224.67 |
| 2026-04-15T19:03:16+00:00 | SELL | Over | 358.70 | 0.7500 | 269.02 |
| 2026-04-15T19:03:18+00:00 | SELL | Over | 358.70 | 0.7571 | 271.57 |
| 2026-04-15T19:03:26+00:00 | SELL | Over | 347.30 | 0.7900 | 274.37 |
| 2026-04-15T19:07:54+00:00 | BUY | Over | 107.03 | 0.7600 | 81.34 |
| 2026-04-15T19:08:42+00:00 | SELL | Over | 107.70 | 0.8700 | 93.70 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: FC St. Pauli 1910 vs. FC Bayern München: O/U 4.5
PnL $640.86 · hold 1h18m · 7B/24S · avg entry 0.1881 → exit 0.2751 (spread 0.087) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-11T16:40:15+00:00 | BUY | Over | 208.16 | 0.2600 | 54.12 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 208.17 | 0.2600 | 54.12 |
| 2026-04-11T16:40:15+00:00 | BUY | Over | 208.16 | 0.2600 | 54.12 |
| 2026-04-11T16:41:17+00:00 | SELL | Over | 85.00 | 0.3488 | 29.65 |
| 2026-04-11T16:41:19+00:00 | SELL | Over | 9.10 | 0.3200 | 2.91 |
| 2026-04-11T16:41:27+00:00 | SELL | Over | 203.40 | 0.3200 | 65.09 |
| 2026-04-11T16:42:01+00:00 | SELL | Over | 24.37 | 0.3000 | 7.31 |
| 2026-04-11T16:42:01+00:00 | SELL | Over | 132.60 | 0.3000 | 39.78 |
| 2026-04-11T16:42:01+00:00 | SELL | Over | 40.00 | 0.3000 | 12.00 |
| 2026-04-11T16:42:03+00:00 | SELL | Over | 40.29 | 0.3000 | 12.09 |
| 2026-04-11T16:42:03+00:00 | SELL | Over | 33.33 | 0.3000 | 10.00 |
| 2026-04-11T16:43:13+00:00 | SELL | Over | 70.80 | 0.3854 | 27.28 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 225.51 | 0.1200 | 27.06 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 225.49 | 0.1200 | 27.06 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 225.49 | 0.1200 | 27.06 |
| 2026-04-11T17:47:21+00:00 | SELL | Over | 37.80 | 0.1562 | 5.90 |
| 2026-04-11T17:48:21+00:00 | SELL | Over | 17.80 | 0.2300 | 4.09 |
| 2026-04-11T17:48:31+00:00 | SELL | Over | 61.38 | 0.1200 | 7.37 |
| 2026-04-11T17:48:33+00:00 | SELL | Over | 83.33 | 0.1200 | 10.00 |
| 2026-04-11T17:48:41+00:00 | SELL | Over | 75.20 | 0.2529 | 19.02 |
| 2026-04-11T17:51:27+00:00 | SELL | Over | 36.00 | 0.4100 | 14.76 |
| 2026-04-11T17:51:31+00:00 | SELL | Over | 36.00 | 0.4100 | 14.76 |
| 2026-04-11T17:51:31+00:00 | SELL | Over | 15.00 | 0.4100 | 6.15 |
| 2026-04-11T17:51:47+00:00 | SELL | Over | 15.00 | 0.4000 | 6.00 |
| 2026-04-11T17:51:49+00:00 | SELL | Over | 37.00 | 0.4000 | 14.80 |
| 2026-04-11T17:51:51+00:00 | SELL | Over | 15.00 | 0.4000 | 6.00 |
| 2026-04-11T17:52:07+00:00 | SELL | Over | 38.00 | 0.3900 | 14.82 |
| 2026-04-11T17:52:11+00:00 | SELL | Over | 27.60 | 0.3900 | 10.76 |
| 2026-04-11T17:58:05+00:00 | BUY | Over | 6.49 | 0.3700 | 2.40 |
| 2026-04-11T17:58:59+00:00 | SELL | Over | 6.60 | 0.6400 | 4.22 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 4: Will Club Atlético de Madrid win on 2026-08-23?
PnL $629.26 · hold 2m18s · 2B/3S · avg entry 0.426 → exit 0.7479 (spread 0.3219) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-08-23T16:24:07+00:00 | BUY | Yes | 1978.70 | 0.4249 | 840.78 |
| 2026-08-23T16:24:07+00:00 | BUY | Yes | 116.90 | 0.4446 | 51.98 |
| 2026-08-23T16:24:54+00:00 | SELL | Yes | 116.80 | 0.7500 | 87.60 |
| 2026-08-23T16:25:49+00:00 | SELL | Yes | 1978.60 | 0.7478 | 1479.63 |
| 2026-08-23T16:26:25+00:00 | SELL | Yes | 0.20 | 0.7500 | 0.15 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 5: Will Real Madrid CF win on 2026-03-17?
PnL $564.47 · hold 13m06s · 1B/2S · avg entry 0.07 → exit 0.9561 (spread 0.8861) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-03-17T21:51:37+00:00 | BUY | Yes | 637.00 | 0.0700 | 44.59 |
| 2026-03-17T21:52:33+00:00 | SELL | Yes | 171.70 | 0.8400 | 144.22 |
| 2026-03-17T22:04:43+00:00 | SELL | Yes | 465.30 | 0.9990 | 464.83 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 6: FC St. Pauli 1910 vs. FC Bayern München: O/U 2.5
PnL $544.83 · hold 1h10m · 5B/6S · avg entry 0.5686 → exit 0.8888 (spread 0.3202) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-04-11T16:40:15+00:00 | BUY | Over | 113.57 | 0.6639 | 75.40 |
| 2026-04-11T16:40:21+00:00 | BUY | Over | 6.06 | 0.6700 | 4.06 |
| 2026-04-11T16:42:21+00:00 | SELL | Over | 120.70 | 0.7900 | 95.35 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 204.66 | 0.5500 | 112.56 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 204.65 | 0.5500 | 112.56 |
| 2026-04-11T17:45:45+00:00 | BUY | Over | 204.65 | 0.5500 | 112.56 |
| 2026-04-11T17:46:51+00:00 | SELL | Over | 7.04 | 0.7100 | 5.00 |
| 2026-04-11T17:46:51+00:00 | SELL | Over | 6.00 | 0.7100 | 4.26 |
| 2026-04-11T17:46:53+00:00 | SELL | Over | 9.00 | 0.7100 | 6.39 |
| 2026-04-11T17:46:59+00:00 | SELL | Over | 202.00 | 0.7500 | 151.50 |
| 2026-04-11T17:50:23+00:00 | SELL | Over | 398.40 | 0.9990 | 398.00 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **RC Strasbourg Alsace vs. OGC Nice: O/U 3.5** -$515.82 · hold 6m46s · entry 0.34 → exit 0.27 · `scalp_sub_15m` / `adverse_exit_sell_below_buy`
2. **Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5** -$508.72 · hold 1h27m · entry 0.2996 → exit 0.2866 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
3. **Panama vs. England: Both Teams to Score** -$474.32 · hold 3m46s · entry 0.66 → exit 0.04 · `single_clip` / `adverse_exit_sell_below_buy`
4. **Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5** -$471.20 · hold 1h16m · entry 0.2806 → exit 0.47 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
5. **Will Paris Saint-Germain FC win on 2026-04-22?** -$427.80 · hold 46s · entry 0.06 → exit 0.15 · `single_clip` / `spread_harvest_sell_above_buy`
6. **RC Strasbourg Alsace vs. OGC Nice: O/U 4.5** -$427.77 · hold 8m10s · entry 0.17 → exit 0.11 · `scalp_sub_15m` / `adverse_exit_sell_below_buy`
7. **Sporting CP vs. Arsenal FC: O/U 2.5** -$416.80 · hold 1m14s · entry 0.06 → exit 0.0523 · `scalp_sub_15m` / `mixed_roundtrip`
8. **UD Las Palmas vs. SD Huesca: O/U 3.5** -$414.38 · hold 8m10s · entry 0.2097 → exit 0.1768 · `scalp_sub_15m` / `adverse_exit_sell_below_buy`
9. **Real Madrid CF vs. Deportivo Alavés: O/U 3.5** -$388.13 · hold 2m16s · entry 0.5837 → exit 0.507 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
10. **Cádiz CF vs. Córdoba CF: O/U 4.5** -$384.52 · hold 23m30s · entry 0.05 → exit 0.1199 · `intraday_swing` / `spread_harvest_sell_above_buy`

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
   - default post-only bids/asks; clip $11.29
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
template: polika72
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 11.287
clip_usdc_p90: 53.32
entry_price_median: 0.4836
entry_price_iqr: (0.3, 0.66)
target_spread: 0.2
target_spread_p75: 0.3137
median_hold_seconds: 66
max_hold_seconds_p75: 112
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

_Generated 2026-08-25T16:46:52.153331+00:00_
