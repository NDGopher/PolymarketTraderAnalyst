# Kalshi Directional MM Bot — Agent Brief

> For the Cursor agent building the Kalshi bot. User wants **directional flow capture**, not penny scalping.

## Core thesis

Run a **two-layer bot**:
1. **Base MM layer** — quote both sides, inventory skew, merge/flatten (HomeRunHazard DNA)
2. **Directional overlay** — when sharp-book consensus moves, **stop passive quoting and take the slow side of Kalshi**

Edge = being on the right side of **big repricing events**, not earning 1¢ spread.

---

## Priority templates (copy logic, not wallets)

| Priority | Trader | Copy what | Skip what |
|---:|---|---|---|
| 1 | **Consensus steam module** (your idea) | Multi-book move → taker on lagging Kalshi | N/A — build this |
| 2 | **HomeRunHazard** | Split→quote both sides→MERGE, inventory skew, 85% maker | Buy-only without merge on Kalshi |
| 3 | **dbdd4515** (syncing) | Universe scanner, esports+sports, buy+redeem+sell hybrid | 101k market brute force |
| 4 | **DrPufferfish** | Maker bid → sell into strength, asymmetric sizing | Pure taker chase |
| 5 | **equity_16** | Multi-sport live activation, 3s cadence, sports_match focus | $1B vol capital reqs |
| 6 | **kch123 / RN1** | Informed MM on liquid totals, skew before catalysts | Whale clip sizes |
| 7 | **gmpm** | Sports match directional, then went inactive — study winners | Cashflow accounting |

**Do NOT template:** Allezpapa (WC whale), Mysaria (politics HFT), swisstony (oracle infra).

---

## Directional overlay spec (consensus steam)

```yaml
signal:
  sources: [pinnacle, betfair, bet365]  # or odds API aggregator
  poll_interval_ms: 1000-3000           # NOT sub-ms required
  min_books_moved: 2                    # user insight: single book = noise
  min_prob_delta: 0.03                  # 3% implied prob move
  window_seconds: 10                    # moves must cluster in time

action:
  if consensus_over_up and kalshi_mid_lags_fair_by >= 5c:
    cancel_passive_quotes
    taker_buy_over(max_clip)
    work_maker_asks_at fair + 10c
  if false_alarm (books revert within 30s):
    flatten at stop -4c

risk:
  max_directional_usdc_per_match: 500
  max_concurrent_live_matches: 5
  no_scale_in_without_new_consensus
```

**polika72 tape supports chase > fade:** 253 chase-up vs 64 fade-down episodes; median MFE at 64s (54% of big moves within 60s). Premium Sportradar optional, not required for v1.

---

## MM base layer spec (Kalshi)

From HomeRunHazard + inventory guide:
- Quote YES+NO (or Over+Under) when spread ≥ 2¢
- Skew quotes when |net| > soft_cap
- MERGE when paired inventory > threshold
- Pull all quotes on consensus steam signal (avoid getting picked off)
- Cancel before known catalysts (puck drop, kickoff, injury time)

---

## Kalshi-specific notes

- Map Polymarket "redeem" → Kalshi hold-to-settlement or early close
- Kalshi sports liquidity thinner — directional overlay may matter MORE than spread
- Use Polymarket research for **signal timing**; implement on Kalshi orderbook
- Validate markout at +30s/+60s/+120s before scaling clips

---

## Next research when sync completes

- dbdd4515 full bot_playbook → primary scaled reference
- UpTheBlues → tennis+soccer micro-market scanner
- RN1 + GamblingIsAllYouNeed → pure MM vs scatter taker baselines
