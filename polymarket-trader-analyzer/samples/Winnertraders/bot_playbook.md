# Elite Replication Playbook — Winnertraders

Wallet `0x13464aabec792c36b062316f474713e681330448`. Reverse-engineered from the **full unique fill tape** (20,475 trades · 2,750 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $16,661.90 |
| Core cashflow (ex-rebates) | $16,180.10 |
| Closed-position legs sum | -$844.29 |
| Leg win rate / profit factor | 65.11% / 0.9845 |
| Polymarket leaderboard ALL | $17,578.63 · vol $2,032,708.12 · rank 9024 |
| polymarket_leaderboard_ALL pnl | ref=17578.63221507959 ours=16661.9043 (MATCH) |
| polydata realized_pnl | ref=17655.63 ours=16661.9043 (MATCH) |
| polydata n_trades | ref=16162 ours=20475 (DRIFT) |
| polydata win_rate | ref=0.5926 ours=0.6511 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 1390 markets · $9,410.53 · avg $6.77 · median hold 17m40s · median spread 0.09
- **Match / other sports:** 1078 markets · -$11,987.46 · avg -$11.12
- **Outcome PnL leaders:**
  - **Under**: $5,390.02
  - **Over**: $3,969.85
  - **New Zealand**: $2,364.86
  - **Punjab Kings**: $599.27
  - **Sport Lisboa e Benfica**: $585.90
  - **Netherlands**: $524.74

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_cheap_tail`: 746
- `directional_buy_sub_mid`: 577
- `directional_buy_above_mid`: 512
- `directional_buy_near_mid`: 332
- `directional_buy_expensive_favorite`: 329
- `two_sided_inventory_cheap_tail`: 86
- `two_sided_inventory_sub_mid`: 51
- `two_sided_inventory_above_mid`: 49
- `two_sided_inventory_near_mid`: 43
- `two_sided_inventory_expensive_favorite`: 25

### First-two-fill sequences
- `BUY->BUY`: 1547
- `BUY->SELL`: 1110
- `single_fill`: 93

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 748 | -$2,672.31 | -$3.57 |
| 0.20-0.40 | 671 | -$2,758.27 | -$4.11 |
| 0.40-0.60 | 639 | $1,638.26 | $2.56 |
| 0.60-0.80 | 465 | $117.08 | $0.25 |
| 0.80-1.00 | 227 | $2,830.94 | $12.47 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$8.51** median (p90 $73.95).
2. Aim entry price ~**0.45** (IQR (0.22, 0.65)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `intraday_swing`: 737
- `single_clip`: 669
- `scalp_sub_15m`: 546
- `scale_in_scale_out`: 382
- `market_make_both_outcomes`: 245
- `multi_hour_position`: 171

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 1785 | 960 |
| PnL | $50,301.01 | -$51,145.30 |
| Median hold | 24m41s | 25m14s |
| Median spread | 0.1 | -0.0484 |
| Scale-in rate | 0.558 | 0.7208 |
| Scale-out rate | 0.5697 | 0.4146 |
| Avg fills/market | 7.06 | 8.18 |
| Both-sides rate | 0.1025 | 0.074 |

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

- **Winners** sell above buy (median spread **0.1**). **Losers** often exit worse (median spread **-0.0484**).
- Losers scale-in **more** (0.7208 vs 0.558) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 498, 'pnl': 716.6684, 'avg': 1.4391, 'win_rate': 0.512}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `spread_harvest_sell_above_buy`: 1824
- `adverse_exit_sell_below_buy`: 500
- `hold_to_resolution_or_redeem`: 281
- `mixed_roundtrip`: 145

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 498 | $716.67 | $1.44 | 51.2% |
| 5-30m | 1007 | $5,305.61 | $5.27 | 73.0% |
| 30m-2h | 777 | -$4,167.19 | -$5.36 | 62.4% |
| 2-12h | 387 | -$5,456.08 | -$14.10 | 63.6% |
| 12h+ | 81 | $2,756.70 | $34.03 | 79.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.1** above avg entry (p75 stretch 0.1971). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 24m41s; p75 1h14m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.1 vs losers -0.0484
- Both-sides inventory on 10.2% of winning markets (losers 7.4%)
- Hold bucket 5-30m: avg PnL $5.27 on 1007 markets (WR 73%)
- Hold bucket 12h+: avg PnL $34.03 on 81 markets (WR 79%)
- Entry band 0.80-1.00: avg $12.47 across 227 markets
- Buy-ladder behavior: fade-into-weakness markets=677, chase-up markets=225

### Fails
- Hold bucket 30m-2h: avg PnL $-5.36 on 777 markets
- Hold bucket 2-12h: avg PnL $-14.10 on 387 markets
- Chase vs fade ladders: `{'chase_up': 225, 'fade_down': 677}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Mavericks vs. Bucks: O/U 218.5
PnL $2,507.61 · hold 11h46m · 14B/3S · avg entry 0.0945 → exit 0.4845 (spread 0.39) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-02-12T04:47:41+00:00 | BUY | Over | 935.00 | 0.2130 | 199.16 |
| 2026-02-12T07:11:17+00:00 | BUY | Over | 200.00 | 0.1020 | 20.40 |
| 2026-02-12T07:11:39+00:00 | BUY | Over | 1892.50 | 0.1030 | 194.93 |
| 2026-02-12T07:25:05+00:00 | BUY | Over | 2000.00 | 0.0510 | 101.98 |
| 2026-02-12T07:25:39+00:00 | BUY | Over | 1083.83 | 0.0510 | 55.28 |
| 2026-02-12T08:39:51+00:00 | BUY | Over | 30.00 | 0.1192 | 3.58 |
| 2026-02-12T08:40:27+00:00 | BUY | Over | 5.00 | 0.1000 | 0.50 |
| 2026-02-12T08:50:55+00:00 | BUY | Over | 10.00 | 0.1355 | 1.35 |
| 2026-02-12T09:08:27+00:00 | BUY | Over | 87.00 | 0.1290 | 11.22 |
| 2026-02-12T09:10:09+00:00 | BUY | Over | 68.54 | 0.1044 | 7.16 |
| 2026-02-12T09:18:29+00:00 | BUY | Over | 20.50 | 0.1150 | 2.36 |
| 2026-02-12T09:31:43+00:00 | BUY | Over | 49.20 | 0.1020 | 5.02 |
| 2026-02-12T10:02:45+00:00 | BUY | Over | 19.80 | 0.1070 | 2.12 |
| 2026-02-12T10:06:25+00:00 | BUY | Over | 28.45 | 0.1000 | 2.85 |
| 2026-02-12T15:43:09+00:00 | SELL | Over | 20.82 | 0.3100 | 6.45 |
| 2026-02-12T16:34:31+00:00 | SELL | Over | 1409.00 | 0.3790 | 534.01 |
| 2026-02-12T16:34:31+00:00 | SELL | Over | 5000.00 | 0.5150 | 2575.00 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: ODI Series New Zealand vs South Africa Women: New Zealand vs South Africa
PnL $551.84 · hold 6h42m · 19B/10S · avg entry 0.1898 → exit 0.2497 (spread 0.0599) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-03-31T22:21:25+00:00 | BUY | New Zealand | 100.00 | 0.5600 | 56.00 |
| 2026-03-31T22:26:11+00:00 | BUY | New Zealand | 100.00 | 0.5500 | 55.00 |
| 2026-03-31T22:38:01+00:00 | SELL | New Zealand | 197.33 | 0.6200 | 122.34 |
| 2026-03-31T23:34:51+00:00 | BUY | New Zealand | 200.00 | 0.4100 | 82.00 |
| 2026-03-31T23:56:35+00:00 | BUY | New Zealand | 250.00 | 0.2100 | 52.50 |
| 2026-04-01T01:20:45+00:00 | BUY | New Zealand | 29.00 | 0.1100 | 3.19 |
| 2026-04-01T01:20:53+00:00 | BUY | New Zealand | 29.00 | 0.1100 | 3.19 |
| 2026-04-01T01:21:59+00:00 | BUY | New Zealand | 30.00 | 0.1100 | 3.30 |
| 2026-04-01T01:28:55+00:00 | BUY | New Zealand | 28.00 | 0.1100 | 3.08 |
| 2026-04-01T01:44:19+00:00 | BUY | New Zealand | 12.00 | 0.1100 | 1.32 |
| 2026-04-01T01:44:29+00:00 | BUY | New Zealand | 16.00 | 0.1100 | 1.76 |
| 2026-04-01T01:44:33+00:00 | BUY | New Zealand | 18.00 | 0.1100 | 1.98 |
| 2026-04-01T02:07:35+00:00 | BUY | New Zealand | 190.00 | 0.1100 | 20.90 |
| 2026-04-01T02:26:19+00:00 | BUY | New Zealand | 103.17 | 0.0900 | 9.29 |
| 2026-04-01T03:17:49+00:00 | BUY | New Zealand | 286.00 | 0.0800 | 22.88 |
| 2026-04-01T03:22:35+00:00 | BUY | New Zealand | 50.00 | 0.0700 | 3.50 |
| 2026-04-01T03:27:41+00:00 | BUY | New Zealand | 176.94 | 0.0600 | 10.62 |
| 2026-04-01T03:37:15+00:00 | BUY | New Zealand | 100.00 | 0.0400 | 4.00 |
| 2026-04-01T03:39:21+00:00 | BUY | New Zealand | 50.00 | 0.0400 | 2.00 |
| 2026-04-01T04:04:49+00:00 | SELL | New Zealand | 940.89 | 0.1010 | 95.06 |
| 2026-04-01T04:08:29+00:00 | SELL | New Zealand | 100.00 | 0.1600 | 16.00 |
| 2026-04-01T04:09:03+00:00 | SELL | New Zealand | 100.00 | 0.1900 | 19.00 |
| 2026-04-01T04:16:55+00:00 | SELL | New Zealand | 100.00 | 0.2400 | 24.00 |
| 2026-04-01T04:21:19+00:00 | SELL | New Zealand | 100.00 | 0.4100 | 41.00 |
| 2026-04-01T04:23:35+00:00 | SELL | New Zealand | 50.00 | 0.5500 | 27.50 |
| 2026-04-01T04:24:55+00:00 | SELL | New Zealand | 50.00 | 0.5700 | 28.50 |
| 2026-04-01T04:39:49+00:00 | SELL | New Zealand | 100.00 | 0.4800 | 48.00 |
| 2026-04-01T04:56:45+00:00 | BUY | New Zealand | 50.00 | 0.1711 | 8.55 |
| 2026-04-01T05:03:33+00:00 | SELL | New Zealand | 48.76 | 0.5100 | 24.87 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: Switzerland vs. Colombia: O/U 8.5 Total Corners
PnL $448.30 · hold 5m55s · 2B/2S · avg entry 0.3586 → exit 0.999 (spread 0.6404) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-07T21:58:34+00:00 | BUY | Under | 200.00 | 0.7300 | 146.00 |
| 2026-07-07T21:58:34+00:00 | BUY | Under | 500.00 | 0.2100 | 105.00 |
| 2026-07-07T22:03:43+00:00 | SELL | Under | 90.09 | 0.9990 | 90.00 |
| 2026-07-07T22:04:29+00:00 | SELL | Under | 609.90 | 0.9990 | 609.29 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 4: Argentina vs. Cabo Verde: O/U 7.5 Total Corners
PnL $319.97 · hold 14m02s · 4B/9S · avg entry 0.3364 → exit 0.94 (spread 0.6036) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-03T23:45:05+00:00 | BUY | Under | 296.13 | 0.3500 | 103.65 |
| 2026-07-03T23:47:32+00:00 | BUY | Under | 149.25 | 0.3500 | 52.24 |
| 2026-07-03T23:47:34+00:00 | BUY | Under | 54.62 | 0.3500 | 19.12 |
| 2026-07-03T23:48:26+00:00 | BUY | Under | 30.08 | 0.1100 | 3.31 |
| 2026-07-03T23:58:35+00:00 | SELL | Under | 29.11 | 0.9400 | 27.36 |
| 2026-07-03T23:59:04+00:00 | SELL | Under | 10.64 | 0.9400 | 10.00 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 17.44 | 0.9400 | 16.39 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:05+00:00 | SELL | Under | 26.04 | 0.9400 | 24.48 |
| 2026-07-03T23:59:07+00:00 | SELL | Under | 342.68 | 0.9400 | 322.12 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 5: France vs. England: 1st Half O/U 4.5 Total Corners
PnL $281.86 · hold 6m34s · 3B/3S · avg entry 0.0977 → exit 0.49 (spread 0.3923) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-18T21:27:06+00:00 | BUY | Under | 100.00 | 0.3944 | 39.44 |
| 2026-07-18T21:29:24+00:00 | BUY | Under | 4.59 | 0.0500 | 0.23 |
| 2026-07-18T21:30:24+00:00 | BUY | Under | 617.00 | 0.0500 | 30.85 |
| 2026-07-18T21:32:52+00:00 | SELL | Under | 200.00 | 0.4900 | 98.00 |
| 2026-07-18T21:33:21+00:00 | SELL | Under | 94.96 | 0.4900 | 46.53 |
| 2026-07-18T21:33:40+00:00 | SELL | Under | 426.62 | 0.4900 | 209.04 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 6: United States vs. Belgium: O/U 11.5 Total Corners
PnL $223.86 · hold 3m35s · 1B/3S · avg entry 0.21 → exit 0.6577 (spread 0.4477) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-07-07T00:04:53+00:00 | BUY | Under | 500.00 | 0.2100 | 105.00 |
| 2026-07-07T00:06:32+00:00 | SELL | Under | 16.34 | 0.5900 | 9.64 |
| 2026-07-07T00:08:08+00:00 | SELL | Under | 59.30 | 0.6600 | 39.14 |
| 2026-07-07T00:08:28+00:00 | SELL | Under | 424.35 | 0.6600 | 280.07 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Indian Premier League: Kolkata Knight Riders vs Sunrisers Hyderabad** -$2,394.22 · hold 3h20m · entry 0.0644 → exit 0.1802 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
2. **Pakistan Super League: Peshawar Zalmi vs Multan Sultans** -$2,176.10 · hold 55m56s · entry 0.3853 → exit 0.4766 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
3. **T20 Series Namibia vs Scotland: Namibia vs Scotland** -$1,272.23 · hold 21h36m · entry 0.0832 → exit 0.0294 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
4. **Indian Premier League: Mumbai Indians vs Lucknow Super Giants** -$1,268.29 · hold 2h28m · entry 0.1078 → exit 0.0499 · `scale_in_scale_out` / `adverse_exit_sell_below_buy`
5. **T20 Challenge Trophy, Women: Rwanda vs Nepal** -$1,267.38 · hold 5h30m · entry 0.0122 → exit 0.0744 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
6. **T20 Series Indonesia vs Sweden: Indonesia vs Sweden** -$1,100.42 · hold 4h56m · entry 0.0583 → exit 0.2307 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
7. **Indian Premier League: Chennai Super Kings vs Delhi Capitals** -$881.33 · hold 4h08m · entry 0.105 → exit 0.3447 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
8. **T20 Series Bangladesh vs Sri Lanka, Women: Bangladesh vs Sri Lanka** -$846.30 · hold 1h21m · entry 0.0077 → exit 0.0304 · `scale_in_scale_out` / `spread_harvest_sell_above_buy`
9. **Indian Premier League: Chennai Super Kings vs Kolkata Knight Riders** -$815.00 · hold 4h08m · entry 0.1135 → exit 0.1301 · `market_make_both_outcomes` / `spread_harvest_sell_above_buy`
10. **T20 Series South Africa vs. India, Women: South Africa vs India** -$729.97 · hold 1h33m · entry 0.1578 → exit 0.06 · `intraday_swing` / `adverse_exit_sell_below_buy`

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
   - default post-only bids/asks; clip $8.51
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
template: Winnertraders
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 8.5113
clip_usdc_p90: 73.95
entry_price_median: 0.45
entry_price_iqr: (0.22, 0.65)
target_spread: 0.1
target_spread_p75: 0.1971
median_hold_seconds: 1481
max_hold_seconds_p75: 4461
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

_Generated 2026-08-25T21:55:36.206664+00:00_
