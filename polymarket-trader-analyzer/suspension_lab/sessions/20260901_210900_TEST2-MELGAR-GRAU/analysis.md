# MELGAR-GRAU Session Analysis: Real Goal, False VAR Alert

Session: `20260901_210900_TEST2-MELGAR-GRAU`  
Game: Atletico Grau vs Melgar (Peru Liga 1)  
Tape: ~35 min, 200ms book samples in `books_long.csv`

**Ground truth (user):** There was a real goal. It was never under VAR review. The red "VAR Alert" on O0.5 was a false alarm caused by a thin lowball bid on a bonded market.

---

## Timeline of the goal

| Time (UTC) | Market | Event | Book state |
|------------|--------|-------|------------|
| **21:32:45.340** | ML-CAG (Grau) | Bid jump 19→34¢ (+15¢), qty 2,568 | Ask 20→40¢. Kalshi moved ~1s before b365 (per user). |
| **21:32:51.405** | O0.5 | Bid jump 60→98¢ (+38¢), qty 249 | Ask 94→99¢. `hold_bond` mode — correct. |
| 21:32:58–21:33:24 | O0.5 | Bonded | 98–99¢ bid, 99¢ ask, 1–2¢ spread. Goal confirmed in market. |
| **21:33:25.152** | O0.5 | First spoof episode | Bid 99→**75¢** x 7.6. **Ask missing** in tape (feed gap). Recovered to 96¢ within 3s. |
| 21:33:27–21:33:52 | O0.5 | Re-bonded | Back to 97–99¢ bid/ask. Game still live. |
| **21:33:53.041** | O0.5 | Second spoof episode (UI alert) | Bid **75¢** x 7.6, ask **99¢** x 105. **24¢ wide spread.** This triggered the false VAR alert. |
| 21:33:53–21:34:12 | O0.5 | Spoof persisted | 75¢ x 7.6 / 99¢ ask unchanged for ~19s. No VAR in football. |
| After 21:34:12 | O0.5 | Recovery | Market returned to bonded levels. |

### What did NOT move

- **O1.5** (TOTAL-2): stayed ~15¢ through the goal window — no false signal (correct).
- **O2.5 / O3.5**: minimal reaction.

---

## Why the VAR alert was wrong

The detector's `_check_var_revert` only watched **best bid** falling ≥10¢ from post-signal peak. On a bonded O0.5 after a confirmed goal:

```
75¢ x 7.6  |  99¢ x 105
   ↑ thin lowball      ↑ real offer — market still says goal stands
```

This is **not** a VAR signature. In true VAR/cancelled-goal events (e.g. Zurich session), **both** bid and ask collapse together and stay reverted.

### Spoof vs true VAR

| Signature | Spoof (MELGAR) | True VAR (Zurich) |
|-----------|----------------|-------------------|
| Ask | Stays ≥95¢ | Collapses with bid |
| Spread | Wide (24¢+) | Tight or both sides gone |
| Bid qty | Thin (<10 contracts) | Often larger MM pull |
| Recovery | Returns to 99¢ | Stays reverted |
| Football | Play continues | Review/cancellation |

---

## Detector replay (saved tape)

```
21:32:45.340 [GOAL] CAG: bid 0.19→0.34 (+15c) [scalp]
21:32:51.405 [GOAL] O0.5: bid 0.60→0.98 (+38c) [hold_bond]
21:33:53.041 [VAR]  O0.5: peak 0.98→0.75 (-23c)   ← FALSE (old logic)
```

With **bond-spoof filter** (ask ≥95¢ + wide spread + thin bid):

```
21:33:53.041 [SPOOF] O0.5: bid 0.75 x8 ask 0.99 (-23c from peak, bonded)
```

No VAR alert. Hold position.

---

## P&L impact (per contract, paper)

### ML-CAG scalp (bid+1¢ entry)

- Entry: 35¢ at 21:32:45
- Exit: 42¢ at 21:32:54 (+7¢ target hit in ~9s)
- **P&L: +7¢**

### O0.5 hold_bond (entry ~99¢ at goal)

| Strategy | Exit | P&L | Notes |
|----------|------|-----|-------|
| Naive VAR exit @ 75¢ | 75¢ | **−24¢** | What old alert would cause |
| With spoof filter | Hold | **0¢** (stays bonded) | Correct — goal stood |
| Hold to resolution | 99¢ | **0¢** | Already at bond |

---

## Rule fix implemented

`is_bond_spoof_bid()` in `exit_engine.py` — suppress VAR exit/alert when:

1. Peak was bonded (≥95¢)
2. Ask still ≥95¢ (market hasn't repriced down)
3. Bid dropped ≥10¢ below ask (wide spread)
4. Bid qty ≤100 contracts (thin / spoof)

Wired into:

- `goal_signal._check_var_revert()` → emits `SpoofBidNotice` (amber) instead of `VarRevertAlert` (red)
- `auto_trader.on_book()` → passes ask + bid_qty to `check_exit()`
- UI → amber "SPOOF BID?" banner, notes pad log

---

## Session data notes

- O0.5 (`TOTAL-1`) was monitored live (goal signal + `books_long.csv`) but not in `session.json` ticker list — added at runtime via UI.
- First 75¢ spoof at 21:33:25 had **no ask** in the feed tick; detector couldn't classify it until ask returned at 21:33:53.
- No manual sportsbook clicks logged (`events.csv` empty) — this session was pure Kalshi tape analysis.

---

## Takeaways

1. **Bonded markets need bid+ask context** — bid-only collapse is not enough for VAR detection.
2. **75¢ on a 99¢-ask O0.5 after a goal** = someone fishing / spoofing, not review.
3. **hold_bond positions should not panic-exit** on thin lowball bids when ask confirms the outcome.
4. **ML line led O0.5** by ~6s on this goal — multi-line lead-lag is real and tradeable on CAG scalp.
