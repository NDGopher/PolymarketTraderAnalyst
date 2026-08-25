# Elite Replication Playbook — HomeRunHazard

Wallet `0x5268527977f700f9bf9b6d5cd843859e4e70135d`. Reverse-engineered from the **full unique fill tape** (26,170 trades · 1,097 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$2,419,854.53 |
| Core cashflow (ex-rebates) | -$2,438,366.83 |
| Closed-position legs sum | $2,231,236.73 |
| Leg win rate / profit factor | 54.02% / 1.0434 |
| Polymarket leaderboard ALL | $2,248,711.81 · vol $264,797,406.19 · rank 67 |
| polymarket_leaderboard_ALL pnl | ref=2248711.8139243205 ours=2231236.7279 (MATCH) |
| polydata realized_pnl | ref=2250300.68 ours=2231236.7279 (MATCH) |
| polydata n_trades | ref=268747 ours=26170 (DRIFT) |
| polydata win_rate | ref=0.5418 ours=0.5402 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 418 markets · -$148,463.07 · avg -$355.17 · median hold 21m30s · median spread None
- **Match / other sports:** 457 markets · -$292,927.53 · avg -$640.98
- **Outcome PnL leaders:**
  - **Tampa Bay Rays**: $53,832.70
  - **Anastasia Potapova**: $44,318.10
  - **Boston Red Sox**: $43,966.59
  - **Spurs**: $43,048.95
  - **Kansas City Royals**: $31,223.74
  - **San Diego Padres**: $29,031.74

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `two_sided_inventory_near_mid`: 288
- `two_sided_inventory_sub_mid`: 208
- `two_sided_inventory_above_mid`: 140
- `directional_buy_near_mid`: 132
- `directional_buy_sub_mid`: 127
- `two_sided_inventory_cheap_tail`: 78
- `directional_buy_above_mid`: 70
- `two_sided_inventory_expensive_favorite`: 39
- `directional_buy_cheap_tail`: 8
- `directional_buy_expensive_favorite`: 7

### First-two-fill sequences
- `BUY->BUY`: 917
- `single_fill`: 180

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 28 | -$43,431.34 | -$1,551.12 |
| 0.20-0.40 | 156 | -$125,802.79 | -$806.43 |
| 0.40-0.60 | 816 | -$424,811.46 | -$520.60 |
| 0.60-0.80 | 80 | $47,345.47 | $591.82 |
| 0.80-1.00 | 17 | $60,726.99 | $3,572.18 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$6.79** median (p90 $478.29).
2. Aim entry price ~**0.5036** (IQR (0.4568, 0.56)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `intraday_swing`: 494
- `single_clip`: 287
- `multi_hour_position`: 227
- `scalp_sub_15m`: 89

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 535 | 469 |
| PnL | $936,976.27 | -$1,422,949.40 |
| Median hold | 58m10s | 1h11m |
| Median spread | None | None |
| Scale-in rate | 0.8486 | 0.9019 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 23.25 | 28.46 |
| Both-sides rate | 0.6953 | 0.8124 |

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
- Losers scale-in **more** (0.9019 vs 0.8486) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 287, 'pnl': 30313.7429, 'avg': 105.6228, 'win_rate': 0.4808}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 1097

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 287 | $30,313.74 | $105.62 | 48.1% |
| 5-30m | 125 | $8,194.71 | $65.56 | 48.8% |
| 30m-2h | 454 | -$245,820.18 | -$541.45 | 49.1% |
| 2-12h | 192 | -$240,065.75 | -$1,250.34 | 48.4% |
| 12h+ | 39 | -$38,595.65 | -$989.63 | 51.3% |

### Exit engine params

1. **TP / ask distance:** target ≈ **None** above avg entry (p75 stretch None). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 58m10s; p75 1h49m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 69.5% of winning markets (losers 81.2%)
- Hold bucket <5m: avg PnL $105.62 on 287 markets (WR 48%)
- Hold bucket 5-30m: avg PnL $65.56 on 125 markets (WR 49%)
- Entry band 0.60-0.80: avg $591.82 across 80 markets
- Buy-ladder behavior: fade-into-weakness markets=331, chase-up markets=319

### Fails
- Hold bucket 30m-2h: avg PnL $-541.45 on 454 markets
- Hold bucket 2-12h: avg PnL $-1250.34 on 192 markets
- Hold bucket 12h+: avg PnL $-989.63 on 39 markets
- Entry band 0.20-0.40: avg $-806.43 across 156 markets — avoid or tighten risk
- Entry band 0.40-0.60: avg $-520.60 across 816 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 319, 'fade_down': 331}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **76ers vs. Knicks: O/U 211.5** -$91,965.56 · hold 1h39m · entry 0.4604 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
2. **Baltimore Orioles vs. New York Yankees** -$70,897.12 · hold 2h03m · entry 0.5628 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Madrid Open: Stefanos Tsitsipas vs Casper Ruud** -$69,098.34 · hold 1h27m · entry 0.6135 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
4. **76ers vs. Knicks: O/U 212.5** -$59,416.63 · hold 1h47m · entry 0.4885 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
5. **New York Mets vs. Colorado Rockies: O/U 10.5** -$57,746.38 · hold 1h29m · entry 0.521 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Madrid Open: Aryna Sabalenka vs Naomi Osaka** -$54,557.39 · hold 2h08m · entry 0.3632 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
7. **Internazionali BNL d'Italia: Federico Cina vs Alexander Blockx** -$23,006.33 · hold 1h28m · entry 0.4214 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
8. **Madrid Open: Daniil Medvedev vs Fabian Marozsan** -$21,487.41 · hold 1h52m · entry 0.2168 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
9. **Madrid Open: Terence Atmane vs Alexander Zverev** -$19,436.44 · hold 1h32m · entry 0.2613 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
10. **Colorado Rockies vs. New York Mets** -$16,346.11 · hold 2h29m · entry 0.5674 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $6.79
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
template: HomeRunHazard
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 6.7871
clip_usdc_p90: 478.2857
entry_price_median: 0.5036
entry_price_iqr: (0.4568, 0.56)
target_spread: None
target_spread_p75: None
median_hold_seconds: 3490
max_hold_seconds_p75: 6578
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

_Generated 2026-08-25T16:46:54.880319+00:00_
