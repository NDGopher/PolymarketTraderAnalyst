# Elite Replication Playbook — sovereign2013

Wallet `0xee613b3fc183ee44f9da9c05f53e2da107e3debf`. Reverse-engineered from the **full unique fill tape** (119,316 trades · 8,938 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$4,392,612.28 |
| Core cashflow (ex-rebates) | -$4,392,657.34 |
| Closed-position legs sum | $2,198,738.71 |
| Leg win rate / profit factor | 51.15% / 1.0414 |
| Polymarket leaderboard ALL | $3,588,720.22 · vol $402,071,822.94 · rank 38 |
| polymarket_leaderboard_ALL pnl | ref=3588720.2180176293 ours=2198738.7126 (DRIFT) |
| polydata realized_pnl | ref=3588720.22 ours=2198738.7126 (DRIFT) |
| polydata n_trades | ref=1047862 ours=119316 (DRIFT) |
| polydata win_rate | ref=0.5174 ours=0.5115 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 3875 markets · $114,731.37 · avg $29.61 · median hold 5h23m · median spread None
- **Match / other sports:** 2481 markets · $271,017.02 · avg $109.24
- **Outcome PnL leaders:**
  - **Under**: $264,084.62
  - **Tulane**: $152,581.26
  - **Lakers**: $150,762.22
  - **Utah State Aggies**: $113,758.17
  - **Hawks**: $107,209.88
  - **Trail Blazers**: $88,784.33

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `two_sided_inventory_near_mid`: 3514
- `directional_buy_near_mid`: 2134
- `two_sided_inventory_sub_mid`: 949
- `two_sided_inventory_above_mid`: 643
- `directional_buy_sub_mid`: 635
- `directional_buy_above_mid`: 425
- `two_sided_inventory_expensive_favorite`: 230
- `two_sided_inventory_cheap_tail`: 180
- `directional_buy_expensive_favorite`: 144
- `directional_buy_cheap_tail`: 84

### First-two-fill sequences
- `BUY->BUY`: 7346
- `single_fill`: 1586
- `BUY->SELL`: 6

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 79 | -$25,220.90 | -$319.25 |
| 0.20-0.40 | 425 | $159,738.19 | $375.85 |
| 0.40-0.60 | 7856 | $133,122.56 | $16.95 |
| 0.60-0.80 | 434 | $100,054.11 | $230.54 |
| 0.80-1.00 | 144 | $24,477.71 | $169.98 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$20.31** median (p90 $634.25).
2. Aim entry price ~**0.4981** (IQR (0.4798, 0.53)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 5405
- `single_clip`: 2651
- `intraday_swing`: 691
- `scalp_sub_15m`: 189
- `market_make_both_outcomes`: 2

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 4614 | 4322 |
| PnL | $7,594,109.26 | -$7,201,937.58 |
| Median hold | 5h46m | 6h06m |
| Median spread | -0.0037 | -0.01 |
| Scale-in rate | 0.821 | 0.8232 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 13.43 | 13.27 |
| Both-sides rate | 0.6131 | 0.6215 |

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

- **Winners** sell above buy (median spread **-0.0037**). **Losers** often exit worse (median spread **-0.01**).
- Losers scale-in **more** (0.8232 vs 0.821) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 1868, 'pnl': 17732.7304, 'avg': 9.4929, 'win_rate': 0.5203}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 8929
- `adverse_exit_sell_below_buy`: 4
- `mixed_roundtrip`: 4
- `spread_harvest_sell_above_buy`: 1

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 1868 | $17,732.73 | $9.49 | 52.0% |
| 5-30m | 408 | -$63,068.61 | -$154.58 | 48.0% |
| 30m-2h | 807 | -$38,579.83 | -$47.81 | 52.9% |
| 2-12h | 3155 | $557,479.86 | $176.70 | 52.0% |
| 12h+ | 2700 | -$81,392.48 | -$30.15 | 51.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **-0.0037** above avg entry (p75 stretch 0.0706). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 5h46m; p75 13h54m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread -0.0037 vs losers -0.01
- Both-sides inventory on 61.3% of winning markets (losers 62.2%)
- Hold bucket <5m: avg PnL $9.49 on 1868 markets (WR 52%)
- Hold bucket 2-12h: avg PnL $176.70 on 3155 markets (WR 52%)
- Entry band 0.20-0.40: avg $375.85 across 425 markets
- Entry band 0.40-0.60: avg $16.95 across 7856 markets
- Entry band 0.60-0.80: avg $230.54 across 434 markets
- Entry band 0.80-1.00: avg $169.98 across 144 markets
- Buy-ladder behavior: fade-into-weakness markets=1727, chase-up markets=1672

### Fails
- Hold bucket 5-30m: avg PnL $-154.58 on 408 markets
- Hold bucket 30m-2h: avg PnL $-47.81 on 807 markets
- Hold bucket 12h+: avg PnL $-30.15 on 2700 markets
- Entry band 0.00-0.20: avg $-319.25 across 79 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 1672, 'fade_down': 1727}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Spread: Virginia Cavaliers (-3.5)** -$98,306.11 · hold 6m26s · entry 0.409 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
2. **Spread: Thunder (-8.5)** -$70,992.09 · hold 46m38s · entry 0.4928 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
3. **Spread: Florida State (-6.5)** -$70,979.38 · hold 15h52m · entry 0.4914 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Spread: Rockets (-7.5)** -$55,520.54 · hold 20h23m · entry 0.462 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
5. **Bills vs. Texans: O/U 44.5** -$55,214.96 · hold 21h20m · entry 0.4892 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
6. **Army vs. Air Force** -$51,257.30 · hold 1h15m · entry 0.4631 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
7. **Chiefs vs. Bills: O/U 50.5** -$37,034.38 · hold 7h31m · entry 0.559 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Missouri vs. Oklahoma** -$36,894.01 · hold 13h58m · entry 0.3693 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **Nets vs. Celtics** -$36,742.02 · hold 20h38m · entry 0.7303 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **UAB Blazers vs. Rice** -$30,622.12 · hold 5h40m · entry 0.4741 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $20.31
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
template: sovereign2013
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 20.3077
clip_usdc_p90: 634.25
entry_price_median: 0.4981
entry_price_iqr: (0.4798, 0.53)
target_spread: -0.0037
target_spread_p75: 0.0706
median_hold_seconds: 20795
max_hold_seconds_p75: 50074
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

_Generated 2026-08-28T15:08:28.307900+00:00_
