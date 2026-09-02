# Fill verification: 20260901_210900_TEST2-MELGAR-GRAU

Target size: **50 contracts**

Queue risk: ~500 MM top qty typical on Kalshi soccer; this analysis checks whether
price lifts or queue consumes enough to suggest fill.

| Time | Ticker | Signal | Mode | Strategy | Verdict | Reason |
|------|--------|--------|------|----------|---------|--------|
| 21:32:45 | 26AUG31CAGMEL-CAG | 34c | `scalp` | join_bid | ✅ FILL | bid lifted past 34c to 35c |
| 21:32:45 | 26AUG31CAGMEL-CAG | 34c | `scalp` | bid_plus_1 | ✅ FILL | queue consumed 2342 contracts |
| 21:32:45 | 26AUG31CAGMEL-CAG | 34c | `scalp` | lift_ask | ✅ FILL | lifted ask @ 40c |
| 21:32:51 | 26AUG31CAGMEL-1 | 98c | `hold_bond` | join_bid | ✅ FILL | queue consumed 75 contracts |
| 21:32:51 | 26AUG31CAGMEL-1 | 98c | `hold_bond` | bid_plus_1 | ❌ NO_FILL | deep queue (249ct ahead), no lift |
| 21:32:51 | 26AUG31CAGMEL-1 | 98c | `hold_bond` | lift_ask | ✅ FILL | lifted ask @ 99c |

## Summary

- **2** goal signals analyzed
- **2** would have filled (at least one strategy)
- **0** partial fill likely
- **0** unlikely to fill at join-bid

### P&L implications

- Backtest P&L should only count FILL or conservative PARTIAL
- NO_FILL signals should be excluded from realized P&L
