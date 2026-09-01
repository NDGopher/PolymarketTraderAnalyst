# Exit backtest: 20260901_195418_TEST

Entry assumption: **join bid** on signal bid

## Trade 1: 26SEP01WHUWOL-4 @ 2026-09-01T19:56:05
- Entry: **90¢** (signal 90¢) | jump +11¢ | mode: `hold_bond`
- Markouts: +15s: 98¢ (+8¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 97¢ @ 17s | **+7¢** | limit fill @ 97c |
| hold_bond | 98¢ @ 17s | **+8¢** | bond @ 98c |
| time_collar_20s | 97¢ @ 17s | **+7¢** | scalp limit +7c |
| recommended | 98¢ @ 17s | **+8¢** | bond @ 98c |

## Trade 2: 26SEP01WHUWOL-5 @ 2026-09-01T19:56:05
- Entry: **64¢** (signal 64¢) | jump +21¢ | mode: `scalp`
- Markouts: +15s: 73¢ (+9¢) | +20s: 73¢ (+9¢) | +25s: 73¢ (+9¢) | +30s: 74¢ (+10¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 71¢ @ 6s | **+7¢** | limit fill @ 71c |
| hold_bond | 77¢ @ 120s | **+13¢** | held 120s |
| time_collar_20s | 71¢ @ 6s | **+7¢** | scalp limit +7c |
| recommended | 71¢ @ 6s | **+7¢** | scalp limit +7c |

## Trade 3: 26SEP01FCZYB-6 @ 2026-09-01T19:57:55
- Entry: **60¢** (signal 60¢) | jump +20¢ | mode: `scalp`
- Markouts: +15s: 41¢ (-19¢) | +20s: 41¢ (-19¢) | +25s: 41¢ (-19¢) | +30s: 40¢ (-20¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 40¢ @ 45s | **-20¢** | time stop 45s |
| hold_bond | 36¢ @ 120s | **-24¢** | held 120s |
| time_collar_20s | 41¢ @ 20s | **-19¢** | stall @ 20s (peak 60c, bid 41c) |
| recommended | 41¢ @ 20s | **-19¢** | stall @ 20s (peak 60c, bid 41c) |

## Trade 4: 26SEP01FCZYB-6 @ 2026-09-01T20:06:08
- Entry: **46¢** (signal 46¢) | jump +20¢ | mode: `scalp`
- Markouts: +15s: 53¢ (+7¢) | +20s: 55¢ (+9¢) | +25s: 56¢ (+10¢) | +30s: 56¢ (+10¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 53¢ @ 12s | **+7¢** | limit fill @ 53c |
| hold_bond | 59¢ @ 120s | **+13¢** | held 120s |
| time_collar_20s | 53¢ @ 12s | **+7¢** | scalp limit +7c |
| recommended | 53¢ @ 12s | **+7¢** | scalp limit +7c |

## Trade 5: 26SEP01WHUWOL-5 @ 2026-09-01T20:07:30
- Entry: **88¢** (signal 88¢) | jump +17¢ | mode: `hold_bond`

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 92¢ @ 45s | **+4¢** | time stop 45s |
| hold_bond | 92¢ @ 120s | **+4¢** | held 120s |
| time_collar_20s | 92¢ @ 45s | **+4¢** | time stop 45s |
| recommended | 92¢ @ 120s | **+4¢** | held 120s |

## Trade 6: 26SEP01BCSOU-3 @ 2026-09-01T20:13:50
- Entry: **58¢** (signal 58¢) | jump +18¢ | mode: `scalp`
- Markouts: +15s: 64¢ (+6¢) | +20s: 64¢ (+6¢) | +25s: 66¢ (+8¢) | +30s: 68¢ (+10¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 65¢ @ 24s | **+7¢** | limit fill @ 65c |
| hold_bond | 72¢ @ 120s | **+14¢** | held 120s |
| time_collar_20s | 65¢ @ 24s | **+7¢** | scalp limit +7c |
| recommended | 65¢ @ 24s | **+7¢** | scalp limit +7c |

## Trade 7: 26SEP01FCZYB-6 @ 2026-09-01T20:14:51
- Entry: **80¢** (signal 80¢) | jump +31¢ | mode: `var_watch`
- Markouts: +15s: 82¢ (+2¢) | +20s: 83¢ (+3¢) | +25s: 81¢ (+1¢) | +30s: 81¢ (+1¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 49¢ @ 45s | **-31¢** | time stop 45s |
| hold_bond | 43¢ @ 120s | **-37¢** | held 120s |
| time_collar_20s | 49¢ @ 45s | **-31¢** | time stop 45s |
| var_watch_collar | 81¢ @ 25s | **+1¢** | VAR limbo @ 25s (peak 84c, bid 81c) |
| recommended | 81¢ @ 25s | **+1¢** | VAR limbo @ 25s (peak 84c, bid 81c) |

## Session totals (per contract)

| Strategy | Total P&L |
|----------|-----------|
| limit_+7c | **-19¢** ($-0.19) |
| hold_bond | **-9¢** ($-0.09) |
| time_collar_20s | **-18¢** ($-0.18) |
| var_watch_collar | **+1¢** ($+0.01) |
| recommended | **+15¢** ($+0.15) |

### Notes
- Entry assumes fill at signal bid (queue risk not modeled).
- `time_collar_20s`: exit at +20s if bid hasn't made new high or gained ≥3¢.
- `var_watch_collar`: at +25s exit if peak <88¢ and bid ≤ entry+3¢; trailing -8¢ from peak.
- Not every line reaches 95¢ — time collar lets mid-price winners run via +7¢ limit.
