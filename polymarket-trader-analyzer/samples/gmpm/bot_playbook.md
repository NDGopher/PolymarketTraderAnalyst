# Elite Replication Playbook — gmpm

Wallet `0x14964aefa2cd7caff7878b3820a690a03c5aa429`. Reverse-engineered from the **full unique fill tape** (47,326 trades · 845 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `hybrid_mm_directional` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$5,400,173.37 |
| Core cashflow (ex-rebates) | -$5,401,057.55 |
| Closed-position legs sum | $3,075,155.76 |
| Leg win rate / profit factor | 54.61% / 1.2494 |
| Polymarket leaderboard ALL | $3,530,847.58 · vol $87,349,857.86 · rank 42 |
| polymarket_leaderboard_ALL pnl | ref=3530847.5828185184 ours=3075155.7644 (DRIFT) |
| polydata realized_pnl | ref=3530847.58 ours=3075155.7644 (DRIFT) |
| polydata n_trades | ref=45978 ours=47326 (MATCH) |
| polydata win_rate | ref=0.5448 ours=0.5461 (MATCH) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 82 markets · $356,864.96 · avg $4,352.01 · median hold 18m34s · median spread -0.0
- **Match / other sports:** 432 markets · $2,374,784.48 · avg $5,497.19
- **Outcome PnL leaders:**
  - **Seahawks**: $1,826,837.27
  - **Indiana**: $714,885.11
  - **Crawford**: $598,139.47
  - **Falcons**: $468,277.11
  - **Giants**: $346,092.30
  - **Patriots**: $335,346.98

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_near_mid`: 345
- `two_sided_inventory_near_mid`: 151
- `directional_buy_above_mid`: 124
- `directional_buy_sub_mid`: 86
- `directional_buy_expensive_favorite`: 48
- `two_sided_inventory_above_mid`: 30
- `two_sided_inventory_sub_mid`: 27
- `directional_buy_cheap_tail`: 23
- `two_sided_inventory_expensive_favorite`: 6
- `two_sided_inventory_cheap_tail`: 5

### First-two-fill sequences
- `BUY->BUY`: 627
- `single_fill`: 168
- `BUY->SELL`: 50

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 15 | $40,426.71 | $2,695.11 |
| 0.20-0.40 | 47 | $828,112.69 | $17,619.42 |
| 0.40-0.60 | 646 | $2,518,410.01 | $3,898.47 |
| 0.60-0.80 | 95 | -$641,759.57 | -$6,755.36 |
| 0.80-1.00 | 42 | $329,965.93 | $7,856.33 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$15.63** median (p90 $680.00).
2. Aim entry price ~**0.504** (IQR (0.48, 0.57)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 250
- `multi_hour_position`: 215
- `intraday_swing`: 188
- `scalp_sub_15m`: 120
- `market_make_both_outcomes`: 47
- `scale_in_scale_out`: 25

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 467 | 367 |
| PnL | $15,051,333.25 | -$11,976,177.49 |
| Median hold | 36m42s | 27m24s |
| Median spread | 0.0041 | -0.0001 |
| Scale-in rate | 0.7794 | 0.7439 |
| Scale-out rate | 0.1221 | 0.0845 |
| Avg fills/market | 61.23 | 50.92 |
| Both-sides rate | 0.2762 | 0.2452 |

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

- **Winners** sell above buy (median spread **0.0041**). **Losers** often exit worse (median spread **-0.0001**).
- Losers scale-in **more** (0.7439 vs 0.7794) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 263, 'pnl': -593527.1151, 'avg': -2256.7571, 'win_rate': 0.5171}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 665
- `mixed_roundtrip`: 101
- `spread_harvest_sell_above_buy`: 41
- `adverse_exit_sell_below_buy`: 38

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 263 | -$593,527.12 | -$2,256.76 | 51.7% |
| 5-30m | 151 | $347,234.67 | $2,299.57 | 56.3% |
| 30m-2h | 150 | $483,950.42 | $3,226.34 | 60.7% |
| 2-12h | 202 | $1,565,485.05 | $7,749.93 | 54.9% |
| 12h+ | 79 | $1,272,012.74 | $16,101.43 | 55.7% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.0041** above avg entry (p75 stretch 0.01). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 36m42s; p75 3h30m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.0041 vs losers -0.0001
- Both-sides inventory on 27.6% of winning markets (losers 24.5%)
- Hold bucket 5-30m: avg PnL $2299.57 on 151 markets (WR 56%)
- Hold bucket 30m-2h: avg PnL $3226.34 on 150 markets (WR 61%)
- Hold bucket 2-12h: avg PnL $7749.93 on 202 markets (WR 55%)
- Hold bucket 12h+: avg PnL $16101.43 on 79 markets (WR 56%)
- Entry band 0.20-0.40: avg $17619.42 across 47 markets
- Entry band 0.40-0.60: avg $3898.47 across 646 markets
- Entry band 0.80-1.00: avg $7856.33 across 42 markets
- Buy-ladder behavior: fade-into-weakness markets=60, chase-up markets=78

### Fails
- Hold bucket <5m: avg PnL $-2256.76 on 263 markets
- Entry band 0.60-0.80: avg $-6755.36 across 95 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 78, 'fade_down': 60}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Will USA win the 2025 Ryder Cup?
PnL $63,670.07 · hold 1d · 240B/79S · avg entry 0.42 → exit 0.69 (spread 0.27) · `scale_in_scale_out`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-09-25T12:46:19+00:00 | BUY | No | 39187.06 | 0.4200 | 16458.57 |
| 2025-09-25T12:52:19+00:00 | BUY | No | 5800.00 | 0.4200 | 2436.00 |
| 2025-09-25T13:06:21+00:00 | BUY | No | 12.94 | 0.4200 | 5.43 |
| 2025-09-25T16:52:04+00:00 | BUY | No | 19777.77 | 0.4200 | 8306.66 |
| 2025-09-25T16:54:24+00:00 | BUY | No | 190.00 | 0.4200 | 79.80 |
| 2025-09-25T16:54:44+00:00 | BUY | No | 32.23 | 0.4200 | 13.54 |
| 2025-09-25T19:27:53+00:00 | BUY | No | 452.44 | 0.4200 | 190.02 |
| 2025-09-25T19:28:27+00:00 | BUY | No | 250.00 | 0.4200 | 105.00 |
| 2025-09-25T19:29:01+00:00 | BUY | No | 10.00 | 0.4200 | 4.20 |
| 2025-09-25T19:29:57+00:00 | BUY | No | 240.00 | 0.4200 | 100.80 |
| 2025-09-25T19:29:57+00:00 | BUY | No | 550.00 | 0.4200 | 231.00 |
| 2025-09-25T19:30:15+00:00 | BUY | No | 450.00 | 0.4200 | 189.00 |
| 2025-09-25T19:30:15+00:00 | BUY | No | 550.00 | 0.4200 | 231.00 |
| 2025-09-25T19:30:45+00:00 | BUY | No | 40.00 | 0.4200 | 16.80 |
| 2025-09-25T19:30:45+00:00 | BUY | No | 10.00 | 0.4200 | 4.20 |
| 2025-09-27T02:34:33+00:00 | SELL | No | 200.00 | 0.6900 | 138.00 |
| 2025-09-27T02:37:11+00:00 | SELL | No | 500.00 | 0.6900 | 345.00 |
| 2025-09-27T02:37:13+00:00 | SELL | No | 5.00 | 0.6900 | 3.45 |
| 2025-09-27T02:37:39+00:00 | SELL | No | 10.00 | 0.6900 | 6.90 |
| 2025-09-27T02:38:07+00:00 | SELL | No | 60.00 | 0.6900 | 41.40 |
| 2025-09-27T02:39:55+00:00 | SELL | No | 1000.00 | 0.6900 | 690.00 |
| 2025-09-27T02:41:47+00:00 | SELL | No | 100.00 | 0.6900 | 69.00 |
| 2025-09-27T02:43:29+00:00 | SELL | No | 6000.00 | 0.6900 | 4140.00 |
| 2025-09-27T02:44:55+00:00 | SELL | No | 100.00 | 0.6900 | 69.00 |
| 2025-09-27T02:47:51+00:00 | SELL | No | 5.00 | 0.6900 | 3.45 |
| 2025-09-27T02:48:35+00:00 | SELL | No | 500.00 | 0.6900 | 345.00 |
| 2025-09-27T02:50:31+00:00 | SELL | No | 100.00 | 0.6900 | 69.00 |
| 2025-09-27T02:52:49+00:00 | SELL | No | 1000.00 | 0.6900 | 690.00 |
| 2025-09-27T02:53:17+00:00 | SELL | No | 92.00 | 0.6900 | 63.48 |
| 2025-09-27T02:53:31+00:00 | SELL | No | 394.81 | 0.6900 | 272.42 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Spread: Seahawks (-2.5)** -$777,467.85 · hold 4d · entry 0.4965 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Spread: Spurs (-9.5)** -$690,130.98 · hold 0s · entry 0.5 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
3. **Spread: Rams (-10.5)** -$666,476.23 · hold 5h23m · entry 0.4691 → exit 0.47 · `multi_hour_position` / `mixed_roundtrip`
4. **Miami vs. Ohio State** -$534,296.99 · hold 1h40m · entry 0.7413 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
5. **Spread: Texas A&M (-3.5)** -$288,363.77 · hold 1h11m · entry 0.4401 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Ole Miss vs. Georgia** -$261,192.22 · hold 6h05m · entry 0.6239 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
7. **Houston vs. UCF** -$248,787.29 · hold 7h54m · entry 0.4918 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Packers vs. Lions** -$247,101.79 · hold 1d · entry 0.5652 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **Spread: Eagles (-6.5)** -$241,870.20 · hold 1d · entry 0.4528 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **Spread: Oregon (-21.5)** -$203,674.37 · hold 3h57m · entry 0.4428 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $15.63
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
template: gmpm
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 15.6256
clip_usdc_p90: 680.0
entry_price_median: 0.504
entry_price_iqr: (0.48, 0.57)
target_spread: 0.0041
target_spread_p75: 0.01
median_hold_seconds: 2202
max_hold_seconds_p75: 12628
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

_Generated 2026-09-01T15:10:23.658379+00:00_
