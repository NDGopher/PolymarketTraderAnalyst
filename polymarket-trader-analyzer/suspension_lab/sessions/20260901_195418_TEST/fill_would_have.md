# Fill verification: 20260901_195418_TEST

Target size: **50 contracts**

Queue risk: ~500 MM top qty typical on Kalshi soccer; this analysis checks whether
price lifts or queue consumes enough to suggest fill.

| Time | Ticker | Signal | Mode | Strategy | Verdict | Reason |
|------|--------|--------|------|----------|---------|--------|
| 19:56:05 | 26SEP01WHUWOL-4 | 90c | `hold_bond` | join_bid | ✅ FILL | bid lifted past 90c to 91c |
| 19:56:05 | 26SEP01WHUWOL-4 | 90c | `hold_bond` | bid_plus_1 | ✅ FILL | queue consumed 451 contracts |
| 19:56:05 | 26SEP01WHUWOL-4 | 90c | `hold_bond` | lift_ask | ✅ FILL | lifted ask @ 99c |
| 19:56:05 | 26SEP01WHUWOL-5 | 64c | `scalp` | join_bid | ✅ FILL | bid lifted past 64c to 65c |
| 19:56:05 | 26SEP01WHUWOL-5 | 64c | `scalp` | bid_plus_1 | ✅ FILL | queue consumed 360 contracts |
| 19:56:05 | 26SEP01WHUWOL-5 | 64c | `scalp` | lift_ask | ✅ FILL | lifted ask @ 76c |
| 19:57:55 | 26SEP01FCZYB-6 | 60c | `scalp` | join_bid | ❌ NO_FILL | deep queue (500ct ahead), no lift |
| 19:57:55 | 26SEP01FCZYB-6 | 60c | `scalp` | bid_plus_1 | ❌ NO_FILL | deep queue (500ct ahead), no lift |
| 19:57:55 | 26SEP01FCZYB-6 | 60c | `scalp` | lift_ask | ✅ FILL | lifted ask @ 79c |
| 20:06:08 | 26SEP01FCZYB-6 | 46c | `scalp` | join_bid | ❌ NO_FILL | deep queue (500ct ahead), no lift |
| 20:06:08 | 26SEP01FCZYB-6 | 46c | `scalp` | bid_plus_1 | ❌ NO_FILL | deep queue (500ct ahead), no lift |
| 20:06:08 | 26SEP01FCZYB-6 | 46c | `scalp` | lift_ask | ✅ FILL | lifted ask @ 67c |
| 20:07:30 | 26SEP01WHUWOL-5 | 88c | `hold_bond` | join_bid | ✅ FILL | bid lifted past 88c to 90c |
| 20:07:30 | 26SEP01WHUWOL-5 | 88c | `hold_bond` | bid_plus_1 | ✅ FILL | bid lifted past 89c to 90c |
| 20:07:30 | 26SEP01WHUWOL-5 | 88c | `hold_bond` | lift_ask | ✅ FILL | lifted ask @ 97c |
| 20:13:50 | 26SEP01BCSOU-3 | 58c | `scalp` | join_bid | ✅ FILL | bid lifted past 58c to 62c |
| 20:13:50 | 26SEP01BCSOU-3 | 58c | `scalp` | bid_plus_1 | ✅ FILL | bid lifted past 59c to 62c |
| 20:13:50 | 26SEP01BCSOU-3 | 58c | `scalp` | lift_ask | ✅ FILL | lifted ask @ 69c |
| 20:14:51 | 26SEP01FCZYB-6 | 80c | `var_watch` | join_bid | ✅ FILL | bid lifted past 80c to 81c |
| 20:14:51 | 26SEP01FCZYB-6 | 80c | `var_watch` | bid_plus_1 | ✅ FILL | queue consumed 464 contracts |
| 20:14:51 | 26SEP01FCZYB-6 | 80c | `var_watch` | lift_ask | ✅ FILL | lifted ask @ 94c |

## Summary

- **7** goal signals analyzed
- **7** would have filled (at least one strategy)
- **0** partial fill likely
- **0** unlikely to fill at join-bid

### P&L implications

- Backtest P&L should only count FILL or conservative PARTIAL
- NO_FILL signals should be excluded from realized P&L
