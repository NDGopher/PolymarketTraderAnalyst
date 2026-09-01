# Fill analysis: 20260901_195418_TEST

Target size: **100 contracts** at signal bid (join queue, not bid+1).

Kalshi almost always shows **500** at the jump price — that is the house/MM layer.
Joining that bid puts you behind it. Fills happen when sellers hit the stack or you bid +1¢.

| Time | Ticker | Entry | Top bid qty | 3-lvl bid | Spread | Mode | Verdict |
|------|--------|-------|-------------|-----------|--------|------|---------|
| 19:56:05 | 26SEP01WHUWOL-4 | 90¢ | 502 | 502 | 9¢ | `hold_bond` | back of queue — partial/none likely at join-bid |
| | | | | | | | _bid lifted to 91c within 5s_ |
| 19:56:05 | 26SEP01WHUWOL-5 | 64¢ | 500 | 500 | 12¢ | `scalp` | back of queue — partial/none likely at join-bid |
| | | | | | | | _bid lifted to 65c within 5s_ |
| 19:57:55 | 26SEP01FCZYB-6 | 60¢ | 500 | 500 | 17¢ | `scalp` | back of queue — partial/none likely at join-bid |
| | | | | | | | _qty at 60c fell 500->490 in 5s_ |
| 20:06:08 | 26SEP01FCZYB-6 | 46¢ | 500 | 500 | 17¢ | `scalp` | back of queue — partial/none likely at join-bid |
| 20:07:30 | 26SEP01WHUWOL-5 | 88¢ | 500 | 500 | 9¢ | `hold_bond` | back of queue — partial/none likely at join-bid |
| | | | | | | | _bid lifted to 90c within 5s_ |
| 20:13:50 | 26SEP01BCSOU-3 | 58¢ | 500 | 500 | 10¢ | `scalp` | back of queue — partial/none likely at join-bid |
| | | | | | | | _bid lifted to 62c within 5s_ |
| 20:14:51 | 26SEP01FCZYB-6 | 80¢ | 500 | 500 | 15¢ | `var_watch` | back of queue — partial/none likely at join-bid |
| | | | | | | | _bid lifted to 81c within 5s_ |

## Practical sizing

- **Join bid at signal:** assume 0–partial fill unless top qty < 50
- **Bid +1¢:** better fill odds; costs 1¢ more
- **100 contracts:** fine on liquid EFL lines; reduce on Swiss/thin books
- **Penalty reviews:** often no ≥10¢ bid jump — green box may not fire (expected)
