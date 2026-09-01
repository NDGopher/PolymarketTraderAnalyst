# Elite Replication Playbook — Allezpapa

Wallet `0xe549581668a5751c1972d3ad2d1991d900bd2d54`. Reverse-engineered from the **full unique fill tape** (57,355 trades · 156 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `directional_or_unclear` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $4,227,794.05 |
| Core cashflow (ex-rebates) | $4,141,946.90 |
| Closed-position legs sum | $11,663,864.02 |
| Leg win rate / profit factor | 98.80% / 51.2755 |
| Polymarket leaderboard ALL | $4,280,722.83 · vol $54,987,532.65 · rank 29 |
| polymarket_leaderboard_ALL pnl | ref=4280722.833949986 ours=4227794.0457 (MATCH) |
| polydata realized_pnl | ref=4280722.83 ours=4227794.0457 (MATCH) |
| polydata n_trades | ref=42825 ours=57355 (DRIFT) |
| polydata win_rate | ref=0.5217 ours=0.988 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 54 markets · $2,103,666.27 · avg $38,956.78 · median hold 4h01m · median spread None
- **Match / other sports:** 82 markets · $8,216,804.54 · avg $100,204.93
- **Outcome PnL leaders:**
  - **Yes**: $6,276,137.52
  - **Over**: $1,981,616.32
  - **No**: $1,431,009.79
  - **England**: $279,483.60
  - **Bosnia and Herzegovina**: $244,958.40
  - **Max Holloway**: $230,173.63

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_above_mid`: 60
- `directional_buy_near_mid`: 34
- `directional_buy_sub_mid`: 31
- `directional_buy_cheap_tail`: 28
- `directional_buy_expensive_favorite`: 2
- `two_sided_inventory_above_mid`: 1

### First-two-fill sequences
- `BUY->BUY`: 150
- `single_fill`: 6

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.00-0.20 | 19 | $2,578,977.12 | $135,735.64 |
| 0.20-0.40 | 30 | $2,692,906.03 | $89,763.53 |
| 0.40-0.60 | 66 | $4,179,374.80 | $63,323.86 |
| 0.60-0.80 | 41 | $2,212,606.07 | $53,966.00 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$10.94** median (p90 $135.85).
2. Aim entry price ~**0.53** (IQR (0.4481, 0.624)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 107
- `scalp_sub_15m`: 23
- `single_clip`: 14
- `intraday_swing`: 12

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 81 | 1 |
| PnL | $11,747,931.63 | -$84,067.62 |
| Median hold | 11h21m | 22h43m |
| Median spread | None | None |
| Scale-in rate | 0.963 | 1.0 |
| Scale-out rate | 0.0 | 0.0 |
| Avg fills/market | 387.41 | 741 |
| Both-sides rate | 0.0 | 1.0 |

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
- Losers scale-in **more** (1.0 vs 0.963) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 25, 'pnl': 1260083.7498, 'avg': 50403.35, 'win_rate': 0.6}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 156

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 25 | $1,260,083.75 | $50,403.35 | 60.0% |
| 5-30m | 11 | $579,562.41 | $52,687.49 | 54.5% |
| 30m-2h | 12 | $984,949.12 | $82,079.09 | 50.0% |
| 2-12h | 26 | $1,694,683.53 | $65,180.14 | 53.8% |
| 12h+ | 82 | $7,144,585.21 | $87,129.09 | 48.8% |

### Exit engine params

1. **TP / ask distance:** target ≈ **None** above avg entry (p75 stretch None). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 11h21m; p75 1d for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 0.0% of winning markets (losers 100.0%)
- Hold bucket <5m: avg PnL $50403.35 on 25 markets (WR 60%)
- Hold bucket 2-12h: avg PnL $65180.14 on 26 markets (WR 54%)
- Hold bucket 12h+: avg PnL $87129.09 on 82 markets (WR 49%)
- Entry band 0.20-0.40: avg $89763.53 across 30 markets
- Entry band 0.40-0.60: avg $63323.86 across 66 markets
- Entry band 0.60-0.80: avg $53966.00 across 41 markets
- Buy-ladder behavior: fade-into-weakness markets=2, chase-up markets=4

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 4, 'fade_down': 2}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Uruguay vs. Cabo Verde: O/U 2.5** -$84,067.62 · hold 22h43m · entry 0.6186 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Will Switzerland win on 2026-06-13?** $0.00 · hold 3d · entry 0.8 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Will Croatia win the 2026 FIFA World Cup?** $0.00 · hold 21h40m · entry 0.009 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Will Ecuador win the 2026 FIFA World Cup?** $0.00 · hold 21h07m · entry 0.008 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
5. **Will Canada win the 2026 FIFA World Cup?** $0.00 · hold 21h15m · entry 0.003 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
6. **Will Argentina win the 2026 FIFA World Cup?** $0.00 · hold 1h38m · entry 0.086 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
7. **Will Switzerland win the 2026 FIFA World Cup?** $0.00 · hold 20h16m · entry 0.012 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Korea Republic vs. Czechia: O/U 2.5** $0.00 · hold 1h58m · entry 0.58 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
9. **Will Senegal win the 2026 FIFA World Cup?** $0.00 · hold 15h41m · entry 0.007 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **Will Sweden win on 2026-06-14?** $0.00 · hold 3d · entry 0.49 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $10.94
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
template: Allezpapa
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 10.9383
clip_usdc_p90: 135.85
entry_price_median: 0.53
entry_price_iqr: (0.4481, 0.624)
target_spread: None
target_spread_p75: None
median_hold_seconds: 40911
max_hold_seconds_p75: 108385
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

_Generated 2026-09-01T14:51:55.605310+00:00_
