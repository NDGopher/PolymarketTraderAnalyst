# polika72 — Additional Quantitative Breakdown

Computed from full unique-fill history (19,978 trades · 5,422 markets).
Generated 2026-08-25T16:23:05.556297+00:00

## 1. Win rate & average PnL by slice

### Hold time

| Bucket | N | Win rate | Total PnL | Avg PnL | Median PnL |
|---|---:|---:|---:|---:|---:|
| <30s | 717 | 74.9% | $2,351.19 | $3.28 | $0.00 |
| 30s-2m | 3234 | 86.7% | $42,763.37 | $13.22 | $5.44 |
| 2-5m | 731 | 64.5% | $2,609.46 | $3.57 | $1.33 |
| 5-15m | 291 | 59.5% | $442.89 | $1.52 | $1.70 |
| 15m+ | 449 | 75.4% | $13,742.46 | $30.61 | $11.51 |

**Read:** The engine is **30s–2m** ($42.8k, 86.7% WR). **15m+** is fewer markets but highest avg ($30.61) — the campaign/impulse-hold tail.

### Entry price band (avg buy)

| Band | N | Win rate | Total PnL | Avg PnL | Median PnL |
|---|---:|---:|---:|---:|---:|
| 0-20¢ | 909 | 71.0% | $4,517.97 | $4.97 | $1.04 |
| 20-40¢ | 1285 | 77.2% | $15,230.70 | $11.85 | $4.65 |
| 40-60¢ | 1494 | 82.1% | $22,820.93 | $15.28 | $4.65 |
| 60-80¢ | 1463 | 86.4% | $17,974.32 | $12.29 | $3.72 |
| 80-100¢ | 271 | 78.4% | $1,365.45 | $5.04 | $1.17 |

**Read:** Best total + avg in **40–60¢**; highest WR in **60–80¢**. Tails (0–20 / 80–100) are weaker per trade.

### Over/Under vs Yes/No vs Other

| Family | N | Win rate | Total PnL | Avg PnL | Median PnL |
|---|---:|---:|---:|---:|---:|
| Over/Under | 3543 | 77.9% | $40,676.84 | $11.48 | $3.39 |
| Yes/No moneyline | 1743 | 84.3% | $21,062.80 | $12.08 | $4.50 |
| Other | 136 | 87.2% | $169.73 | $1.25 | $0.54 |

**Read:** O/U is the volume engine ($40.7k). Yes/No moneylines are fewer markets but **higher WR (84.3%)** and similar avg PnL.

## 2. Campaign / re-entry behavior

Definition: inventory returns to flat (~0 net shares), then a later buy opens a new long = re-entry / campaign.

- Markets with ≥1 re-entry: **317** (5.85% of markets)
- Avg entries when campaigning: **2.09**
- Campaign markets: PnL **$9,675.13**, avg **$30.52**, WR **82.0%**
- Single-entry markets: PnL **$52,234.23**, avg **$10.23**, WR **73.5%**

Campaigns are rare (~6%) but **~3× higher avg PnL** and better WR than one-and-done.

### Best multi-leg examples

#### Example 1: Odense BK vs. Randers FC: O/U 2.5
PnL $358.54 · hold 4262s · entries 3 · fills 45 · avg entry 0.5035 → exit 0.7144

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-04-19T12:19:02+00:00 | BUY | Over | 265.2 | 0.45 | taker | 265.2 | ENTRY#1 |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 263.68 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 262.17 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 260.65 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 259.14 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 257.62 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 256.11 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 254.59 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 253.08 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 251.56 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 250.05 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 248.53 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 247.02 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 245.5 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 243.99 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 242.47 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 240.96 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 239.44 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 237.93 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 236.41 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 234.9 |  |
| 2026-04-19T12:20:04+00:00 | SELL | Over | 1.52 | 0.66 | maker | 233.38 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 2.27 | 0.66 | maker | 231.11 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 2.27 | 0.66 | maker | 228.84 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 227.32 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 225.81 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 224.29 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 222.78 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 221.26 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 219.75 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 218.23 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 216.72 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 215.2 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 213.68 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 212.17 |  |
| 2026-04-19T12:20:06+00:00 | SELL | Over | 1.52 | 0.66 | maker | 210.65 |  |
| 2026-04-19T12:20:24+00:00 | SELL | Over | 210.4 | 0.65 | maker | 0.25 | FLAT |
| 2026-04-19T13:18:30+00:00 | BUY | Over | 329.7 | 0.35 | taker | 329.95 | ENTRY#2 |
| 2026-04-19T13:20:08+00:00 | SELL | Over | 41.77 | 0.6 | maker | 288.19 |  |
| 2026-04-19T13:20:10+00:00 | SELL | Over | 3.33 | 0.6 | maker | 284.85 |  |

#### Example 2: Odense BK vs. Randers FC: O/U 3.5
PnL $334.65 · hold 5204s · entries 2 · fills 37 · avg entry 0.2289 → exit 0.4104

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-04-19T12:19:02+00:00 | BUY | Over | 29.16 | 0.24 | taker | 29.16 | ENTRY#1 |
| 2026-04-19T12:19:02+00:00 | BUY | Over | 225.9 | 0.24 | taker | 255.06 |  |
| 2026-04-19T12:19:06+00:00 | BUY | Over | 32.54 | 0.27 | maker | 287.6 |  |
| 2026-04-19T12:22:02+00:00 | SELL | Over | 52.0 | 0.37 | maker | 235.6 |  |
| 2026-04-19T12:22:26+00:00 | SELL | Over | 2.78 | 0.36 | maker | 232.82 |  |
| 2026-04-19T12:23:08+00:00 | SELL | Over | 82.6 | 0.34 | maker | 150.22 |  |
| 2026-04-19T12:23:08+00:00 | SELL | Over | 9.5 | 0.34 | maker | 140.72 |  |
| 2026-04-19T12:23:10+00:00 | SELL | Over | 117.65 | 0.34 | maker | 23.08 |  |
| 2026-04-19T12:28:48+00:00 | SELL | Over | 5.0 | 0.3 | taker | 18.08 |  |
| 2026-04-19T12:31:48+00:00 | SELL | Over | 5.0 | 0.3 | taker | 13.08 |  |
| 2026-04-19T13:18:30+00:00 | BUY | Over | 222.2 | 0.13 | taker | 235.28 |  |
| 2026-04-19T13:18:32+00:00 | BUY | Over | 222.2 | 0.13 | taker | 457.48 |  |
| 2026-04-19T13:18:34+00:00 | BUY | Over | 222.2 | 0.15 | maker | 679.68 |  |
| 2026-04-19T13:20:24+00:00 | SELL | Over | 58.26 | 0.24 | maker | 621.42 |  |
| 2026-04-19T13:20:24+00:00 | SELL | Over | 80.49 | 0.24 | maker | 540.92 |  |
| 2026-04-19T13:20:24+00:00 | SELL | Over | 83.33 | 0.24 | maker | 457.59 |  |
| 2026-04-19T13:21:06+00:00 | SELL | Over | 222.1 | 0.25 | taker | 235.49 |  |
| 2026-04-19T13:21:06+00:00 | SELL | Over | 13.4 | 0.2425 | taker | 222.09 |  |
| 2026-04-19T13:21:10+00:00 | SELL | Over | 208.7 | 0.22 | maker | 13.39 |  |
| 2026-04-19T13:24:04+00:00 | SELL | Over | 8.33 | 0.24 | taker | 5.06 |  |
| 2026-04-19T13:28:48+00:00 | BUY | Over | 254.16 | 0.2297 | taker | 259.22 |  |
| 2026-04-19T13:28:48+00:00 | BUY | Over | 254.16 | 0.23 | taker | 513.38 |  |
| 2026-04-19T13:28:48+00:00 | BUY | Over | 99.85 | 0.2396 | taker | 613.23 |  |
| 2026-04-19T13:28:50+00:00 | BUY | Over | 154.33 | 0.24 | maker | 767.56 |  |
| 2026-04-19T13:29:54+00:00 | SELL | Over | 13.73 | 0.51 | maker | 753.83 |  |
| 2026-04-19T13:29:54+00:00 | SELL | Over | 2.96 | 0.51 | maker | 750.87 |  |
| 2026-04-19T13:30:14+00:00 | SELL | Over | 100.0 | 0.5 | maker | 650.87 |  |
| 2026-04-19T13:30:24+00:00 | SELL | Over | 153.9 | 0.49 | maker | 496.97 |  |
| 2026-04-19T13:30:24+00:00 | SELL | Over | 254.0 | 0.49 | maker | 242.97 |  |
| 2026-04-19T13:30:24+00:00 | SELL | Over | 237.2 | 0.49 | maker | 5.77 |  |
| 2026-04-19T13:31:18+00:00 | SELL | Over | 5.6 | 0.51 | maker | 0.17 | FLAT |
| 2026-04-19T13:44:38+00:00 | BUY | Over | 92.4 | 0.66 | maker | 92.57 | ENTRY#2 |
| 2026-04-19T13:44:38+00:00 | BUY | Over | 32.99 | 0.66 | maker | 125.56 |  |
| 2026-04-19T13:45:40+00:00 | SELL | Over | 28.89 | 0.99 | maker | 96.67 |  |
| 2026-04-19T13:45:46+00:00 | SELL | Over | 2.11 | 0.99 | maker | 94.56 |  |
| 2026-04-19T13:45:46+00:00 | SELL | Over | 30.69 | 0.99 | maker | 63.87 |  |
| 2026-04-19T13:45:46+00:00 | SELL | Over | 63.41 | 0.99 | maker | 0.46 | FLAT |

#### Example 3: Iraq vs. Norway: Draw at halftime?
PnL $333.67 · hold 507s · entries 2 · fills 6 · avg entry 0.2439 → exit 0.8618

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-06-16T22:43:25+00:00 | BUY | No | 288.45 | 0.21 | taker | 288.45 | ENTRY#1 |
| 2026-06-16T22:43:25+00:00 | BUY | No | 288.45 | 0.21 | taker | 576.9 |  |
| 2026-06-16T22:44:07+00:00 | SELL | No | 288.3 | 0.86 | taker | 288.6 |  |
| 2026-06-16T22:44:07+00:00 | SELL | No | 288.3 | 0.8637 | taker | 0.3 | FLAT |
| 2026-06-16T22:51:46+00:00 | BUY | Yes | 58.8 | 0.51 | maker | 59.1 | ENTRY#2 |
| 2026-06-16T22:51:52+00:00 | BUY | Yes | 14.7 | 0.51 | maker | 73.8 |  |

#### Example 4: Iraq vs. Norway: O/U 3.5
PnL $294.08 · hold 528s · entries 2 · fills 10 · avg entry 0.7411 → exit 0.8442

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-06-16T22:43:25+00:00 | BUY | Over | 696.04 | 0.64 | maker | 696.04 | ENTRY#1 |
| 2026-06-16T22:43:25+00:00 | BUY | Over | 857.8 | 0.64 | maker | 1553.84 |  |
| 2026-06-16T22:43:25+00:00 | BUY | Over | 161.76 | 0.64 | maker | 1715.6 |  |
| 2026-06-16T22:43:56+00:00 | SELL | Over | 857.7 | 0.84 | taker | 857.9 |  |
| 2026-06-16T22:43:56+00:00 | SELL | Over | 857.7 | 0.84 | taker | 0.2 | FLAT |
| 2026-06-16T22:51:47+00:00 | BUY | Over | 319.55 | 0.88 | maker | 319.75 | ENTRY#2 |
| 2026-06-16T22:51:47+00:00 | BUY | Over | 623.85 | 0.88 | maker | 943.6 |  |
| 2026-06-16T22:51:50+00:00 | BUY | Over | 304.3 | 0.88 | maker | 1247.9 |  |
| 2026-06-16T22:52:13+00:00 | SELL | Over | 623.7 | 0.85 | taker | 624.2 |  |
| 2026-06-16T22:52:13+00:00 | SELL | Over | 623.7 | 0.85 | taker | 0.5 | FLAT |

#### Example 5: Will FC Nantes win on 2026-04-19?
PnL $240.79 · hold 6336s · entries 2 · fills 7 · avg entry 0.4057 → exit 0.7162

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-04-19T15:24:14+00:00 | BUY | Yes | 129.16 | 0.48 | maker | 129.16 | ENTRY#1 |
| 2026-04-19T15:24:14+00:00 | BUY | Yes | 129.18 | 0.48 | maker | 258.34 |  |
| 2026-04-19T15:25:08+00:00 | SELL | Yes | 129.0 | 0.6207 | taker | 129.34 |  |
| 2026-04-19T15:25:08+00:00 | SELL | Yes | 129.0 | 0.62 | taker | 0.34 | FLAT |
| 2026-04-19T15:25:08+00:00 | SELL | Yes | 129.0 | 0.62 | taker | -128.66 |  |
| 2026-04-19T17:09:14+00:00 | BUY | No | 181.73 | 0.3 | taker | 53.07 | ENTRY#2 |
| 2026-04-19T17:09:50+00:00 | SELL | No | 185.6 | 0.9163 | taker | -132.53 |  |

#### Example 6: Gwangju FC vs. FC Anyang: O/U 4.5
PnL $226.58 · hold 2034s · entries 2 · fills 14 · avg entry 0.2406 → exit 0.393

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-04-26T08:10:26+00:00 | BUY | Over | 83.33 | 0.08 | maker | 83.33 | ENTRY#1 |
| 2026-04-26T08:13:42+00:00 | SELL | Over | 83.2 | 0.12 | maker | 0.13 | FLAT |
| 2026-04-26T08:17:56+00:00 | BUY | Over | 28.98 | 0.17 | taker | 29.11 | ENTRY#2 |
| 2026-04-26T08:17:56+00:00 | BUY | Over | 28.98 | 0.17 | taker | 58.09 |  |
| 2026-04-26T08:17:56+00:00 | BUY | Over | 28.98 | 0.17 | taker | 87.07 |  |
| 2026-04-26T08:19:12+00:00 | SELL | Over | 28.4 | 0.35 | maker | 58.67 |  |
| 2026-04-26T08:19:12+00:00 | SELL | Over | 30.4 | 0.34 | maker | 28.27 |  |
| 2026-04-26T08:42:54+00:00 | BUY | Over | 47.38 | 0.36 | taker | 75.65 |  |
| 2026-04-26T08:42:54+00:00 | BUY | Over | 58.65 | 0.3575 | taker | 134.3 |  |
| 2026-04-26T08:42:54+00:00 | BUY | Over | 58.66 | 0.36 | taker | 192.96 |  |
| 2026-04-26T08:44:00+00:00 | SELL | Over | 60.9 | 0.63 | maker | 132.06 |  |
| 2026-04-26T08:44:10+00:00 | SELL | Over | 9.0 | 0.65 | taker | 123.06 |  |
| 2026-04-26T08:44:16+00:00 | SELL | Over | 15.87 | 0.63 | maker | 107.18 |  |
| 2026-04-26T08:44:20+00:00 | SELL | Over | 21.22 | 0.63 | maker | 85.96 |  |

#### Example 7: FC Internazionale Milano vs. Cagliari Calcio: O/U 2.5
PnL $220.53 · hold 240s · entries 2 · fills 7 · avg entry 0.351 → exit 0.6701

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-04-17T19:59:42+00:00 | BUY | Over | 23.33 | 0.24 | taker | 23.33 | ENTRY#1 |
| 2026-04-17T20:00:30+00:00 | SELL | Over | 8.01 | 0.43 | maker | 15.32 |  |
| 2026-04-17T20:00:48+00:00 | SELL | Over | 2.62 | 0.42 | maker | 12.7 |  |
| 2026-04-17T20:00:50+00:00 | SELL | Over | 11.17 | 0.42 | maker | 1.53 |  |
| 2026-04-17T20:00:50+00:00 | SELL | Over | 1.71 | 0.42 | maker | -0.18 | FLAT |
| 2026-04-17T20:03:08+00:00 | BUY | Over | 286.1 | 0.36 | taker | 285.92 | ENTRY#2 |
| 2026-04-17T20:03:42+00:00 | SELL | Over | 292.0 | 0.69 | maker | -6.08 |  |

#### Example 8: Chelsea FC vs. Nottingham Forest FC: O/U 3.5
PnL $208.66 · hold 4916s · entries 2 · fills 4 · avg entry 0.3998 → exit 0.5787

| Time | Side | Outcome | Size | Price | Role | Net | Flag |
|---|---|---|---:|---:|---|---:|---|
| 2026-05-04T14:01:52+00:00 | BUY | Over | 305.0 | 0.38 | taker | 305.0 | ENTRY#1 |
| 2026-05-04T14:03:08+00:00 | SELL | Over | 304.9 | 0.5605 | taker | 0.1 | FLAT |
| 2026-05-04T15:21:58+00:00 | BUY | Over | 42.45 | 0.5418 | taker | 42.55 | ENTRY#2 |
| 2026-05-04T15:23:48+00:00 | SELL | Over | 42.3 | 0.71 | maker | 0.25 | FLAT |

## 3. Averaging-down leak

### Strict definition (buy ≥2¢ below VWAP while long)
- Losers with avg-down: **14 / 993 (1.41%)**
- Avg sim improvement on those losers if skipped: **$10.04**
- Total sim improvement on those losers: **$140.54**
- Global FIFO if never do this: $58,092.35 vs $58,487.99 (Δ $-395.63)

### MTM-red definition (buy while last price < VWAP − 0.5¢)
- Losers with red buys: **15 / 993 (1.51%)**
- Winners with red buys: **27 (0.67%)** — dip-buying is common on winners
- Total red-buy USDC on losers: **$319.65**
- Avg/total sim Δ on those losers: **$4.17** / **$62.53**
- Global never-buy-while-red: $58,429.79 vs $58,487.99 (Δ **$-58.20**)

> Global improvement can be negative because buying dips while temporarily red is often the profitable campaign pattern on winners.

**Opinion:** Averaging down is **not** his main leak by frequency. Blindly banning all red buys **destroys** edge globally because profitable campaigns buy dips. Ban only **red buys without a new live event signal**.

## 4. Maker vs Taker

Method: `Data API trades?takerOnly=true vs full history; fills in full but not taker-only = maker`
- Fills: **10,834 maker** / **9,144 taker**

| Leg | Maker % | Taker % | Maker USDC | Taker USDC |
|---|---:|---:|---:|---:|
| Entry (BUYs) | 38.38% | 61.62% | $77,447.15 | $124,336.45 |
| Exit (SELLs) | 49.09% | 50.91% | $127,828.29 | $132,567.80 |

### Per-market dominant pattern

- `enter_taker_exit_maker`: 1723 (34.9%)
- `enter_taker_exit_taker`: 1468 (29.8%)
- `enter_maker_exit_maker`: 1062 (21.5%)
- `enter_maker_exit_taker`: 680 (13.8%)

**Read:** He most often **enters as taker** (61.6% of buy volume) and **exits mixed**, with the single most common pattern **enter_taker → exit_maker** (1,723 markets). That is “hit the impulse, then work asks into strength.”

## 5. Latency / impulse detection

Time from first buy → max favorable price (winners): **p25 44s · median 64s · p75 99s · p90 387s**
When MFE ≥ 10¢: median **61s**, p75 **90s** (n=3256)

- Winners with sells: 3871
- Of which MFE ≥ 10¢: **3256**
- Big move already ≥10¢ within **30s**: 252 (**7.74%** of big moves; **6.51%** of all winners)
- Within **60s**: 1761 (**54.08%** of big moves; **45.49%** of all winners)

**Read:** ~**half of big (≥10¢) excursions peak by 60s**; only ~8% by 30s. He’s fast, but not “sub-second only” — many markouts mature over ~1 minute.

## 6. Risk management

- Max inventory (shares): **6,000.0** on `Netherlands vs. Japan: O/U 4.5` (that market PnL $502.30)
- Max inventory ≈USDC: **$1,484.10** on `Will Club Atlético de Madrid win on 2026-08-23?`
- Worst 10 trades sum: **$-4,429.46** = **16.48%** of all losing-market PnL

| PnL | Hold | Market |
|---:|---:|---|
| $-515.82 | 406s | RC Strasbourg Alsace vs. OGC Nice: O/U 3.5 |
| $-508.72 | 5250s | Melbourne City FC vs. Western Sydney Wanderers FC: O/U 4.5 |
| $-474.32 | 226s | Panama vs. England: Both Teams to Score |
| $-471.20 | 4560s | Paris Saint-Germain FC vs. Liverpool FC: O/U 3.5 |
| $-427.80 | 46s | Will Paris Saint-Germain FC win on 2026-04-22? |
| $-427.77 | 490s | RC Strasbourg Alsace vs. OGC Nice: O/U 4.5 |
| $-416.80 | 74s | Sporting CP vs. Arsenal FC: O/U 2.5 |
| $-414.38 | 490s | UD Las Palmas vs. SD Huesca: O/U 3.5 |
| $-388.13 | 136s | Real Madrid CF vs. Deportivo Alavés: O/U 3.5 |
| $-384.52 | 1410s | Cádiz CF vs. Córdoba CF: O/U 4.5 |

Loser time-to-flat after entry: median **106s**, p75 **204s**, mean **262s**
- Flat within 60s: **26.27%**
- Within 120s: **56.52%**
- Within 5m: **84.11%**
