# Elite Replication Playbook — WTSA

Wallet `0x04d5524a0a5af2eca6e39e03defc261d42fe66d8`. Reverse-engineered from the **full unique fill tape** (17,934 trades · 61 markets). This is an implementation spec for a high-end bot, not vibes.

## 0. True strategy identity (read this first)

Classification `directional_or_unclear` — mix of spread capture and directional inventory.

Heuristic label from the scanner may still say `likely_market_maker` because of fast round-trips + sell>buy + maker rebates. **Operationally, build a live scalper with optional maker quoting**, not a Yes/No pair inventory bot.

## 1. Performance anchors

| Source / metric | Value |
|---|---|
| Cashflow realized (sells−buys+redeems+rebates) | $169,030.34 |
| Core cashflow (ex-rebates) | $160,372.00 |
| Closed-position legs sum | $3,581,052.07 |
| Leg win rate / profit factor | 98.70% / 122.4517 |
| Polymarket leaderboard ALL | $445,687.54 · vol $14,298,289.84 · rank 468 |
| polymarket_leaderboard_ALL pnl | ref=445687.5427547153 ours=169030.3377 (DRIFT) |
| polydata realized_pnl | ref=519173.09 ours=169030.3377 (DRIFT) |
| polydata n_trades | ref=29173 ours=17934 (DRIFT) |
| polydata win_rate | ref=0.5402 ours=0.987 (DRIFT) |

Notes: Polymarket leaderboard ALL is the primary official PnL check (we match within tolerance). PolyData uses a different event aggregation / trade counting method — expect DRIFT on WR and trade count; use it as a secondary research signal, not the ground truth for fills.

## 2. Universe — where the money is

- **O/U / totals:** 21 markets · $395,661.76 · avg $18,841.04 · median hold 14m25s · median spread None
- **Match / other sports:** 38 markets · $890,430.19 · avg $23,432.37
- **Outcome PnL leaders:**
  - **Yes**: $546,676.50
  - **No**: $343,753.69
  - **Under**: $285,824.33
  - **Over**: $109,837.44
  - **Associação Chapecoense de Futebol**: $20,166.22
  - **Portland Timbers**: $4,300.00

### Bot universe rules

1. Only liquid live sports (soccer/football first — their tape is soccer-heavy).
2. Prefer O/U lines with tight books and active in-game trading.
3. Default bias toward **Over** unless your signal says otherwise (their Over PnL dominates).
4. Skip politics/crypto until you have separate evidence.
5. Require enough depth to enter ~median clip and exit within 1–2 minutes.

## 3. ENTRY — exact mechanics

### Style histogram
- `directional_buy_near_mid`: 23
- `directional_buy_sub_mid`: 18
- `directional_buy_above_mid`: 16
- `directional_buy_cheap_tail`: 3
- `two_sided_inventory_near_mid`: 1

### First-two-fill sequences
- `BUY->BUY`: 60
- `single_fill`: 1

### Entry price → realized edge

| Avg buy band | Markets | Total PnL | Avg PnL |
|---|---:|---:|---:|
| 0.20-0.40 | 13 | $182,533.90 | $14,041.07 |
| 0.40-0.60 | 38 | $1,039,138.45 | $27,345.75 |
| 0.60-0.80 | 10 | $88,885.82 | $8,888.58 |

**Best band:** 0.40–0.60 (near mid) — highest average PnL. Tails (≤0.20 or ≥0.80) make less per market.

### Entry checklist (bot)

1. Clip **$5.36** median (p90 $104.12).
2. Aim entry price ~**0.5129** (IQR (0.4666, 0.567)).
3. Trigger = microstructure, not long-term forecast:
   - mid dips / liquidity hole you can buy
   - imminent volatility (attack, corner, shot) where Over can jump
   - resting bid gets lifted? you’re being taken — manage immediately
4. Prefer **maker bids**; take only if the expected jump already started and ask is still inside your edge.
5. Same-second multi-fills are normal (one order, many counterparties) — treat as one decision, many fills.

## 4. MANAGEMENT — what they do after entry

### Styles
- `multi_hour_position`: 21
- `scalp_sub_15m`: 19
- `intraday_swing`: 19
- `single_clip`: 2

### Winners vs losers

| Metric | Winners | Losers |
|---|---:|---:|
| N | 32 | None |
| PnL | $1,310,558.18 | n/a |
| Median hold | 37m09s | n/a |
| Median spread | None | None |
| Scale-in rate | 1.0 | None |
| Scale-out rate | 0.0 | None |
| Avg fills/market | 293.84 | None |
| Both-sides rate | 0.0312 | None |

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
- Losers scale-in **more** (None vs 1.0) — averaging down is how they bleed; the bot should **forbid** revenge scale-ins without a fresh signal.
- Hold edge peaks in **<5m** ({'n': 9, 'pnl': 81792.2521, 'avg': 9088.028, 'win_rate': 0.4444}) and a strong **30m–2h** bucket for the larger in-game campaigns.

## 5. EXIT — rules that print

- `hold_to_resolution_or_redeem`: 61

| Hold bucket | N | Total PnL | Avg | Win rate |
|---|---:|---:|---:|---:|
| <5m | 9 | $81,792.25 | $9,088.03 | 44.4% |
| 5-30m | 16 | $385,870.50 | $24,116.91 | 56.2% |
| 30m-2h | 15 | $321,986.43 | $21,465.76 | 60.0% |
| 2-12h | 18 | $440,027.46 | $24,445.97 | 50.0% |
| 12h+ | 3 | $80,881.53 | $26,960.51 | 33.3% |

### Exit engine params

1. **TP / ask distance:** target ≈ **None** above avg entry (p75 stretch None). On live O/U this is often a burst move, not slow grind.
2. **Time stop:** median hold 37m09s; p75 4h19m for the scalps — escalate urgency after that.
3. **Scale-out:** peel into strength (their winners stack sells). Don’t wait for one perfect print.
4. **Stop:** if mid < entry − ~3–5¢ on unhedged inventory with no signal → take the loss (copy losers’ speed, not their hope).
5. **Flatten before resolution** — redeem is residual.
6. Taker exits are fine when the move already happened and maker asks won’t fill.

## 6. What works / what fails

### Works
- Both-sides inventory on 3.1% of winning markets (losers 0.0%)
- Entry band 0.40-0.60: avg $27345.75 across 38 markets
- Buy-ladder behavior: fade-into-weakness markets=0, chase-up markets=3

### Fails
- (no strong negative bucket)
- Chase vs fade ladders: `{'chase_up': 3, 'fade_down': 0}`

## 7. Fill-by-fill autopsies (copy these patterns)

## 8. Failure modes (do not bot these)

1. **Will Toronto FC win on 2026-07-16?** $0.00 · hold 17h28m · entry 0.2996 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
2. **Will Vancouver Whitecaps FC win on 2026-07-16?** $0.00 · hold 14h33m · entry 0.6092 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
3. **Will Chicago Fire FC win on 2026-07-16?** $0.00 · hold 10h14m · entry 0.3546 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
4. **Club Tijuana vs. Tigres de la UANL: O/U 2.5** $0.00 · hold 43m57s · entry 0.519 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
5. **Will Club León FC win on 2026-07-17?** $0.00 · hold 38m36s · entry 0.44 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
6. **Will Criciúma EC win on 2026-07-18?** $0.00 · hold 0s · entry 0.43 → exit None · `single_clip` / `hold_to_resolution_or_redeem`
7. **Will AC Goianiense win on 2026-07-20?** $0.00 · hold 4h44m · entry 0.49 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
8. **Pumas de la UNAM vs. CF Pachuca: O/U 2.5** $0.00 · hold 29m30s · entry 0.4861 → exit None · `intraday_swing` / `hold_to_resolution_or_redeem`
9. **Will Vancouver Whitecaps FC win on 2026-07-22?** $0.00 · hold 5h47m · entry 0.534 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`
10. **Will Philadelphia Union win on 2026-07-22?** $0.00 · hold 5h44m · entry 0.4578 → exit None · `multi_hour_position` / `hold_to_resolution_or_redeem`

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
   - default post-only bids/asks; clip $5.36
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
template: WTSA
mode: one_sided_live_scalper  # not classic two-sided MM
preferred_outcome_bias: Over
clip_usdc_median: 5.3564
clip_usdc_p90: 104.12
entry_price_median: 0.5129
entry_price_iqr: (0.4666, 0.567)
target_spread: None
target_spread_p75: None
median_hold_seconds: 2229
max_hold_seconds_p75: 15587
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

_Generated 2026-08-25T21:55:37.988914+00:00_
