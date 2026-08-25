# Elite Replication Playbook — SineNooneEI

Wallet `0x38337de21ff0bb0a11a40761507d51e318d633d1`. Reverse-engineered from the **full unique fill tape** (16,603 trades · 1,580 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `hybrid_mm_directional` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $541,301.28 |
| Core cashflow (ex-rebates) | $523,137.79 |
| Closed-position legs sum | $3,761,463.08 |
| Leg win rate / profit factor | 79.53% / 1.9658 |
| Polymarket leaderboard ALL | $639,212.87 · vol $29,168,764.39 · rank 318 |
| polymarket_leaderboard_ALL pnl | ref=639212.8736756515 ours=541301.2799 (DRIFT) |
| polydata realized_pnl | ref=506308.1 ours=523137.7892 (MATCH) |
| polydata n_trades | ref=14776 ours=16603 (DRIFT) |
| polydata win_rate | ref=0.5312 ours=0.7953 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 7 markets · $72,156.06 · avg $10,308.01 · median hold 1m36s · median spread None
- **Match / other sports:** 1572 markets · $3,816,013.53 · avg $2,427.49
- **Outcome PnL leaders:**
  - **SK Gaming**: $261,339.00
  - **Dplus KIA**: $238,098.32
  - **Team Yandex**: $235,504.44
  - **Movistar KOI**: $186,135.02
  - **Team Liquid**: $172,912.47
  - **G2 Esports**: $167,039.68

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_above_mid`: 560
- `directional_buy_sub_mid`: 541
- `directional_buy_near_mid`: 300
- `directional_buy_expensive_favorite`: 87
- `directional_buy_cheap_tail`: 76
- `two_sided_inventory_near_mid`: 8
- `two_sided_inventory_sub_mid`: 6
- `two_sided_inventory_above_mid`: 2

### First-two-fill sequences
- `BUY->BUY`: 969
- `single_fill`: 610
- `BUY->SELL`: 1

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 29 | $68,889.33 | $2,375.49 |
| 0.20-0.40 | 382 | $1,219,824.16 | $3,193.26 |
| 0.40-0.60 | 664 | $994,426.76 | $1,497.63 |
| 0.60-0.80 | 476 | $1,416,045.47 | $2,974.89 |
| 0.80-1.00 | 29 | $62,277.37 | $2,147.50 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$35.15** median (p90 $2,878.21).
2. Aim entry price ~**0.57** (IQR (0.4374, 0.6689)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `single_clip`: 744
- `scalp_sub_15m`: 674
- `multi_hour_position`: 91
- `intraday_swing`: 71

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 845 | 210 |
| PnL | $7,560,464.40 | -$3,799,001.32 |
| Median hold | 9s | 53s |
| Median spread | -0.0342 | None |
| Scale-in rate | 0.6225 | 0.7524 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 10.07 | 20.71 |
| Both-sides rate | 0.0118 | 0.0286 |

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

- **Winners** sell above buy (median spread **-0.0342**). **Losers** often exit worse (median spread **None**).
- Losers scale-in **more** (0.7524 vs 0.6225) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 1379, 'pnl': 3022086.8724, 'avg': 2191.5061, 'win_rate': 0.5257}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 1576
- `adverse_exit_sell_below_buy`: 3
- `mixed_roundtrip`: 1

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 1379 | $3,022,086.87 | $2,191.51 | 52.6% |
| 5-30m | 38 | $63,882.16 | $1,681.11 | 60.5% |
| 30m-2h | 61 | $196,132.74 | $3,215.29 | 54.1% |
| 2-12h | 99 | $398,861.98 | $4,028.91 | 61.6% |
| 12h+ | 3 | $80,499.33 | $26,833.11 | 100.0% |

### Exit engine params

1. **TP / ask distance:** target ≈ **-0.0342** above avg entry (p75 stretch -0.0101). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 9s; p75 1m13s for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 1.2% of winning markets (losers 2.9%)
- Hold bucket <5m: avg PnL $2191.51 on 1379 markets (WR 53%)
- Hold bucket 5-30m: avg PnL $1681.11 on 38 markets (WR 61%)
- Hold bucket 30m-2h: avg PnL $3215.29 on 61 markets (WR 54%)
- Hold bucket 2-12h: avg PnL $4028.91 on 99 markets (WR 62%)
- Entry band 0.20-0.40: avg $3193.26 across 382 markets
- Entry band 0.40-0.60: avg $1497.63 across 664 markets
- Entry band 0.60-0.80: avg $2974.89 across 476 markets
- Buy-ladder behavior: fade-into-weakness markets=16, chase-up markets=47

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 47, 'fade_down': 16}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Spread: Pistons (-8.5)** -$126,706.51 · hold 3h58m · entry 0.4964 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Counter-Strike: paiN vs Passion UA (BO3) - ESL Pro League Stage 1** -$84,487.84 · hold 20s · entry 0.57 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
3. **Will Chelsea FC win on 2026-03-14?** -$81,935.18 · hold 1m56s · entry 0.5672 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
4. **LoL: Cloud9 vs LYON - Game 2 Winner** -$69,220.58 · hold 0s · entry 0.6898 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
5. **LoL: DRX vs Nongshim Red Force - Game 1 Winner** -$62,131.89 · hold 1m22s · entry 0.6213 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
6. **Counter-Strike: FURIA vs Vitality (BO5) - IEM Krakow Playoffs** -$59,675.53 · hold 6h26m · entry 0.3324 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
7. **LoL: Cloud9 vs LYON (BO5) - LCS Lock In Playoffs** -$52,198.45 · hold 2h55m · entry 0.6989 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Counter-Strike: Vitality vs MOUZ (BO3) - IEM Krakow Playoffs** -$49,989.72 · hold 8h20m · entry 0.3498 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
9. **LoL: Dplus KIA vs DN Freecs - Game 3 Winner** -$47,509.46 · hold 2m58s · entry 0.5985 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`
10. **LoL: JD Gaming vs Top Esports - Game 2 Winner** -$45,213.06 · hold 1m40s · entry 0.419 → exit None · `scalp_sub_15m` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $35.15
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
template: SineNooneEI
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 35.1481
clip_usdc_p90: 2878.2108
entry_price_median: 0.57
entry_price_iqr: (0.4374, 0.6689)
target_spread: -0.0342
target_spread_p75: -0.0101
median_hold_seconds: 9
max_hold_seconds_p75: 73
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

_Generated 2026-08-25T21:55:39.321164+00:00_
