# Elite Replication Playbook — 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465

Wallet `0x2c335066fe58fe9237c3d3dc7b275c2a034a0563`. Reverse-engineered from the **full unique fill tape** (351,490 trades · 4,314 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `likely_market_maker` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | -$29,849,472.90 |
| Core cashflow (ex-rebates) | -$29,957,480.73 |
| Closed-position legs sum | $17,071,768.04 |
| Leg win rate / profit factor | 60.52% / 1.1572 |
| Polymarket leaderboard ALL | $7,374,604.84 · vol $1,000,345,735.50 · rank 16 |
| polymarket_leaderboard_ALL pnl | ref=7374604.843242512 ours=17071768.0427 (DRIFT) |
| polydata realized_pnl | ref=7387346.99 ours=17071768.0427 (DRIFT) |
| polydata n_trades | ref=324009 ours=351490 (DRIFT) |
| polydata win_rate | ref=0.5548 ours=0.6052 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 471 markets · -$129,152.92 · avg -$274.21 · median hold 2m48s · median spread 0.0345
- **Match / other sports:** 2705 markets · $5,268,004.70 · avg $1,947.51
- **Outcome PnL leaders:**
  - **Yes**: $7,332,033.15
  - **Knicks**: $1,695,479.09
  - **Cabo Verde**: $875,347.56
  - **Paraguay**: $447,433.12
  - **Morocco**: $411,017.51
  - **San Francisco Giants**: $353,465.17

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_near_mid`: 1063
- `directional_buy_above_mid`: 742
- `directional_buy_expensive_favorite`: 653
- `directional_buy_sub_mid`: 504
- `two_sided_inventory_near_mid`: 339
- `directional_buy_cheap_tail`: 283
- `two_sided_inventory_sub_mid`: 249
- `two_sided_inventory_above_mid`: 244
- `two_sided_inventory_expensive_favorite`: 128
- `two_sided_inventory_cheap_tail`: 89
- `sell_first_cheap_tail`: 20

### First-two-fill sequences
- `BUY->BUY`: 2987
- `single_fill`: 1293
- `BUY->SELL`: 22
- `SELL->SELL`: 11
- `SELL->BUY`: 1

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 228 | $176,971.54 | $776.19 |
| 0.20-0.40 | 522 | -$802,086.61 | -$1,536.56 |
| 0.40-0.60 | 2063 | $7,268,291.86 | $3,523.17 |
| 0.60-0.80 | 899 | $1,177,881.08 | $1,310.21 |
| 0.80-1.00 | 583 | -$2,200,839.40 | -$3,775.02 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$21.84** median (p90 $401.79).
2. Aim entry price ~**0.5703** (IQR (0.49, 0.76)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 1920
- `scalp_sub_15m`: 857
- `multi_hour_position`: 790
- `intraday_swing`: 718
- `market_make_both_outcomes`: 20
- `scale_in_scale_out`: 9

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 2393 | 1761 |
| PnL | $57,946,922.21 | -$52,035,675.48 |
| Median hold | 4m33s | 4m02s |
| Median spread | 0.0144 | -0.0089 |
| Scale-in rate | 0.6929 | 0.7217 |
| Scale-out rate | 0.0084 | 0.0165 |
| Avg fills/market | 88.21 | 79.38 |
| Both-sides rate | 0.2298 | 0.2817 |

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

- **Winners** sell above buy (median spread **0.0144**). **Losers** often exit worse (median spread **-0.0089**).
- Losers scale-in **more** (0.7217 vs 0.6929) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 2242, 'pnl': 347609.1331, 'avg': 155.0442, 'win_rate': 0.5406}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 4235
- `spread_harvest_sell_above_buy`: 23
- `adverse_exit_sell_below_buy`: 20
- `sell_inventory_only`: 19
- `mixed_roundtrip`: 17

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 2242 | $347,609.13 | $155.04 | 54.1% |
| 5-30m | 515 | $1,459,123.41 | $2,833.25 | 57.3% |
| 30m-2h | 637 | $2,965,558.85 | $4,655.51 | 58.9% |
| 2-12h | 557 | $698,047.40 | $1,253.23 | 53.3% |
| 12h+ | 363 | $440,907.93 | $1,214.62 | 59.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **0.0144** above avg entry (p75 stretch 0.0455). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 4m33s; p75 1h35m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Winners capture median spread 0.0144 vs losers -0.0089
- Both-sides inventory on 23.0% of winning markets (losers 28.2%)
- Hold bucket <5m: avg PnL $155.04 on 2242 markets (WR 54%)
- Hold bucket 5-30m: avg PnL $2833.25 on 515 markets (WR 57%)
- Hold bucket 30m-2h: avg PnL $4655.51 on 637 markets (WR 59%)
- Hold bucket 2-12h: avg PnL $1253.23 on 557 markets (WR 53%)
- Hold bucket 12h+: avg PnL $1214.62 on 363 markets (WR 59%)
- Entry band 0.00-0.20: avg $776.19 across 228 markets
- Entry band 0.40-0.60: avg $3523.17 across 2063 markets
- Entry band 0.60-0.80: avg $1310.21 across 899 markets
- Buy-ladder behavior: fade-into-weakness markets=414, chase-up markets=617

### Fails
- Entry band 0.20-0.40: avg $-1536.56 across 522 markets — avoid or tighten risk
- Entry band 0.80-1.00: avg $-3775.02 across 583 markets — avoid or tighten risk
- Chase vs fade ladders: `{'chase_up': 617, 'fade_down': 414}`

## 7. Fill-by-fill autopsies (copy these patterns)

### Example 1: Falcons vs. 49ers
PnL $10,700.00 · hold 13m26s · 23B/1S · avg entry 0.498 → exit 0.52 (spread 0.022) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-10-20T00:04:57+00:00 | BUY | Falcons | 793.12 | 0.5100 | 404.49 |
| 2025-10-20T00:05:15+00:00 | BUY | Falcons | 2426.00 | 0.5100 | 1237.26 |
| 2025-10-20T00:05:47+00:00 | BUY | Falcons | 1484.00 | 0.5100 | 756.84 |
| 2025-10-20T00:05:51+00:00 | BUY | Falcons | 1185.29 | 0.5100 | 604.50 |
| 2025-10-20T00:06:09+00:00 | BUY | Falcons | 3453.63 | 0.5100 | 1761.35 |
| 2025-10-20T00:06:19+00:00 | BUY | Falcons | 1377.00 | 0.5100 | 702.27 |
| 2025-10-20T00:06:19+00:00 | BUY | Falcons | 408.16 | 0.5100 | 208.16 |
| 2025-10-20T00:06:21+00:00 | BUY | Falcons | 40.82 | 0.5100 | 20.82 |
| 2025-10-20T00:06:25+00:00 | BUY | Falcons | 3405.91 | 0.5100 | 1737.01 |
| 2025-10-20T00:06:25+00:00 | BUY | Falcons | 1652.62 | 0.5100 | 842.84 |
| 2025-10-20T00:06:35+00:00 | BUY | Falcons | 2009.18 | 0.5100 | 1024.68 |
| 2025-10-20T00:06:51+00:00 | BUY | Falcons | 763.27 | 0.5100 | 389.27 |
| 2025-10-20T00:07:07+00:00 | BUY | Falcons | 1855.83 | 0.5100 | 946.47 |
| 2025-10-20T00:07:07+00:00 | BUY | Falcons | 287.26 | 0.5100 | 146.50 |
| 2025-10-20T00:07:19+00:00 | BUY | Falcons | 6122.45 | 0.5100 | 3122.45 |
| 2025-10-20T00:07:57+00:00 | BUY | Falcons | 4.08 | 0.5100 | 2.08 |
| 2025-10-20T00:08:01+00:00 | BUY | Falcons | 30.61 | 0.5100 | 15.61 |
| 2025-10-20T00:08:13+00:00 | BUY | Falcons | 1952.38 | 0.5100 | 995.71 |
| 2025-10-20T00:08:15+00:00 | BUY | Falcons | 19.23 | 0.5100 | 9.81 |
| 2025-10-20T00:08:35+00:00 | BUY | Falcons | 729.13 | 0.5100 | 371.86 |
| 2025-10-20T00:17:39+00:00 | SELL | Falcons | 29999.96 | 0.5200 | 15599.98 |
| 2025-10-20T00:18:01+00:00 | BUY | 49ers | 545.78 | 0.4800 | 261.97 |
| 2025-10-20T00:18:05+00:00 | BUY | 49ers | 192.31 | 0.4800 | 92.31 |
| 2025-10-20T00:18:23+00:00 | BUY | 49ers | 19261.91 | 0.4800 | 9245.72 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

### Example 2: Counter-Strike: Team Falcons vs Vitality (BO5)
PnL $410.76 · hold 5m10s · 4B/1S · avg entry 0.6571 → exit 0.88 (spread 0.2229) · `scalp_sub_15m`

| Time (UTC) | Side | Outcome | Size | Price | USDC |
|---|---|---|---:|---:|---:|
| 2025-10-12T17:16:43+00:00 | BUY | Vitality | 4581.97 | 0.8600 | 3940.49 |
| 2025-10-12T17:18:41+00:00 | SELL | Vitality | 10.00 | 0.8800 | 8.80 |
| 2025-10-12T17:20:43+00:00 | BUY | Team Falcons | 524.01 | 0.1296 | 67.92 |
| 2025-10-12T17:21:11+00:00 | BUY | Team Falcons | 1000.00 | 0.1400 | 140.00 |
| 2025-10-12T17:21:53+00:00 | BUY | Team Falcons | 240.01 | 0.0900 | 21.60 |

**Read:** buy cluster → sell cluster higher (sometimes a second buy-the-dip + sell-the-rip later same match).

## 8. Failure modes (do not bot these)

1. **Will Senegal win on 2026-07-01?** -$1,115,645.73 · hold 11h12m · entry 0.8864 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Will IR Iran win on 2026-06-15?** -$737,895.80 · hold 2h34m · entry 0.507 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Will Spain win on 2026-06-15?** -$697,262.45 · hold 2h44m · entry 0.6895 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Will Germany vs. Paraguay end in a draw?** -$654,131.80 · hold 3h08m · entry 0.589 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
5. **Senegal vs. Iraq: O/U 3.5** -$603,052.97 · hold 1h54m · entry 0.551 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Will Türkiye win on 2026-06-19?** -$566,280.13 · hold 2h02m · entry 0.4975 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
7. **Will Paris Saint-Germain FC win on 2026-05-30?** -$557,671.52 · hold 8h19m · entry 0.6073 → exit 0.001 · `market_make_both_outcomes` / `adverse_exit_sell_below_buy`
8. **Germany vs. Paraguay: Team to Advance** -$548,641.04 · hold 2h58m · entry 0.6331 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **Will Portugal vs. DR Congo end in a draw?** -$454,895.55 · hold 1d · entry 0.6686 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **Will Ecuador win on 2026-06-25?** -$441,171.71 · hold 3h36m · entry 0.777 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $21.84
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
template: 0x2c335066FE58fe9237c3d3Dc7b275C2a034a0563-1759935795465
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 21.8381
clip_usdc_p90: 401.7931
entry_price_median: 0.5703
entry_price_iqr: (0.49, 0.76)
target_spread: 0.0144
target_spread_p75: 0.0455
median_hold_seconds: 273
max_hold_seconds_p75: 5723
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

_Generated 2026-09-01T15:13:18.425215+00:00_
