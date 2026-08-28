# Elite Replication Playbook — DrPufferfish

Wallet `0xdb27bf2ac5d428a9c63dbc914611036855a6c56e`. Reverse-engineered from the **full unique fill tape** (64,290 trades · 719 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $4,176,633.54 |
| Core cashflow (ex-rebates) | $4,175,613.54 |
| Closed-position legs sum | $46,297,730.97 |
| Leg win rate / profit factor | 90.22% / 21.0256 |
| Polymarket leaderboard ALL | $4,055,413.26 · vol $248,548,251.18 · rank 30 |
| polymarket_leaderboard_ALL pnl | ref=4055413.259574452 ours=4175613.5447 (MATCH) |
| polydata realized_pnl | ref=4055413.26 ours=4175613.5447 (MATCH) |
| polydata n_trades | ref=272027 ours=64290 (DRIFT) |
| polydata win_rate | ref=0.481 ours=0.9022 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 13 markets · $26,160.57 · avg $2,012.35 · median hold 0s · median spread None
- **Match / other sports:** 579 markets · $10,350,373.08 · avg $17,876.29
- **Outcome PnL leaders:**
  - **No**: $2,117,185.42
  - **Nets**: $925,753.04
  - **Hawks**: $877,997.07
  - **Hornets**: $784,687.13
  - **Grizzlies**: $757,904.27
  - **Yes**: $689,925.66

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_cheap_tail`: 155
- `directional_buy_sub_mid`: 152
- `directional_buy_near_mid`: 144
- `directional_buy_above_mid`: 114
- `directional_buy_expensive_favorite`: 51
- `two_sided_inventory_sub_mid`: 23
- `sell_first_cheap_tail`: 22
- `two_sided_inventory_above_mid`: 19
- `two_sided_inventory_cheap_tail`: 16
- `two_sided_inventory_near_mid`: 14
- `two_sided_inventory_expensive_favorite`: 9

### First-two-fill sequences
- `BUY->BUY`: 547
- `single_fill`: 148
- `SELL->SELL`: 14
- `BUY->SELL`: 10

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 128 | $1,108,823.86 | $8,662.69 |
| 0.20-0.40 | 150 | $4,539,997.13 | $30,266.65 |
| 0.40-0.60 | 266 | $6,532,097.53 | $24,556.76 |
| 0.60-0.80 | 113 | $1,356,925.63 | $12,008.19 |
| 0.80-1.00 | 42 | $144,351.35 | $3,436.94 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$3.20** median (p90 $195.00).
2. Aim entry price ~**0.51** (IQR (0.41, 0.66)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 211
- `multi_hour_position`: 183
- `intraday_swing`: 151
- `scalp_sub_15m`: 130
- `scale_in_scale_out`: 22
- `market_make_both_outcomes`: 22

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 355 | 45 |
| PnL | $14,635,040.94 | -$1,182,385.61 |
| Median hold | 17m40s | 50m16s |
| Median spread | 0.0111 | -0.0035 |
| Scale-in rate | 0.7493 | 0.6222 |
| Scale-out rate | 0.0901 | 0.2889 |
| Avg fills/market | 79.03 | 99.4 |
| Both-sides rate | 0.1803 | 0.3778 |

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

- **Winners** sell above buy (median spread **0.0111**). **Losers** often exit worse (median spread **-0.0035**).
- Losers scale-in **more** (0.6222 vs 0.7493) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 259, 'pnl': 3738937.7727, 'avg': 14436.0532, 'win_rate': 0.5483}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 615
- `mixed_roundtrip`: 36
- `spread_harvest_sell_above_buy`: 35
- `sell_inventory_only`: 20
- `adverse_exit_sell_below_buy`: 13

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 259 | $3,738,937.77 | $14,436.05 | 54.8% |
| 5-30m | 119 | $1,779,547.91 | $14,954.18 | 47.9% |
| 30m-2h | 116 | $1,900,546.04 | $16,384.02 | 49.1% |
| 2-12h | 133 | $4,779,257.21 | $35,934.26 | 52.6% |
| 12h+ | 92 | $1,254,366.40 | $13,634.42 | 31.5% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.0111** above avg entry (p75 stretch 0.0461). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 17m40s; p75 2h18m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.0111 vs losers -0.0035
- Both-sides inventory on 18.0% of winning markets (losers 37.8%)
- Hold bucket <5m: avg PnL $14436.05 on 259 markets (WR 55%)
- Hold bucket 5-30m: avg PnL $14954.18 on 119 markets (WR 48%)
- Hold bucket 30m-2h: avg PnL $16384.02 on 116 markets (WR 49%)
- Hold bucket 2-12h: avg PnL $35934.26 on 133 markets (WR 53%)
- Hold bucket 12h+: avg PnL $13634.42 on 92 markets (WR 32%)
- Entry band 0.00-0.20: avg $8662.69 across 128 markets
- Entry band 0.20-0.40: avg $30266.65 across 150 markets
- Entry band 0.40-0.60: avg $24556.76 across 266 markets
- Entry band 0.60-0.80: avg $12008.19 across 113 markets
- Entry band 0.80-1.00: avg $3436.94 across 42 markets
- Buy-ladder behavior: fade-into-weakness markets=50, chase-up markets=46

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 46, 'fade_down': 50}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Rockets vs. Lakers
PnL $75,885.11 · hold 23h47m · 195B/79S · avg entry 0.5342 → exit 0.56 (spread 0.0258) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-12-25T01:01:33+00:00 | BUY | Rockets | 4095.99 | 0.5499 | 2252.39 |
| 2025-12-25T02:46:41+00:00 | BUY | Rockets | 287.46 | 0.5400 | 155.23 |
| 2025-12-25T02:50:55+00:00 | BUY | Rockets | 89.13 | 0.5400 | 48.13 |
| 2025-12-25T02:51:03+00:00 | BUY | Rockets | 355.24 | 0.5400 | 191.83 |
| 2025-12-25T02:53:53+00:00 | BUY | Rockets | 2.00 | 0.5400 | 1.08 |
| 2025-12-25T03:12:51+00:00 | BUY | Rockets | 1500.00 | 0.5400 | 810.00 |
| 2025-12-25T03:13:21+00:00 | BUY | Rockets | 100.00 | 0.5400 | 54.00 |
| 2025-12-25T03:13:21+00:00 | BUY | Rockets | 400.00 | 0.5400 | 216.00 |
| 2025-12-25T03:18:17+00:00 | BUY | Rockets | 1456.09 | 0.5400 | 786.29 |
| 2025-12-25T03:19:27+00:00 | BUY | Rockets | 3.28 | 0.5400 | 1.77 |
| 2025-12-25T03:19:33+00:00 | BUY | Rockets | 1.89 | 0.5400 | 1.02 |
| 2025-12-25T03:21:07+00:00 | BUY | Rockets | 71.74 | 0.5400 | 38.74 |
| 2025-12-25T03:28:53+00:00 | BUY | Rockets | 2.17 | 0.5400 | 1.17 |
| 2025-12-25T03:33:51+00:00 | BUY | Rockets | 217.39 | 0.5400 | 117.39 |
| 2025-12-25T03:34:23+00:00 | BUY | Rockets | 5.74 | 0.5400 | 3.10 |
| 2025-12-26T00:32:47+00:00 | BUY | Rockets | 1265.89 | 0.5400 | 683.58 |
| 2025-12-26T00:32:47+00:00 | BUY | Rockets | 8.15 | 0.5400 | 4.40 |
| 2025-12-26T00:33:03+00:00 | BUY | Rockets | 217.39 | 0.5400 | 117.39 |
| 2025-12-26T00:33:09+00:00 | BUY | Rockets | 217.39 | 0.5400 | 117.39 |
| 2025-12-26T00:33:37+00:00 | BUY | Rockets | 495.37 | 0.5400 | 267.50 |
| 2025-12-26T00:33:49+00:00 | BUY | Rockets | 30.00 | 0.5400 | 16.20 |
| 2025-12-26T00:40:23+00:00 | BUY | Rockets | 2406.48 | 0.5300 | 1275.43 |
| 2025-12-26T00:41:51+00:00 | BUY | Rockets | 70.00 | 0.5300 | 37.10 |
| 2025-12-26T00:42:01+00:00 | BUY | Rockets | 69.32 | 0.5300 | 36.74 |
| 2025-12-26T00:42:01+00:00 | BUY | Rockets | 11.04 | 0.5300 | 5.85 |
| 2025-12-26T00:42:01+00:00 | BUY | Rockets | 100.00 | 0.5300 | 53.00 |
| 2025-12-26T00:42:29+00:00 | BUY | Rockets | 212.77 | 0.5300 | 112.77 |
| 2025-12-26T00:42:39+00:00 | BUY | Rockets | 182.49 | 0.5300 | 96.72 |
| 2025-12-26T00:42:49+00:00 | BUY | Rockets | 10.00 | 0.5300 | 5.30 |
| 2025-12-26T00:49:15+00:00 | BUY | Rockets | 120270.88 | 0.5300 | 63743.57 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: Chris Eubank Jr. vs Conor Benn Nov 15, 2025
PnL $50,078.27 · hold 37m04s · 12B/7S · avg entry 0.3994 → exit 0.42 (spread 0.0206) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-11-15T21:20:55+00:00 | BUY | Benn | 158.40 | 0.3800 | 60.19 |
| 2025-11-15T21:35:15+00:00 | BUY | Benn | 5.00 | 0.4000 | 2.00 |
| 2025-11-15T21:36:13+00:00 | BUY | Benn | 333.33 | 0.4000 | 133.33 |
| 2025-11-15T21:37:19+00:00 | BUY | Benn | 74987.00 | 0.4000 | 29994.80 |
| 2025-11-15T21:38:05+00:00 | BUY | Benn | 161.29 | 0.3800 | 61.29 |
| 2025-11-15T21:38:15+00:00 | SELL | Benn | 81.44 | 0.4200 | 34.20 |
| 2025-11-15T21:38:59+00:00 | BUY | Benn | 161.29 | 0.3800 | 61.29 |
| 2025-11-15T21:39:55+00:00 | SELL | Benn | 9.90 | 0.4200 | 4.16 |
| 2025-11-15T21:40:33+00:00 | SELL | Benn | 220.00 | 0.4200 | 92.40 |
| 2025-11-15T21:42:29+00:00 | SELL | Benn | 47.62 | 0.4200 | 20.00 |
| 2025-11-15T21:43:35+00:00 | SELL | Benn | 713.90 | 0.4200 | 299.84 |
| 2025-11-15T21:43:43+00:00 | BUY | Benn | 6.45 | 0.3800 | 2.45 |
| 2025-11-15T21:45:01+00:00 | SELL | Benn | 26.29 | 0.4200 | 11.04 |
| 2025-11-15T21:47:19+00:00 | SELL | Benn | 98.00 | 0.4200 | 41.16 |
| 2025-11-15T21:50:15+00:00 | BUY | Benn | 1687.85 | 0.3800 | 641.38 |
| 2025-11-15T21:50:45+00:00 | BUY | Benn | 161.29 | 0.3800 | 61.29 |
| 2025-11-15T21:53:05+00:00 | BUY | Benn | 105.68 | 0.3800 | 40.16 |
| 2025-11-15T21:53:57+00:00 | BUY | Benn | 6670.00 | 0.4000 | 2668.00 |
| 2025-11-15T21:57:59+00:00 | BUY | Benn | 100.00 | 0.3900 | 39.00 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 3: 76ers vs. Grizzlies
PnL $25,958.35 · hold 5h11m · 98B/11S · avg entry 0.491 → exit 0.54 (spread 0.049) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-12-30T19:48:51+00:00 | BUY | 76ers | 191.73 | 0.4900 | 93.95 |
| 2025-12-30T19:52:49+00:00 | BUY | 76ers | 378.05 | 0.4900 | 185.24 |
| 2025-12-30T19:53:01+00:00 | BUY | 76ers | 425.49 | 0.4900 | 208.49 |
| 2025-12-30T19:53:03+00:00 | BUY | 76ers | 2188.24 | 0.4900 | 1072.24 |
| 2025-12-30T19:53:05+00:00 | BUY | 76ers | 431.37 | 0.4900 | 211.37 |
| 2025-12-30T19:53:11+00:00 | BUY | 76ers | 9025.66 | 0.4900 | 4422.57 |
| 2025-12-30T23:57:45+00:00 | BUY | 76ers | 1710.00 | 0.4800 | 820.80 |
| 2025-12-30T23:57:45+00:00 | BUY | 76ers | 442.03 | 0.4800 | 212.17 |
| 2025-12-30T23:57:51+00:00 | BUY | 76ers | 90.00 | 0.4800 | 43.20 |
| 2025-12-30T23:57:55+00:00 | BUY | 76ers | 3.00 | 0.4800 | 1.44 |
| 2025-12-30T23:57:57+00:00 | BUY | 76ers | 2.00 | 0.4800 | 0.96 |
| 2025-12-30T23:58:19+00:00 | BUY | 76ers | 150.00 | 0.4800 | 72.00 |
| 2025-12-30T23:58:43+00:00 | BUY | 76ers | 9.62 | 0.4800 | 4.62 |
| 2025-12-30T23:59:07+00:00 | BUY | 76ers | 9.00 | 0.4800 | 4.32 |
| 2025-12-30T23:59:09+00:00 | BUY | 76ers | 1106.00 | 0.4800 | 530.88 |
| 2025-12-31T00:32:25+00:00 | BUY | 76ers | 10.00 | 0.5000 | 5.00 |
| 2025-12-31T00:32:29+00:00 | BUY | 76ers | 73.00 | 0.5000 | 36.50 |
| 2025-12-31T00:32:33+00:00 | BUY | 76ers | 75.00 | 0.5000 | 37.50 |
| 2025-12-31T00:32:59+00:00 | BUY | 76ers | 10.00 | 0.5000 | 5.00 |
| 2025-12-31T00:35:33+00:00 | SELL | 76ers | 51929.26 | 0.5400 | 28041.80 |
| 2025-12-31T00:46:57+00:00 | SELL | 76ers | 5.56 | 0.5400 | 3.00 |
| 2025-12-31T00:57:43+00:00 | SELL | 76ers | 925.93 | 0.5400 | 500.00 |
| 2025-12-31T00:58:07+00:00 | SELL | 76ers | 7.84 | 0.5400 | 4.23 |
| 2025-12-31T00:58:15+00:00 | SELL | 76ers | 15048.52 | 0.5400 | 8126.20 |
| 2025-12-31T00:58:21+00:00 | SELL | 76ers | 257.41 | 0.5400 | 139.00 |
| 2025-12-31T00:58:27+00:00 | SELL | 76ers | 100.00 | 0.5400 | 54.00 |
| 2025-12-31T00:58:35+00:00 | SELL | 76ers | 8.56 | 0.5400 | 4.62 |
| 2025-12-31T00:59:03+00:00 | SELL | 76ers | 200.00 | 0.5400 | 108.00 |
| 2025-12-31T00:59:17+00:00 | SELL | 76ers | 185.19 | 0.5400 | 100.00 |
| 2025-12-31T00:59:57+00:00 | SELL | 76ers | 2190.00 | 0.5400 | 1182.60 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Pistons vs. Celtics** -$123,412.12 · hold 13h32m · entry 0.5208 → exit 0.47 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
2. **Spread: Pistons (-9.5)** -$108,248.05 · hold 8m26s · entry 0.4763 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
3. **Chiefs vs. Broncos** -$87,922.18 · hold 13m40s · entry 0.6379 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
4. **Spread: Thunder (-11.5)** -$84,368.74 · hold 20m08s · entry 0.4866 → exit 0.48 · `intraday_swing` / `mixed_roundtrip`
5. **Falcons vs. Vikings** -$67,653.93 · hold 30m04s · entry 0.5848 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Eagles vs. Chargers** -$65,540.87 · hold 44m40s · entry 0.507 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
7. **Thunder vs. Jazz** -$39,793.93 · hold 1h06m · entry 0.1848 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
8. **Champions League Final: 3+ goals?** -$32,532.08 · hold 0s · entry 0.43 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
9. **Will the Seattle Mariners win the 2025 World Series?** -$29,671.92 · hold 5d · entry 0.6043 → exit 0.278 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
10. **UFC Fight Night: Muhammad vs. Machado Garry (Welterweight, Main Card)** -$29,143.07 · hold 15h55m · entry 0.2754 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $3.20
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
template: DrPufferfish
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 3.2
clip_usdc_p90: 195.0
entry_price_median: 0.51
entry_price_iqr: (0.41, 0.66)
target_spread: 0.0111
target_spread_p75: 0.0461
median_hold_seconds: 1060
max_hold_seconds_p75: 8328
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

_Generated 2026-08-28T14:18:31.630629+00:00_
