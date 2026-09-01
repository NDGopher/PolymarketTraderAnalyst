# Inventory Skew & Orderbook Imbalance — Builder's Guide

> For building your own MM / live-scalp bot on Polymarket (not copy-trading).

## 1. Two different concepts (don't conflate them)

| Concept | What it measures | Who owns it |
|---|---|---|
| **Inventory skew** | Your net position (long Over, short Yes, etc.) | You |
| **Orderbook imbalance (OBI)** | Bid vs ask depth on the CLOB | The market |

Both matter, but they answer different questions:
- **OBI** → "Which way is flow / liquidity leaning in the next few seconds?"
- **Inventory skew** → "Am I exposed if mid moves against me?"

---

## 2. Inventory skew (your position)

### Definition

For a binary market with outcomes A and B (Over/Under or Yes/No):

```
net_A = shares_A - shares_B   # in share units
net_usdc ≈ net_A × mid_A      # approximate dollar exposure
```

**Skew ratio:** `net_A / max_inventory_cap` → ranges from -1 (max short A) to +1 (max long A).

### How top Polymarket MMs use it

**HomeRunHazard / kch123 / RN1 pattern (two-sided MM):**

1. Buy both Over AND Under when combined cost < $1 (after fees).
2. When `net_Over > threshold`:
   - Stop bidding Over (or lower Over bid by 2–5¢)
   - Keep bidding Under (or increase Under bid)
   - MERGE pairs when `min(shares_Over, shares_Under) > 0`
3. When `|net| > hard_cap`: pull ALL quotes, merge immediately.

**Quote skew formula (standard MM):**

```python
reservation_price = fair_mid - (inventory_skew × skew_factor)

# Example: fair Over mid = 0.50, you're long 500 Over shares, skew_factor = 0.0001
# reservation = 0.50 - (500 × 0.0001) = 0.45  → bid lower, ask lower (want to sell)
```

**Interpretation:** When long, shift your reservation price DOWN → you bid less aggressively and ask more aggressively → natural mean-reversion toward flat.

### When skew helps you "be on the right side"

| Situation | Right-side action |
|---|---|
| Long Over, goal just scored | Pull Over bids immediately; don't "hope" — you got picked off |
| Long Over, no event, OBI shows ask-heavy book | Hold or add if your model says fair > mid (dip buy) |
| Long both sides (paired) | Skew ≈ 0; profit = spread + merge, not direction |
| Short inventory (sold without hedge) | Rare on Polymarket retail; flatten fast |

**Key insight from autopsies:** Losers scale-in more than winners (polika72: 39% vs 28% scale-in rate). **Forbid averaging down without a fresh signal.**

---

## 3. Orderbook imbalance (OBI)

### Definition

```
OBI = (bid_depth - ask_depth) / (bid_depth + ask_depth)
```

Computed over top N price levels (usually 3–5) on the outcome you're trading.

| OBI | Reading |
|---|---|
| +0.3 to +1.0 | Bid-heavy — support below, but also "wall" may get lifted |
| -0.3 to -1.0 | Ask-heavy — resistance above, often a **dip-buy zone** for scalpers |
| Near 0 | Balanced book — MM-friendly for two-sided quoting |

### How to use OBI for strategy (not copy-trading)

**For MM bots (HomeRunHazard-style):**
- Quote both sides when OBI ≈ 0 and spread is wide enough.
- When OBI > +0.5 (heavy bids): widen your bid (don't join the queue at the back).
- When OBI < -0.5 (heavy asks): widen your ask OR reduce size — someone may be dumping.
- **Cancel all quotes** when OBI flips sign rapidly (goal, injury, large taker sweep).

**For live scalpers (polika72-style):**
- Entry trigger: OBI < -0.4 AND mid drops 3–5¢ in <30s → post maker bid (dip buy).
- Impulse trigger: OBI flips positive fast after attack/corner → take or bid Over.
- Exit trigger: OBI > +0.3 AND mid ≥ entry + 15–20¢ → scale out asks.

**Combining OBI + inventory:**

```python
if net_over > soft_cap and obi > 0:
    # Long AND bid-heavy = you're adding to crowded side → DON'T bid
    pull_bids()
elif net_over < soft_cap and obi < -0.4 and fair_over > mid:
    # Flat/short, ask-heavy dip, model says cheap → BUY
    place_maker_bid()
```

---

## 4. Being on the "right side" of MM plays

You're not trying to predict the match. You're trying to:

1. **Earn spread** when both sides trade through you.
2. **Avoid adverse selection** — getting filled right before bad news.
3. **Stay flat** into resolution unless you have intentional edge.

### Practical rules from on-chain autopsies

| Rule | Source |
|---|---|
| MERGE when paired inventory > 0 | HomeRunHazard, kch123 |
| 85% maker entry, exit via redeem not panic sell | HomeRunHazard |
| Median hold <2min for scalps; flatten before whistle | polika72 |
| Pull quotes 30–60s before known catalysts | Institutional MM playbook |
| Target spread capture ~15–20¢ on O/U Over | polika72 median winner spread 0.20 |
| Never scale-in losers without new signal | polika72 loser DNA |

### Fair value anchor (critical for both MM and scalper)

Polymarket mid alone is **laggy** on live sports. Top takers anchor to:
- Betfair / Pinnacle implied prob
- Live model (xG, score, time remaining)

**Your bot's "fair" should update on events BEFORE Polymarket mid moves.** That's the edge — not raw speed alone.

---

## 5. Architecture sketch

```
External fair (Betfair + live model)
        │
        ▼
┌───────────────────┐     ┌─────────────────────┐
│ OBI + mid monitor │────▶│ Signal: quote / dip / │
│ (Polymarket WS)   │     │ impulse / flatten     │
└───────────────────┘     └──────────┬──────────┘
                                     │
┌───────────────────┐     ┌──────────▼──────────┐
│ Inventory tracker │◀───▶│ Quote engine (skew)   │
│ net_shares/market │     │ post-only + merge     │
└───────────────────┘     └─────────────────────┘
```

---

## 6. Parameter starters

```yaml
# MM mode (HomeRunHazard-like)
max_net_shares_per_market: 500
soft_skew_cap: 200          # start skewing quotes
hard_skew_cap: 500          # pull all quotes + merge
skew_factor: 0.0001         # reservation shift per share
min_spread_to_quote: 0.02   # 2¢
merge_threshold_shares: 50

# Scalp mode (polika72-like)
obi_dip_entry: -0.4
dip_mid_drop_cents: 3
target_spread: 0.20
time_stop_seconds: 112      # p75 hold
stop_loss_cents: 4
clip_usdc: 11
preferred_outcome: Over
```
