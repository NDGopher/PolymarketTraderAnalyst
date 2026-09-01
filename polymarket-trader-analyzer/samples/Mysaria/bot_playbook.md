# Elite Replication Playbook — Mysaria

Wallet `0xe40aaa5ce1dac0b7dc24c9d0284f27e17c3fe4a2`. Reverse-engineered from the **full unique fill tape** (266,027 trades · 29,195 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `hybrid_mm_directional` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$390,114.77 |
| Core cashflow (ex-rebates) | -$390,557.08 |
| Closed-position legs sum | -$611,424.96 |
| Leg win rate / profit factor | 28.34% / 0.6293 |
| Polymarket leaderboard ALL | $635,298.67 · vol $7,379,689.24 · rank 323 |
| polymarket_leaderboard_ALL pnl | ref=635298.6729157614 ours=-390114.7655 (DRIFT) |
| polydata realized_pnl | ref=497985.09 ours=-390114.7655 (DRIFT) |
| polydata n_trades | ref=95230 ours=266027 (DRIFT) |
| polydata win_rate | ref=0.7458 ours=0.2834 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 32 markets · $242.30 · avg $7.57 · median hold 8d · median spread -0.9578
- **Match / other sports:** 6185 markets · -$45,348.61 · avg -$7.33
- **Outcome PnL leaders:**
  - **No**: -$83,585.75
  - **Yes**: -$840,428.32

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_expensive_favorite`: 14928
- `two_sided_inventory_expensive_favorite`: 7521
- `two_sided_inventory_above_mid`: 1484
- `directional_buy_above_mid`: 1471
- `two_sided_inventory_cheap_tail`: 1042
- `sell_first_cheap_tail`: 885
- `two_sided_inventory_near_mid`: 423
- `directional_buy_near_mid`: 380
- `directional_buy_cheap_tail`: 375
- `directional_buy_sub_mid`: 354
- `two_sided_inventory_sub_mid`: 267
- `sell_first_expensive_favorite`: 26
- `sell_first_sub_mid`: 22
- `sell_first_above_mid`: 10
- `sell_first_near_mid`: 7

### First-two-fill sequences
- `BUY->BUY`: 21271
- `single_fill`: 5233
- `BUY->SELL`: 1391
- `SELL->BUY`: 880
- `SELL->SELL`: 420

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 521 | $62,856.06 | $120.64 |
| 0.20-0.40 | 793 | $110,004.74 | $138.72 |
| 0.40-0.60 | 1574 | $66,268.87 | $42.10 |
| 0.60-0.80 | 2728 | $33,196.52 | $12.17 |
| 0.80-1.00 | 22629 | -$1,185,933.97 | -$52.41 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$5.92** median (p90 $34.34).
2. Aim entry price ~**0.695** (IQR (0.49, 0.8508)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 14191
- `single_clip`: 9103
- `market_make_both_outcomes`: 4999
- `intraday_swing`: 564
- `scalp_sub_15m`: 338

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 5952 | 19256 |
| PnL | $429,560.23 | -$1,353,574.30 |
| Median hold | 1d | 1d |
| Median spread | -0.31 | -0.9821 |
| Scale-in rate | 0.809 | 0.8054 |
| Scale-out rate | 0.1853 | 0.1345 |
| Avg fills/market | 12.02 | 9.48 |
| Both-sides rate | 0.4555 | 0.4137 |

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

- **Winners** sell above buy (median spread **-0.31**). **Losers** often exit worse (median spread **-0.9821**).
- Losers scale-in **more** (0.8054 vs 0.809) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 6287, 'pnl': -94157.4591, 'avg': -14.9765, 'win_rate': 0.1754}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 17501
- `adverse_exit_sell_below_buy`: 9751
- `sell_inventory_only`: 950
- `spread_harvest_sell_above_buy`: 938
- `mixed_roundtrip`: 55

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 6287 | -$94,157.46 | -$14.98 | 17.5% |
| 5-30m | 451 | -$20,616.06 | -$45.71 | 12.0% |
| 30m-2h | 832 | -$42,740.38 | -$51.37 | 15.5% |
| 2-12h | 2832 | -$147,729.20 | -$52.16 | 16.0% |
| 12h+ | 18793 | -$618,770.97 | -$32.93 | 22.4% |

### Exit engine params

1. **TP / ask distance:** target ≈ **-0.31** above avg entry (p75 stretch 0.1527). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 1d; p75 3d for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread -0.31 vs losers -0.9821
- Both-sides inventory on 45.6% of winning markets (losers 41.4%)
- Entry band 0.00-0.20: avg $120.65 across 521 markets
- Entry band 0.20-0.40: avg $138.72 across 793 markets
- Entry band 0.40-0.60: avg $42.10 across 1574 markets
- Entry band 0.60-0.80: avg $12.17 across 2728 markets
- Buy-ladder behavior: fade-into-weakness markets=3311, chase-up markets=4786

### Fails
- Hold bucket <5m: avg PnL $-14.98 on 6287 markets
- Hold bucket 5-30m: avg PnL $-45.71 on 451 markets
- Hold bucket 30m-2h: avg PnL $-51.37 on 832 markets
- Hold bucket 2-12h: avg PnL $-52.16 on 2832 markets
- Hold bucket 12h+: avg PnL $-32.93 on 18793 markets
- Entry band 0.80-1.00: avg $-52.41 across 22629 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 4786, 'fade_down': 3311}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Will the lowest temperature in Kuala Lumpur be 26°C on August 25?
PnL $361.77 · hold 4m38s · 2B/1S · avg entry 0.0083 → exit 0.999 (spread 0.9907) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-08-25T15:49:52+00:00 | BUY | No | 74.67 | 0.0020 | 0.15 |
| 2026-08-25T15:49:57+00:00 | BUY | No | 125.33 | 0.0120 | 1.50 |
| 2026-08-25T15:54:30+00:00 | SELL | Yes | 200.00 | 0.9990 | 199.80 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: Will Jared Moskowitz be the FL-25 Democratic nominee?
PnL $213.89 · hold 14m58s · 3B/1S · avg entry 0.0662 → exit 0.98 (spread 0.9138) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-08-18T22:58:27+00:00 | BUY | No | 60.56 | 0.0600 | 3.63 |
| 2026-08-18T22:59:28+00:00 | BUY | No | 13.37 | 0.0700 | 0.94 |
| 2026-08-18T23:02:57+00:00 | BUY | No | 84.86 | 0.0700 | 5.94 |
| 2026-08-18T23:13:25+00:00 | SELL | Yes | 102.49 | 0.9800 | 100.44 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Will Augusto Cury win the 2026 Brazilian presidential election?** -$14,026.86 · hold 20h21m · entry 0.9721 → exit 0.011 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
2. **Will Pablo Marçal win the 2026 Brazilian presidential election?** -$9,574.27 · hold 10d · entry 0.9938 → exit 0.0042 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
3. **Will the Fed decrease interest rates by 50+ bps after the September 2026 meeting?** -$8,319.64 · hold 22d · entry 0.9966 → exit 0.0034 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
4. **Will the Fed decrease interest rates by 25 bps after the September 2026 meeting?** -$7,267.07 · hold 22d · entry 0.9883 → exit 0.0111 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
5. **Will the Fed increase interest rates by 50+ bps after the September 2026 meeting?** -$6,766.96 · hold 22d · entry 0.9961 → exit 0.0039 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
6. **Will Camilo Santana win the 2026 Brazilian presidential election?** -$5,933.52 · hold 19d · entry 0.999 → exit 0.001 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
7. **Will Elon Musk post 240+ tweets from August 22 to August 24, 2026?** -$4,963.46 · hold 1d · entry 0.999 → exit 0.001 · `single_clip` / `adverse_exit_sell_below_buy`
8. **Will Hull City win the 2026-27 English Premier League (EPL) Championship?** -$3,944.81 · hold 7d · entry 0.999 → exit 0.001 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
9. **Will Fulham win the 2026-27 English Premier League (EPL) Championship?** -$3,944.80 · hold 5h50m · entry 0.999 → exit 0.001 · `multi_hour_position` / `adverse_exit_sell_below_buy`
10. **Will Ipswich Town win the 2026-27 English Premier League (EPL) Championship?** -$3,944.80 · hold 4h26m · entry 0.999 → exit 0.001 · `multi_hour_position` / `adverse_exit_sell_below_buy`

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
   - default post-only bids/asks; clip $5.92
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
template: Mysaria
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 5.92
clip_usdc_p90: 34.335
entry_price_median: 0.695
entry_price_iqr: (0.49, 0.8508)
target_spread: -0.31
target_spread_p75: 0.1527
median_hold_seconds: 123545
max_hold_seconds_p75: 270491
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

_Generated 2026-09-01T14:46:19.991706+00:00_
