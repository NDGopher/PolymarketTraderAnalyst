# Exit backtest: 20260901_195418_TEST

Entry assumption: **+1c** on signal bid

## Trade 1: 26SEP01WHUWOL-4 @ 2026-09-01T19:56:05
- Entry: **91¢** (signal 90¢) | jump +11¢ | mode: `hold_bond`
- Markouts: +15s: 98¢ (+7¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 98¢ @ 17s | **+7¢** | limit fill @ 98c |
| hold_bond | 98¢ @ 17s | **+7¢** | bond @ 98c |
| time_collar_20s | 98¢ @ 17s | **+7¢** | scalp limit +7c |
| recommended | 98¢ @ 17s | **+7¢** | bond @ 98c |

## Trade 2: 26SEP01WHUWOL-5 @ 2026-09-01T19:56:05
- Entry: **65¢** (signal 64¢) | jump +21¢ | mode: `scalp`
- Markouts: +15s: 73¢ (+8¢) | +20s: 73¢ (+8¢) | +25s: 73¢ (+8¢) | +30s: 74¢ (+9¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 72¢ @ 13s | **+7¢** | limit fill @ 72c |
| hold_bond | 77¢ @ 120s | **+12¢** | held 120s |
| time_collar_20s | 72¢ @ 13s | **+7¢** | scalp limit +7c |
| recommended | 72¢ @ 13s | **+7¢** | scalp limit +7c |

## Trade 3: 26SEP01FCZYB-6 @ 2026-09-01T19:57:55
- Entry: **61¢** (signal 60¢) | jump +20¢ | mode: `scalp`
- Markouts: +15s: 41¢ (-20¢) | +20s: 41¢ (-20¢) | +25s: 41¢ (-20¢) | +30s: 40¢ (-21¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 40¢ @ 45s | **-21¢** | time stop 45s |
| hold_bond | 36¢ @ 120s | **-25¢** | held 120s |
| time_collar_20s | 41¢ @ 20s | **-20¢** | stall @ 20s (peak 61c, bid 41c) |
| recommended | 41¢ @ 20s | **-20¢** | stall @ 20s (peak 61c, bid 41c) |

## Trade 4: 26SEP01FCZYB-6 @ 2026-09-01T20:06:08
- Entry: **47¢** (signal 46¢) | jump +20¢ | mode: `scalp`
- Markouts: +15s: 53¢ (+6¢) | +20s: 55¢ (+8¢) | +25s: 56¢ (+9¢) | +30s: 56¢ (+9¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 54¢ @ 16s | **+7¢** | limit fill @ 54c |
| hold_bond | 59¢ @ 120s | **+12¢** | held 120s |
| time_collar_20s | 54¢ @ 16s | **+7¢** | scalp limit +7c |
| recommended | 54¢ @ 16s | **+7¢** | scalp limit +7c |

## Trade 5: 26SEP01WHUWOL-5 @ 2026-09-01T20:07:30
- Entry: **89¢** (signal 88¢) | jump +17¢ | mode: `hold_bond`

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 92¢ @ 45s | **+3¢** | time stop 45s |
| hold_bond | 92¢ @ 120s | **+3¢** | held 120s |
| time_collar_20s | 92¢ @ 45s | **+3¢** | time stop 45s |
| recommended | 92¢ @ 120s | **+3¢** | held 120s |

## Trade 6: 26SEP01BCSOU-3 @ 2026-09-01T20:13:50
- Entry: **59¢** (signal 58¢) | jump +18¢ | mode: `scalp`
- Markouts: +15s: 64¢ (+5¢) | +20s: 64¢ (+5¢) | +25s: 66¢ (+7¢) | +30s: 68¢ (+9¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 66¢ @ 24s | **+7¢** | limit fill @ 66c |
| hold_bond | 72¢ @ 120s | **+13¢** | held 120s |
| time_collar_20s | 66¢ @ 24s | **+7¢** | scalp limit +7c |
| recommended | 66¢ @ 24s | **+7¢** | scalp limit +7c |

## Trade 7: 26SEP01FCZYB-6 @ 2026-09-01T20:14:51
- Entry: **81¢** (signal 80¢) | jump +31¢ | mode: `var_watch`
- Markouts: +15s: 82¢ (+1¢) | +20s: 83¢ (+2¢) | +25s: 81¢ (+0¢) | +30s: 81¢ (+0¢)

| Strategy | Exit | P&L | Reason |
|----------|------|-----|--------|
| limit_+7c | 49¢ @ 45s | **-32¢** | time stop 45s |
| hold_bond | 43¢ @ 120s | **-38¢** | held 120s |
| time_collar_20s | 83¢ @ 20s | **+2¢** | stall @ 20s (peak 84c, bid 83c) |
| var_watch_collar | 81¢ @ 25s | **+0¢** | VAR limbo @ 25s (peak 84c, bid 81c) |
| recommended | 81¢ @ 25s | **+0¢** | VAR limbo @ 25s (peak 84c, bid 81c) |

## Session totals (per contract)

| Strategy | Total P&L |
|----------|-----------|
| limit_+7c | **-22¢** ($-0.22) |
| hold_bond | **-16¢** ($-0.16) |
| time_collar_20s | **+13¢** ($+0.13) |
| var_watch_collar | **+0¢** ($+0.00) |
| recommended | **+11¢** ($+0.11) |

### Notes
- Entry assumes fill at signal bid (queue risk not modeled).
- `time_collar_20s`: exit at +20s if bid hasn't made new high or gained ≥3¢.
- `var_watch_collar`: at +25s exit if peak <88¢ and bid ≤ entry+3¢; trailing -8¢ from peak.
- Not every line reaches 95¢ — time collar lets mid-price winners run via +7¢ limit.
