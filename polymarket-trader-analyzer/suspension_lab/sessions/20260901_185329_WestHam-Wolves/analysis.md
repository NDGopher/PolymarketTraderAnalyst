# Suspension Lab Analysis: WestHam-Wolves

Session: `20260901_185329_WestHam-Wolves`
Started: 2026-09-01T18:53:29.862000+00:00
Tickers tracked: 4
Primary analysis ticker (most movement): `KXEFLCHAMPIONSHIPTOTAL-26SEP01WHUWOL-3`
Book tape rows: 8,057 (~1611s at 200ms)
Manual events: 6

## Sportsbook click timeline

| Time | Event | B365 | FD | DK | Primary mid | Spread | Wide? |
|------|-------|------|----|----|-------------|--------|-------|
| 19:19:03.596 | B365_DOWN | DOWN | UP | UP | 0.55 | 9c | no |
| 19:19:03.971 | DRAFTKINGS_DOWN | DOWN | UP | DOWN | 0.55 | 9c | no |
| 19:19:08.428 | B365_UP | UP | UP | DOWN | 0.54 | 8c | no |
| 19:19:09.300 | FANDUEL_DOWN | UP | DOWN | DOWN | 0.54 | 7c | no |
| 19:19:20.908 | DRAFTKINGS_UP | UP | DOWN | UP | 0.56 | 5c | no |
| 19:20:23.956 | FANDUEL_UP | UP | UP | UP | 0.58 | 1c | no |

## Suspension timing (your clicks)

- **bet365 DOWN:** 19:19:03.596
- **DraftKings DOWN:** 19:19:03.971 (+0.38s vs b365 first down)
- **FanDuel DOWN:** 19:19:09.300 (+5.70s vs b365 first down)
- **bet365 UP:** 19:19:08.428 (+4.83s vs b365 first down)
- **DraftKings UP:** 19:19:20.908 (+17.31s vs b365 first down)
- **FanDuel UP:** 19:19:08.428 (+4.83s vs b365 first down)
- **b365 → DK lag:** 0.38s
- **b365 → FD lag:** 5.70s
- **b365 → FD reopen lag:** 0.00s

## Kalshi mid jumps (from 200ms tape, no clicks needed)

| Time | Mid move | Spread | Wide? |
|------|----------|--------|-------|
| 18:53:32.753 | 0.28 → 0.58 (+30c) | 60c | YES |
| 18:53:35.968 | 0.76 → 0.56 (-19c) | 5c | no |
| 18:54:32.768 | 0.55 → 0.65 (+10c) | 22c | YES |
| 18:54:37.196 | 0.64 → 0.56 (-7c) | 5c | no |
| 18:54:47.474 | 0.55 → 0.62 (+8c) | 16c | YES |
| 18:55:41.237 | 0.62 → 0.57 (-5c) | 5c | no |
| 18:55:46.875 | 0.62 → 0.56 (-6c) | 2c | no |
| 18:57:03.241 | 0.53 → 0.61 (+8c) | 18c | YES |
| 18:57:14.717 | 0.61 → 0.53 (-8c) | 2c | no |
| 18:59:42.265 | 0.52 → 0.62 (+10c) | 22c | YES |
| 18:59:49.719 | 0.62 → 0.54 (-8c) | 3c | no |
| 19:01:20.413 | 0.51 → 0.60 (+10c) | 21c | YES |
| 19:02:20.623 | 0.62 → 0.54 (-9c) | 5c | no |
| 19:13:14.482 | 0.40 → 0.48 (+8c) | 24c | YES |
| 19:13:24.158 | 0.51 → 0.37 (-14c) | 2c | no |

## Lag analysis: books vs Kalshi

- First Kalshi jump (>=5c): **18:53:32.753** (0.28 → 0.58)
- vs your **b365 DOWN** click: **-1530.84s** (negative = Kalshi moved before you clicked)
- vs your **DK DOWN** click: **-1531.22s**

## Markouts after suspension clicks (primary ticker)

### B365_DOWN @ 19:19:03.596
- At click: mid **0.55**, spread **9c**, wide=no, suggest bid **0.5200**
- Markouts: +1s: 0.55 (+0c, spread 9c) | +3s: 0.55 (+0c, spread 9c) | +5s: 0.54 (-1c, spread 8c) | +10s: 0.54 (-1c, spread 8c) | +30s: 0.56 (+1c, spread 5c)

### DRAFTKINGS_DOWN @ 19:19:03.971
- At click: mid **0.55**, spread **9c**, wide=no, suggest bid **0.5200**
- Markouts: +1s: 0.55 (+0c, spread 9c) | +3s: 0.55 (+0c, spread 9c) | +5s: 0.54 (-1c, spread 8c) | +10s: 0.55 (+0c, spread 7c) | +30s: 0.56 (+1c, spread 5c)

### FANDUEL_DOWN @ 19:19:09.300
- At click: mid **0.54**, spread **7c**, wide=no, suggest bid **0.5200**
- Markouts: +1s: 0.54 (+0c, spread 7c) | +3s: 0.54 (+0c, spread 7c) | +5s: 0.55 (+1c, spread 7c) | +10s: 0.56 (+2c, spread 5c) | +30s: 0.56 (+3c, spread 4c)

## Tradeability at suspension

At **b365 DOWN**: spread **9c**, wide=no — tight book, untradeable flag=no
- Strategy: could consider bidding near mid or lifting ask if liquidity exists

## Summary

1. **Book order:** b365 first, DK 375000ms later, FD 5704000ms after b365.
3. **Kalshi:** largest move +30c at 18:53:32.753 (0.28 → 0.58).
