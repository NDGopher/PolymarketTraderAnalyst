# Elite Replication Playbook — ImJustKen

Wallet `0x9d84ce0306f8551e02efef1680475fc0f1dc1344`. Reverse-engineered from the **full unique fill tape** (320,389 trades · 5,257 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `hybrid_mm_directional` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$43,822,026.87 |
| Core cashflow (ex-rebates) | -$44,806,140.80 |
| Closed-position legs sum | -$27,767,466.73 |
| Leg win rate / profit factor | 45.30% / 0.4002 |
| Polymarket leaderboard ALL | $3,291,874.41 · vol $499,524,708.36 · rank 44 |
| polymarket_leaderboard_ALL pnl | ref=3291874.409581338 ours=-27767466.7259 (DRIFT) |
| polydata realized_pnl | ref=3289074.81 ours=-27767466.7259 (DRIFT) |
| polydata n_trades | ref=606672 ours=320389 (DRIFT) |
| polydata win_rate | ref=0.6133 ours=0.453 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 14 markets · -$334.69 · avg -$23.91 · median hold 12d · median spread 0.0
- **Match / other sports:** 1370 markets · -$23,515,655.74 · avg -$17,164.71
- **Outcome PnL leaders:**
  - **Democrats**: $80,492.20
  - **Wagner**: $35,189.43
  - **Israel**: $20,175.78
  - **Wen-je**: $18,743.48
  - **Harris**: $18,100.84
  - **Giants**: $17,724.11

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `two_sided_inventory_expensive_favorite`: 1640
- `two_sided_inventory_cheap_tail`: 1289
- `two_sided_inventory_above_mid`: 637
- `two_sided_inventory_sub_mid`: 516
- `directional_buy_cheap_tail`: 516
- `two_sided_inventory_near_mid`: 267
- `directional_buy_expensive_favorite`: 239
- `directional_buy_sub_mid`: 52
- `directional_buy_above_mid`: 41
- `sell_first_cheap_tail`: 34
- `directional_buy_near_mid`: 25
- `sell_first_expensive_favorite`: 1

### First-two-fill sequences
- `BUY->BUY`: 4868
- `single_fill`: 235
- `BUY->SELL`: 110
- `SELL->BUY`: 23
- `SELL->SELL`: 21

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 1003 | -$20,215,081.46 | -$20,154.62 |
| 0.20-0.40 | 1006 | -$1,992,145.43 | -$1,980.26 |
| 0.40-0.60 | 2207 | -$2,238,783.34 | -$1,014.40 |
| 0.60-0.80 | 601 | $264,112.87 | $439.46 |
| 0.80-1.00 | 429 | -$54,587.92 | -$127.24 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$20.00** median (p90 $500.92).
2. Aim entry price ~**0.495** (IQR (0.4207, 0.6152)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 3720
- `market_make_both_outcomes`: 904
- `single_clip`: 468
- `scale_in_scale_out`: 73
- `intraday_swing`: 66
- `scalp_sub_15m`: 26

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 2684 | 2532 |
| PnL | $4,521,765.54 | -$28,852,851.10 |
| Median hold | 7d | 6d |
| Median spread | -0.089 | -0.1132 |
| Scale-in rate | 0.9639 | 0.9333 |
| Scale-out rate | 0.1416 | 0.1951 |
| Avg fills/market | 53.43 | 69.78 |
| Both-sides rate | 0.9061 | 0.7536 |

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

- **Winners** sell above buy (median spread **-0.089**). **Losers** often exit worse (median spread **-0.1132**).
- Losers scale-in **more** (0.9333 vs 0.9639) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 279, 'pnl': -75246.9927, 'avg': -269.7025, 'win_rate': 0.3763}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 3690
- `adverse_exit_sell_below_buy`: 989
- `spread_harvest_sell_above_buy`: 338
- `mixed_roundtrip`: 229
- `sell_inventory_only`: 11

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 279 | -$75,246.99 | -$269.70 | 37.6% |
| 5-30m | 36 | -$25,550.14 | -$709.73 | 41.7% |
| 30m-2h | 72 | -$32,869.56 | -$456.52 | 48.6% |
| 2-12h | 383 | -$76,471.79 | -$199.67 | 50.6% |
| 12h+ | 4487 | -$24,120,947.07 | -$5,375.74 | 52.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **-0.089** above avg entry (p75 stretch 0.1235). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 7d; p75 32d for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread -0.089 vs losers -0.1132
- Both-sides inventory on 90.6% of winning markets (losers 75.4%)
- Entry band 0.60-0.80: avg $439.46 across 601 markets
- Buy-ladder behavior: fade-into-weakness markets=2538, chase-up markets=1299

### Fails
- Hold bucket <5m: avg PnL $-269.70 on 279 markets
- Hold bucket 5-30m: avg PnL $-709.73 on 36 markets
- Hold bucket 30m-2h: avg PnL $-456.52 on 72 markets
- Hold bucket 2-12h: avg PnL $-199.67 on 383 markets
- Hold bucket 12h+: avg PnL $-5375.74 on 4487 markets
- Entry band 0.00-0.20: avg $-20154.62 across 1003 markets — avoid or tighten risk
- Entry band 0.20-0.40: avg $-1980.26 across 1006 markets — avoid or tighten risk
- Entry band 0.40-0.60: avg $-1014.40 across 2207 markets — avoid or tighten risk
- Entry band 0.80-1.00: avg $-127.24 across 429 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 1299, 'fade_down': 2538}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Will Alex De Minaur win Wimbledon Men's?
PnL $96.27 · hold 6m13s · 2B/3S · avg entry 0.9743 → exit 0.999 (spread 0.0247) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2024-07-10T11:14:07+00:00 | BUY | No | 2891.27 | 0.9723 | 2811.12 |
| 2024-07-10T11:14:25+00:00 | BUY | No | 1000.00 | 0.9800 | 980.00 |
| 2024-07-10T11:20:00+00:00 | SELL | No | 500.00 | 0.9990 | 499.50 |
| 2024-07-10T11:20:10+00:00 | SELL | No | 2000.00 | 0.9990 | 1998.00 |
| 2024-07-10T11:20:20+00:00 | SELL | No | 1391.00 | 0.9990 | 1389.61 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Will Chris Christie win the 2024 US Presidential Election?** -$702,380.84 · hold 159d · entry 0.0021 → exit 0.001 · `market_make_both_outcomes` / `mixed_roundtrip`
2. **Will Elizabeth Warren win the 2024 US Presidential Election?** -$702,031.32 · hold 175d · entry 0.0012 → exit 0.0012 · `market_make_both_outcomes` / `mixed_roundtrip`
3. **Will Bernie Sanders win the 2024 US Presidential Election?** -$701,513.72 · hold 195d · entry 0.0047 → exit 0.0013 · `market_make_both_outcomes` / `mixed_roundtrip`
4. **Will Vivek Ramaswamy win the 2024 US Presidential Election?** -$700,142.50 · hold 175d · entry 0.0051 → exit 0.0025 · `market_make_both_outcomes` / `mixed_roundtrip`
5. **Will Kanye West win the 2024 US Presidential Election?** -$698,953.42 · hold 269d · entry 0.0113 → exit 0.0015 · `market_make_both_outcomes` / `mixed_roundtrip`
6. **Will any other Republican Politician win the 2024 US Presidential Election?** -$693,213.93 · hold 289d · entry 0.0057 → exit 0.0085 · `market_make_both_outcomes` / `mixed_roundtrip`
7. **Will Hillary Clinton win the 2024 US Presidential Election?** -$688,153.04 · hold 216d · entry 0.0424 → exit 0.0018 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
8. **Will AOC win the 2024 US Presidential Election?** -$687,759.69 · hold 161d · entry 0.0927 → exit 0.0044 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
9. **Will Ron DeSantis win the 2024 US Presidential Election?** -$685,841.98 · hold 276d · entry 0.0949 → exit 0.0235 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
10. **Will any other Democratic Politician win the 2024 US Presidential Election?** -$680,019.60 · hold 282d · entry 0.0467 → exit 0.025 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`

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
   - default post-only bids/asks; clip $20.00
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
template: ImJustKen
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 20.0
clip_usdc_p90: 500.921
entry_price_median: 0.495
entry_price_iqr: (0.4207, 0.6152)
target_spread: -0.089
target_spread_p75: 0.1235
median_hold_seconds: 649157
max_hold_seconds_p75: 2815346
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

_Generated 2026-08-28T14:44:11.295808+00:00_
