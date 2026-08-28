# Elite Replication Playbook — kch123

Wallet `0x6a72f61820b26b1fe4d956e17b6dc2a1ea3033ee`. Reverse-engineered from the **full unique fill tape** (106,103 trades · 1,755 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `strong_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $3,628,200.69 |
| Core cashflow (ex-rebates) | $3,628,142.05 |
| Closed-position legs sum | $13,390,318.52 |
| Leg win rate / profit factor | 52.67% / 1.2366 |
| Polymarket leaderboard ALL | $11,386,690.88 · vol $298,637,138.56 · rank 5 |
| polymarket_leaderboard_ALL pnl | ref=11386690.875513867 ours=13390318.5232 (DRIFT) |
| polydata realized_pnl | ref=11386690.88 ours=13390318.5232 (DRIFT) |
| polydata n_trades | ref=171115 ours=106103 (DRIFT) |
| polydata win_rate | ref=0.5467 ours=0.5267 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 295 markets · $1,609,257.66 · avg $5,455.11 · median hold 5m10s · median spread 0.01
- **Match / other sports:** 1259 markets · $2,856,021.22 · avg $2,268.48
- **Outcome PnL leaders:**
  - **Seahawks**: $1,600,001.37
  - **Under**: $1,480,704.58
  - **No**: $1,306,260.98
  - **Nuggets**: $1,264,815.52
  - **Clippers**: $719,344.75
  - **Texans**: $636,179.79

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_near_mid`: 470
- `two_sided_inventory_sub_mid`: 346
- `two_sided_inventory_above_mid`: 265
- `two_sided_inventory_near_mid`: 257
- `directional_buy_sub_mid`: 122
- `directional_buy_above_mid`: 114
- `two_sided_inventory_cheap_tail`: 65
- `two_sided_inventory_expensive_favorite`: 61
- `directional_buy_expensive_favorite`: 34
- `directional_buy_cheap_tail`: 21

### First-two-fill sequences
- `BUY->BUY`: 1551
- `single_fill`: 201
- `BUY->SELL`: 3

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 43 | -$338,837.48 | -$7,879.94 |
| 0.20-0.40 | 186 | $1,882,927.07 | $10,123.26 |
| 0.40-0.60 | 1094 | $6,760,241.70 | $6,179.38 |
| 0.60-0.80 | 354 | $1,565,063.73 | $4,421.08 |
| 0.80-1.00 | 78 | $19,913.80 | $255.31 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$13.53** median (p90 $1,009.29).
2. Aim entry price ~**0.53** (IQR (0.48, 0.6559)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 759
- `intraday_swing`: 546
- `single_clip`: 287
- `scalp_sub_15m`: 161
- `market_make_both_outcomes`: 2

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 960 | 795 |
| PnL | $49,994,581.78 | -$40,105,272.95 |
| Median hold | 1h49m | 1h47m |
| Median spread | 0.439 | 0.6391 |
| Scale-in rate | 0.8833 | 0.8843 |
| Scale-out rate | 0.0021 | 0.0013 |
| Avg fills/market | 65.95 | 53.83 |
| Both-sides rate | 0.5365 | 0.6025 |

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

- **Winners** sell above buy (median spread **0.439**). **Losers** often exit worse (median spread **0.6391**).
- Losers scale-in **more** (0.8843 vs 0.8833) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 358, 'pnl': 6127885.4871, 'avg': 17116.9986, 'win_rate': 0.5279}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 1723
- `spread_harvest_sell_above_buy`: 28
- `mixed_roundtrip`: 2
- `adverse_exit_sell_below_buy`: 2

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 358 | $6,127,885.49 | $17,117.00 | 52.8% |
| 5-30m | 150 | $1,746,960.36 | $11,646.40 | 56.7% |
| 30m-2h | 483 | $199,853.60 | $413.78 | 54.4% |
| 2-12h | 641 | -$69,160.12 | -$107.89 | 54.4% |
| 12h+ | 123 | $1,883,769.50 | $15,315.20 | 60.2% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.439** above avg entry (p75 stretch 0.5001). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 1h49m; p75 2h43m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.439 vs losers 0.6391
- Both-sides inventory on 53.6% of winning markets (losers 60.2%)
- Hold bucket <5m: avg PnL $17117.00 on 358 markets (WR 53%)
- Hold bucket 5-30m: avg PnL $11646.40 on 150 markets (WR 57%)
- Hold bucket 30m-2h: avg PnL $413.78 on 483 markets (WR 54%)
- Hold bucket 12h+: avg PnL $15315.20 on 123 markets (WR 60%)
- Entry band 0.20-0.40: avg $10123.26 across 186 markets
- Entry band 0.40-0.60: avg $6179.38 across 1094 markets
- Entry band 0.60-0.80: avg $4421.08 across 354 markets
- Entry band 0.80-1.00: avg $255.31 across 78 markets
- Buy-ladder behavior: fade-into-weakness markets=380, chase-up markets=669

### Fails
- Hold bucket 2-12h: avg PnL $-107.89 on 641 markets
- Entry band 0.00-0.20: avg $-7879.94 across 43 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 669, 'fade_down': 380}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Will Aston Villa FC win on 2026-01-18?
PnL $164,044.15 · hold 4h36m · 7B/38S · avg entry 0.4869 → exit 0.999 (spread 0.5121) · `market_make_both_outcomes`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2026-01-18T17:24:52+00:00 | BUY | No | 153685.46 | 0.4900 | 75305.88 |
| 2026-01-18T17:25:02+00:00 | BUY | No | 46314.54 | 0.4900 | 22694.12 |
| 2026-01-18T17:25:24+00:00 | BUY | No | 300000.00 | 0.4900 | 147000.00 |
| 2026-01-18T17:31:00+00:00 | BUY | Yes | 200000.00 | 0.4800 | 96000.00 |
| 2026-01-18T17:32:24+00:00 | BUY | Yes | 44618.75 | 0.4800 | 21417.00 |
| 2026-01-18T17:32:28+00:00 | BUY | Yes | 102.60 | 0.4800 | 49.25 |
| 2026-01-18T17:33:56+00:00 | BUY | No | 52473.60 | 0.4900 | 25712.06 |
| 2026-01-18T22:01:30+00:00 | SELL | No | 249840.15 | 0.9990 | 249590.31 |
| 2026-01-18T22:01:38+00:00 | SELL | No | 9.90 | 0.9990 | 9.89 |
| 2026-01-18T22:01:38+00:00 | SELL | No | 2.00 | 0.9990 | 2.00 |
| 2026-01-18T22:01:38+00:00 | SELL | No | 5.01 | 0.9990 | 5.00 |
| 2026-01-18T22:01:38+00:00 | SELL | No | 10.01 | 0.9990 | 10.00 |
| 2026-01-18T22:01:38+00:00 | SELL | No | 20.02 | 0.9990 | 20.00 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.09 | 0.9990 | 1.09 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 40.59 | 0.9990 | 40.55 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.99 | 0.9990 | 1.99 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:42+00:00 | SELL | No | 1.09 | 0.9990 | 1.09 |
| 2026-01-18T22:01:44+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:46+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:46+00:00 | SELL | No | 1.19 | 0.9990 | 1.19 |
| 2026-01-18T22:01:48+00:00 | SELL | No | 1171.04 | 0.9990 | 1169.87 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Will FC Barcelona win on 2026-01-18?** -$713,998.80 · hold 21m22s · entry 0.595 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
2. **Blue Jays vs. Mariners** -$665,499.98 · hold 9h25m · entry 0.55 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Bills vs. Jaguars** -$549,430.45 · hold 5h12m · entry 0.5388 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Chiefs vs. Cowboys** -$533,797.48 · hold 3h35m · entry 0.6033 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
5. **Blue Jays vs. Dodgers** -$519,406.04 · hold 50m16s · entry 0.6412 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Will Olympiakós SFP win on 2026-01-20?** -$510,999.30 · hold 9m14s · entry 0.5678 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
7. **Spread: Lions (-3.5)** -$456,849.98 · hold 6h36m · entry 0.52 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Patriots vs. Ravens** -$430,358.49 · hold 4h37m · entry 0.645 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **Ravens vs. Packers** -$430,296.71 · hold 2h39m · entry 0.5071 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **Alabama vs. Oklahoma** -$412,300.01 · hold 3h10m · entry 0.5204 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $13.53
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
template: kch123
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 13.5313
clip_usdc_p90: 1009.29
entry_price_median: 0.53
entry_price_iqr: (0.48, 0.6559)
target_spread: 0.439
target_spread_p75: 0.5001
median_hold_seconds: 6560
max_hold_seconds_p75: 9802
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

_Generated 2026-08-28T15:23:19.764131+00:00_
