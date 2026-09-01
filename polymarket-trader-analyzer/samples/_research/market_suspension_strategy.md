# Market Suspension Strategy — Builder Spec

> User thesis: when **multiple bookmakers pull live odds off the board** during a match, something is happening. Buy Over on Kalshi/Polymarket before the market fully reprices. Exit flat if false alarm; hold/sell into spike if goal.

## Terminology

| Term | Meaning |
|---|---|
| **Market suspension / "odds down"** | Book stops accepting bets — market removed from live board |
| **NOT this** | Decimal odds shortening (probability up) — different signal |
| **Reopen** | Books repost lines after reviewing the event |

---

## Why this signal exists

Bookmakers suspend live markets when their risk desk sees **ambiguous or high-impact information** before they can reprice:

- Goal (pending confirmation / VAR)
- Penalty awarded
- Red card
- Serious injury stoppage
- VAR review started
- Sometimes: dangerous attack, offside check, technical glitch

They suspend because **pricing wrong for 10 seconds costs more than missing 10 seconds of handle.**

---

## Is suspension faster than goal feeds?

**Often yes for the "something happened" alert — not always for "it was a goal."**

```
Typical timeline (soccer goal, top league):

T+0s   Event in stadium
T+1-3s TV broadcast delay
T+2-5s Sharp books SUSPEND (pull off board)     ← YOUR SIGNAL
T+3-8s Some books still showing stale lines
T+5-15s Goal confirmed on TV / data feed
T+5-30s Books reopen with new lines
T+10-60s Polymarket/Kalshi may still lag         ← YOUR ENTRY WINDOW
```

**Key insight:** Suspension is a **binary event** (on board → off board). Easy to detect visually or programmatically. No need to parse 3% probability deltas.

**What suspension tells you:**
- ✅ "Something happened worth stopping risk" — high confidence if 2+ books
- ❌ NOT specifically "goal" — could be card, VAR, injury, penalty

**What suspension does NOT guarantee:**
- That Polymarket/Kalshi are still quoting (they may already have sharp MMs)
- That the event helps Over (red card can cut Over; 0-0 at 80' VAR check ≠ goal)

---

## Multi-book rule (critical)

| Pattern | Interpretation | Action |
|---|---|---|
| 1 book suspends | Noise / glitch / idiosyncratic | **Ignore** |
| 2+ books suspend within 5s | Real event likely | **Trigger** |
| Books suspend 30s+ (VAR) | Outcome uncertain | **Smaller size or wait for reopen direction** |
| Books reopen, score unchanged | False alarm | **Exit flat / small loss** |
| Books reopen, Over line jumped | Goal or major event | **Hold or scale out into spike** |

User observation validated: bet365 alone ≠ signal. Multi-book suspension = signal.

---

## Strategy logic (v1)

```python
# Per match, track live Over market on Kalshi + suspension state of N books

on_tick():
    suspended = count_books_off_board(match_id)  # pinnacle, betfair, bet365, etc.
    
    if suspended >= 2 and not already_in_trade:
        fair_over = estimate_fair_over_from_last_known_lines()
        kalshi_ask = get_kalshi_best_ask("Over")
        
        if kalshi_ask <= fair_over + buffer:  # market hasn't fully reacted
            taker_buy_over(clip=CLIP)
            state = "IN_SUSPENSION_TRADE"
            entry_price = kalshi_ask
            entry_ts = now()

    if state == "IN_SUSPENSION_TRADE":
        if books_reopened() and score_unchanged():
            # false alarm — card, injury, nothing
            flatten(max_loss=STOP_FLAT)  # target -2c to -5c
            
        if over_mid >= entry_price + TARGET_SPIKE:
            scale_out_over(fraction=0.5)
            
        if age > TIME_STOP (90s) and not spiked:
            flatten()
```

### Parameters (start here)

```yaml
min_books_suspended: 2
suspension_window_seconds: 5      # books must go down within this window
clip_usdc: 50                     # start small on Kalshi
target_spike_cents: 10            # take profit if Over jumps 10c+
stop_flat_cents: 4                 # exit false alarm
time_stop_seconds: 90
markets: [soccer_ou_over, nhl_ou_over]  # start with liquid totals
```

---

## Event-type breakdown (manage expectations)

| Suspension cause | Over impact | Exit plan |
|---|---|---|
| **Goal** | Strong UP | Hold / scale out +10–25¢ |
| **Penalty awarded** | Often UP (not certain) | Smaller size; exit on reopen if no conversion |
| **VAR (no goal yet)** | Uncertain | Tighter stop; may whipsaw |
| **Red card** | Depends on score/state | Often hurts Over if chasing high totals |
| **Injury stoppage** | Minimal | Exit flat on reopen |
| **False / technical** | None | Exit flat |

**Win rate will NOT be 80%.** Edge = **asymmetric payoff**: many small flats/losses, occasional large spikes on goals.

This matches polika72's profile: 80% WR on closed legs but median winner spread +20¢ vs losers -4¢ — many small cuts, fat tails on goals.

---

## vs polika72 tape

We cannot prove polika72 uses suspension from on-chain data alone. But the pattern fits:

- 62% taker entry = hitting fast-moving markets
- Chase-up 253 > fade-down 64 = buying into moves, not dips
- Median MFE at 64s = time for suspension → reopen → spike cycle
- Enter taker / exit maker = take on event, sell the rip

**Hypothesis to validate:** correlate polika72 buy timestamps with historical book suspension logs for same matches.

---

## Data sources for suspension detection

| Source | Suspension data? | Cost |
|---|---|---|
| **Odds API aggregators** (OddsJam, OpticOdds, Betfair API) | Often yes — `market_status=suspended` | $$ |
| **Betfair Exchange API** | `marketStatus` INPLAY + SUSPENDED | Low cost |
| **Pinnacle API** (if available) | Line present/absent | Restricted |
| **Scraping bet365** | Fragile, ToS risk | DIY |
| **Sportradar/Betgenius** | Event + suspension flags | $$$ |

**Minimum viable:** Betfair Exchange API + one sharp book via aggregator. Poll every **500ms–1s** during live matches.

---

## Kalshi / Polymarket lag reality check

User is right that these are not always 10–60s behind. On **major live soccer**, sharp participants may reprice in **5–15 seconds** of a goal.

**Your edge window is the GAP between:**
1. Multi-book suspension (T+2–5s), and
2. Kalshi/Polymarket mid fully adjusting (T+?s)

**You must measure this gap empirically** per league and match. Log:
- `t_suspend` — when 2+ books off board
- `t_kalshi_move` — when Kalshi Over mid moves ≥5¢
- `t_goal_feed` — when official/score API updates

If `t_kalshi_move - t_suspend < 2s` on average, edge is dead for that market. If median gap is 5–20s, edge is alive.

---

## Integration with MM base layer

When suspension fires:
1. **Cancel all passive MM quotes** on that match (avoid getting picked off)
2. **Execute directional overlay** (buy Over per spec)
3. After flat or scale-out, **resume MM** if inventory clean

Do not run MM and directional on same match simultaneously without coordination.

---

## Build roadmap

1. **Week 1:** Log suspensions + Kalshi mid moves for 20 live soccer O/U — no trading
2. **Week 2:** Measure gap distribution; filter leagues with median gap > 5s
3. **Week 3:** Paper trade suspension → Over buy → reopen exit rules
4. **Week 4:** Live tiny clips; track markout at +30s/+60s

---

## Related docs

- `kalshi_directional_mm_brief.md` — two-layer bot architecture
- `inventory_skew_guide.md` — MM base layer quoting
- `samples/polika72/bot_playbook.md` — live scalper reference
