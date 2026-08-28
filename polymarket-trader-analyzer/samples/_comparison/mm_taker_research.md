# Polymarket Market Makers vs Takers — Research Synthesis

> Generated 2026-08-28. Combines leaderboard/web/institutional research with on-chain autopsies of 10 hand-selected wallets.

## TL;DR

| Goal | Best to study | Why |
|---|---|---|
| **Build a market-making bot** | HomeRunHazard → kch123 → sovereign2013 → RN1* | Pure two-sided sports inventory MM; buy-only + MERGE/REDEEM exits; 60–85% maker entry |
| **Copy-trade as taker (realistic)** | DrPufferfish → Winnertraders → polika72 | Maker-led or small-clip scalpers with reconciled PnL; still need speed |
| **Copy-trade as taker (hard / infra)** | swisstony, SineNooneEI, Anjun | Oracle/latency bots or esports selection alpha — edge is infrastructure, not rules |
| **Avoid copying blindly** | ImJustKen (incomplete sync), WTSA-style hold-to-redeem | Data gaps or path-dependent bankroll plays |

\*RN1 full autopsy still syncing (119k markets). Profile from leaderboard + PolyData + Twitter/community research.

---

## Part 1 — How top Polymarket MMs actually operate

### Institutional playbook (Jump, SIG, Wintermute on Kalshi/Polymarket)

1. **Split → quote → merge** — Mint YES+NO pairs at $1 combined, post both sides of the book, merge when inventory skews or spread captured.
2. **Maker rebates + LP rewards** — Edge is often fee/rebate capture on tight spreads, not directional prediction.
3. **Inventory skew** — Widen or pull the overweight side; lean quotes toward flat net exposure.
4. **Cancel before catalysts** — Pull quotes seconds before goals, injury news, or resolution triggers.
5. **Universe selection** — Focus on liquid sports totals/moneylines with recurring flow (NHL/NFL/NBA), not illiquid politics.

### Polymarket-specific mechanics we see on-chain

| Pattern | Who does it | Signal |
|---|---|---|
| Buy YES + buy NO, exit via MERGE/REDEEM | HomeRunHazard, kch123, sovereign2013 | `both_sides_rate` 57–69%, `buy_only=True` or near-zero sells |
| Maker entry, taker exit on resolution | kch123, sovereign2013 | 72–76% maker entry, 98%+ taker exit |
| FLB (favorite-longshot bias) harvesting | RN1*, HomeRunHazard | Quote longshots rich, favorites cheap in sports |
| Hybrid MM → directional overlay | kch123, ImJustKen/Domer | High maker % but massive one-sided NFL/NHL clips |
| **Not MM** — oracle/taker arb | swisstony | $1.8B vol, 16k buys / 0 sells in 30d sample, sub-second holds |

### Twitter / community signals

- **RN1** — Widely cited as the canonical Polymarket sports MM; ~91% maker in community analyses; both-sides quoting across thousands of NHL/NFL markets.
- **swisstony** — #1 leaderboard PnL (~$23.6M); described as oracle-anchored soccer/sports bot exploiting stale lines vs Betfair/Pinnacle.
- **kch123** — Top-5 PnL; hybrid MM with huge clip sizes on NFL/NHL; maker-led but redeems rather than sells.
- **DrPufferfish** — Known asymmetric scalper; posts resting bids, clips losers fast, lets winners run — taker/MM hybrid, not pure MM.
- **GamblingIsAllYouNeed** — "Scatter" dip-buying across many markets; taker-led, not a MM template.

---

## Part 2 — Hand-selected trader batch (10 wallets)

### Market makers / MM templates

| Rank | Trader | LB PnL | Identity | Both-sides | Entry maker% | Clip median | Copy diff | Verdict |
|---:|---|---:|---|---:|---:|---:|---:|---|
| 1 | **HomeRunHazard** | $2.25M | `two_sided_inventory_mm` | 68.6% | 84.9% | $8 | 8/3 | **Best pure MM template** — sports O/U, merge/redeem exit |
| 2 | **kch123** | $11.4M | `two_sided_inventory_mm` | 56.6% | 72.5% | $15 | 7/4 | Scale MM; NFL/NHL; closed PnL $13.4M; Sharpe 3.1 |
| 3 | **sovereign2013** | $3.6M | `two_sided_inventory_mm` | 61.7% | 75.5% | $20 | 7/4 | NBA/NHL bot; closed PnL $2.2M (LB drift — review) |
| 4 | **RN1*** | ~$13M | `two_sided_inventory_mm` (est.) | ~91% (est.) | ~91% (est.) | small | 9/2 | Gold standard at scale; needs full autopsy |
| 5 | **Winnertraders** | $17.6k | `hybrid_liquidity_scalper` | 9.2% | 62.2% | $7 | 6/5 | **Best small-bankroll MM starter** — copyable clip sizes |
| — | ImJustKen | $3.3M | incomplete | 82.7% | 74.4% | $6 | 7/4 | MM-shaped but sync ends Oct 2024; politics losses — do not copy until backfilled |

**HomeRunHazard playbook (copy this for MM bot):**
- Markets: sports totals (O/U), some matchups
- Entry: 85% maker limit bids on both Over and Under
- Exit: MERGE + REDEEM (not sell) — cashflow equity looks negative; trust closed-legs PnL
- Size: median $8, p90 $489 — accessible for small accounts
- Risk: high cashflow DD is normal for merge-redeem books

**kch123 playbook (scale version):**
- Same MM DNA but 100k+ trades, median clip $15, massive NFL/NHL one-sided accumulation then redeem
- 52.7% win rate on legs but positive expectancy via size asymmetry
- Sub-30s hold bucket: $5.8M of $13.4M closed PnL — fast inventory turnover

### Taker-alpha / copy-follow candidates

| Rank | Trader | LB PnL | Identity | Entry taker% | Clip median | Copy diff | Follow? |
|---:|---|---:|---|---:|---:|---:|---|
| 1 | **DrPufferfish** | $4.1M | `hybrid_liquidity_scalper` | 22% | $2 | 6/5 | **Best follow candidate** — maker entry, active sell exits, 90% WR legs |
| 2 | **Winnertraders** | $17.6k | `hybrid_liquidity_scalper` | 38% | $7 | 6/5 | Small scale; good for learning taker/MM hybrid |
| 3 | **polika72** | $57k | `one_sided_informed_scalper` | 62% | $11 | 8/3 | Live-game taker; 80% WR but latency-dependent |
| 4 | **SineNooneEI** | $639k | `directional_hold_to_resolution` | 59% | $29 | 9/2 | Esports selection; hold to redeem — not copyable live |
| 5 | **Anjun** | $862k | esports MM/taker mix | 15% | $5 | 7/4 | Esports specialist; 293k trades; needs domain expertise |
| 6 | **swisstony** | $23.6M | `oracle_anchored_sports_taker_bot` | ~100% | n/a | 10/1 | **Do not copy** — infra/oracle play |
| 7 | **GamblingIsAllYouNeed*** | ~$4.5M | scatter dip-buy | high taker | n/a | 8/3 | Autopsy in progress; taker scatter, not MM |

**DrPufferfish playbook (best taker to study):**
- Maker-first entry (78%) into mispriced NBA/NHL lines
- Active sell exits (not redeem-only) — cashflow PnL matches LB ($4.18M vs $4.06M)
- Asymmetric sizing: avg win $41k vs avg loss $26k
- 89–100% win rate in <5min hold buckets — scalper, not holder

**polika72 playbook (live taker):**
- 62% taker entry, 51% taker exit — pure speed play on sports totals
- 80% leg win rate but only $57k LB — edge is real but small capacity
- Copy difficulty 8/10: need live data feed + sub-second execution

**swisstony (do not copy):**
- $1.85B volume, #1 PnL; 30d sample: 16,112 buys, 0 sells
- Oracle-anchored: stale Polymarket line vs external book
- Requires co-located feeds, not retail copy-trading

---

## Part 3 — What you should build vs what you should follow

### If building a market-making system

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Split USDC  │────▶│ Quote YES+NO │────▶│ Skew/cancel │
│ (mint pair) │     │ maker limits │     │ on inventory│
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                     ┌──────────────┐     ┌─────▼──────┐
                     │ MERGE pairs  │◀────│ Flatten    │
                     │ + REDEEM     │     │ before news│
                     └──────────────┘     └────────────┘
```

**Priority implementation checklist:**
1. Start with **HomeRunHazard** universe: sports O/U, both sides, maker-only entries
2. Add **inventory skew** from kch123/RN1: pull overweight side when net > threshold
3. Implement **MERGE/REDEEM** exit path (not just sell) — critical for buy-only MM books
4. Target **maker rebate** capture; edge is spread + rebate, not prediction
5. Avoid politics/crypto until sports MM is profitable

**Realistic capital:** HomeRunHazard median clip $8 → $500–2k bankroll to prototype; kch123/RN1 need $50k+ for inventory.

### If copy-trading as taker

**Tier A — structurally copyable (with bot):**
- **DrPufferfish** — Resting bid + quick sell; 6/10 difficulty; monitor NBA/NHL pre-game lines
- **Winnertraders** — Same pattern at smaller scale; good paper-trade target

**Tier B — possible but latency-competitive:**
- **polika72** — Live in-game totals; need sport-specific trigger (score, pace, weather)
- **Anjun** — Esports; only if you have same domain expertise + faster feed

**Tier C — do not copy-trade:**
- **swisstony** — Oracle arb; you will always be late
- **SineNooneEI / WTSA** — Hold-to-redeem; edge is market selection months ahead
- **GamblingIsAllYouNeed** — Scatter dip-buy; needs wide capital + screening system

**Copy-trading reality check:**
- Polymarket fills are on-chain; follower latency 1–30s vs bot <100ms
- Maker-led traders (DrPufferfish 78% maker) are easier — you can mirror limit prices
- Pure takers (polika72 62% taker) — you eat worse prices on every follow trade

---

## Part 4 — Cross-comparison matrix

| Trader | Type | Preferred PnL | LB ALL | Trades | WR | Both-sides | Maker entry | Sharpe | Exit style |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| HomeRunHazard | MM | $2.23M | $2.25M | 26k | 54% | 69% | 85% | 4.9* | merge/redeem |
| kch123 | MM | $13.4M | $11.4M | 106k | 53% | 57% | 73% | 3.1 | redeem-heavy |
| sovereign2013 | MM | $2.2M | $3.6M | 119k | 51% | 62% | 76% | 0.4 | redeem-heavy |
| Winnertraders | hybrid | $17k | $18k | 20k | 65% | 9% | 62% | 4.7 | sell |
| DrPufferfish | taker/MM | $4.18M | $4.06M | 64k | 90% | 11% | 78% | 2.4 | sell |
| polika72 | taker | $58k | $57k | 20k | 80% | 1% | 38% | 14.7 | sell |
| Anjun | esports | $4.75M† | $862k | 293k | 60% | 40% | 85% | -0.02 | sell |
| SineNooneEI | hold | $541k | $639k | 17k | 80% | 1% | 41% | 0.9 | redeem |
| swisstony | oracle | n/a | $23.6M | 6.4M‡ | 58% | n/a | n/a | n/a | redeem |
| ImJustKen | MM? | DRIFT | $3.3M | 320k | 45%† | 83% | 74% | n/a | sell |

\*Closed-legs Sharpe where cashflow is misleading (merge/redeem books)  
†Reconciliation drift — use LB as ground truth  
‡PolyData trade count

---

## Part 5 — Recommended next steps

1. **Prototype MM bot** using HomeRunHazard rules on 5–10 liquid NHL O/U markets.
2. **Paper-follow DrPufferfish** — log fills vs theirs; measure slippage at 5s/30s delay.
3. **Backfill RN1 + ImJustKen + GamblingIsAllYouNeed** full autopsies (chunked 90-day sync).
4. **Do not** copy-trade swisstony or hold-to-redeem accounts without selection model.

---

## Artifacts

| Trader | Report |
|---|---|
| HomeRunHazard | `samples/HomeRunHazard/MASTER.md` |
| kch123 | `samples/kch123/MASTER.md` |
| sovereign2013 | `samples/sovereign2013/MASTER.md` |
| DrPufferfish | `samples/DrPufferfish/MASTER.md` |
| ImJustKen | `samples/ImJustKen/MASTER.md` |
| Winnertraders | `samples/Winnertraders/MASTER.md` |
| polika72 | `samples/polika72/MASTER.md` |
| Anjun | `samples/Anjun/MASTER.md` |
| SineNooneEI | `samples/SineNooneEI/MASTER.md` |
| swisstony | `samples/swisstony/profile.json` (lightweight) |

Full cross-trader table: `samples/_comparison/comparison.md`
