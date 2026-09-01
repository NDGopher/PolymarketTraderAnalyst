# Kalshi Directional MM Bot — Agent Brief

> For the Cursor agent building the Kalshi bot. User wants **directional flow capture**, not penny scalping.

## Core thesis

Run a **two-layer bot**:
1. **Base MM layer** — quote both sides, inventory skew, merge/flatten (HomeRunHazard DNA)
2. **Directional overlay** — **market suspension signal** (primary) + optional price steam (secondary)

Edge = being on the right side of **big repricing events**, not earning 1¢ spread.

**Primary signal (user thesis):** When **2+ bookmakers pull live odds off the board** during a match, buy Over on Kalshi before full reprice. Exit flat on false alarm; sell into spike on goal.

Full spec: **`market_suspension_strategy.md`** in this folder.

---

## Priority templates (copy logic, not wallets)

| Priority | Trader | Copy what | Skip what |
|---:|---|---|---|
| 1 | **Market suspension module** (user thesis) | Multi-book off-board → taker Over on Kalshi | Single-book suspend |
| 2 | **HomeRunHazard** | Split→quote both sides→MERGE, inventory skew, 85% maker | Buy-only without merge |
| 3 | **dbdd4515** (syncing) | Universe scanner, esports+sports, buy+redeem+sell hybrid | 101k market brute force |
| 4 | **DrPufferfish** | Maker bid → sell into strength, asymmetric sizing | Pure taker chase |
| 5 | **equity_16** | Multi-sport live activation, 3s cadence, sports_match focus | $1B vol capital reqs |
| 6 | **kch123 / RN1** | Informed MM on liquid totals, skew before catalysts | Whale clip sizes |
| 7 | **gmpm** | Sports match directional, then went inactive | Cashflow accounting |

**Do NOT template:** Allezpapa (WC whale), Mysaria (politics HFT), swisstony (oracle infra).

---

## Directional overlay spec (market suspension — PRIMARY)

```yaml
signal:
  type: market_suspension           # NOT price delta
  sources: [betfair, pinnacle, bet365]  # via odds API
  poll_interval_ms: 500-1000
  min_books_suspended: 2
  suspension_window_seconds: 5

action:
  on_suspension:
    cancel_all_mm_quotes_on_match
    if kalshi_over_ask not yet spiked:
      taker_buy_over(clip=50)
  on_reopen_no_goal:
    flatten(max_loss=4c)
  on_over_spike >= 10c:
    scale_out_50pct
  time_stop_seconds: 90

risk:
  max_directional_usdc_per_match: 500
  max_concurrent_live_matches: 5
  no_reentry_same_suspension_event: true
```

See `market_suspension_strategy.md` for event-type table and measurement plan.

---

## Secondary signal (price steam — optional)

If books stay live but move hard without suspending:
- 2+ books implied prob +3% in 10s → chase Over on lagging Kalshi
- Lower priority than suspension; use when books don't suspend on minor events

---

## MM base layer spec (Kalshi)

From HomeRunHazard + inventory guide:
- Quote YES+NO (or Over+Under) when spread ≥ 2¢
- Skew quotes when |net| > soft_cap
- MERGE when paired inventory > threshold
- **Pull all quotes when suspension fires** on that match
- Cancel before known catalysts (puck drop, kickoff)

Full skew/OBI guide: `inventory_skew_guide.md`

---

## Kalshi-specific notes

- Map Polymarket "redeem" → Kalshi hold-to-settlement or early close
- Kalshi sports liquidity thinner — directional overlay may matter MORE than spread
- Use Polymarket research for **signal timing validation**; implement on Kalshi orderbook
- **Measure suspension-to-Kalshi-move gap** before scaling — edge dies if gap < 2s

---

## File map (this repo)

```
polymarket-trader-analyzer/samples/_research/
├── kalshi_directional_mm_brief.md      ← THIS FILE (agent brief)
├── market_suspension_strategy.md       ← PRIMARY strategy spec
├── inventory_skew_guide.md             ← MM base layer
├── new_trader_synthesis.md             ← wallet autopsy summaries
└── ../polika72/bot_playbook.md         ← live scalper reference
```

GitHub branch: `cursor/polymarket-trader-deep-dives-35c6`
