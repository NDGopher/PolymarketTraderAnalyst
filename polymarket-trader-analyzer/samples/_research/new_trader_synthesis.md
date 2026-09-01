# New Trader Deep Dives — Sep 2026

Hand-selected wallets from user links. Full autopsies running for large accounts; lightweight + PolyData profiles below.

## Quick reference

| Trader | LB PnL | Rank | Style | Replicable? |
|---|---:|---:|---|---|
| **Allezpapa** | $4.28M | 29 | World Cup hold-to-redeem whale | Event-only, not daily |
| **Mysaria** | $635k | 323 | Hybrid MM politics/weather/tweets | Partial — needs full sync |
| **gmpm** | $3.53M | 42 | Elite then **inactive** (0 trades 90d) | Unknown — gone |
| **equity_16** | $7.37M | 16 | Multi-sport live bot (MLB/soccer/esports) | Hard — $1B vol infra |
| **UpTheBlues** | $1.14M | 160 | Tennis + soccer live micro-markets | Medium — niche sports |
| **dbdd4515** | $1.21M | 149 | Esports + live sports buy/redeem bot | **Best MM/scalp hybrid target** |
| **polika72** | $57k | 3243 | Soccer O/U one-sided live scalper | Yes — see bot_playbook |

---

## Allezpapa (World Cup crusher) — FULL AUTOPSY ✅

**Wallet:** `0xe549581668a5751c1972d3ad2d1991d900bd2d54`  
**Active:** Jun 9 – Jul 19, 2026 only (~40 days), then gone  
**Report:** `samples/Allezpapa/`

### What happened
- **57,355 buys, 0 sells** — pure buy-and-redeem
- **98.8% win rate** on 83 closed legs (82W / 1L)
- **$4.23M cashflow PnL** matches leaderboard ($4.28M)
- Single biggest win: **Spain World Cup winner $2.25M** (bought $420k, redeemed)
- Other winners: Norway-England draw $739k, Spain-Argentina draw $444k, Ecuador ML $410k
- Only loser: Uruguay vs Cabo Verde O/U 2.5 -$84k

### How they did it
This is **not** market making or live scalping. It's **mega-event directional selection** with whale sizing during the 2026 World Cup:
- Concentrated in 156 markets, almost all FIFA WC
- Median ticket $8.51 but **max clip $260,000**
- Hold to resolution (median hold 11h+, many multi-day)
- Massive draw/ML positions that resolved correctly

### Is it replicable on a normal soccer day?
**No.** This edge requires:
1. A once-in-four-years liquidity event with mispriced tails
2. Seven-figure bankroll tolerance (max DD -$2.07M on equity curve)
3. Correct macro calls (Spain to win WC, key draw outcomes)
4. Willingness to go inactive after the event

Normal EPL Tuesday games don't offer $2M+ mispricings on outright winner markets. **Do not build a daily bot from this template.**

---

## Mysaria — FULL AUTOPSY ✅ (sync caveat)

**Wallet:** `0xe40aaa5ce1dac0b7dc24c9d0284f27e17c3fe4a2`  
**Report:** `samples/Mysaria/`

### Profile
- LB $635k rank 323; **266k trades in 27 days** (Aug 5 – Sep 1 2026 in our sync)
- 37% both-sides markets — hybrid MM on politics, weather, tweet-count markets
- Top winners: Fed no-change $15k, Lula Brazil election $9k, Elon tweet bands $4k
- Median gap **12 seconds** — HFT-style on non-sports

### Caveat
Our tape shows **negative closed PnL** vs positive LB — likely incomplete lifetime sync or heavy open-position / conversion accounting. Treat LB as ground truth; re-sync needed for full picture.

### Strategy to copy
- Two-sided inventory on political/entertainment markets with wide spreads
- NOT a sports/live model — different infrastructure (resolution calendars, not match feeds)

---

## gmpm (elite then gone) — AUTOPSY IN PROGRESS

**Wallet:** `0x14964aefa2cd7caff7878b3820a690a03c5aa429`

### PolyData / API
- LB **$3.53M** rank 42; 826 markets; **$0 activity last 90 days**
- 42,442 buys / 3,536 sells / 25 redeems — historically buy-heavy with some sells
- Win rate ~54%

### Interpretation
Classic **hit-and-retire** profile: concentrated run on ~845 markets, then wallet went dark. Possibly:
- One major event cycle (like Allezpapa but earlier/different event)
- Operator rotated to new wallet
- Extracted profits and stopped

**Not copyable live** — study closed positions when autopsy completes for event type.

---

## equity_16 (rank #16, bad week) — AUTOPSY IN PROGRESS

**Wallet:** `0x2c335066fe58fe9237c3d3dc7b275c2a034a0563`  
**LB:** $7.37M · **$1B volume** · rank 16

### Recent 90d tape (sample)
- 4,659 buys / 0 sells / 287 redeems / 39 merges
- **MLB** (Dodgers-Braves 527 fills), **EPL** (Chelsea, Man City, Man U), **CS esports**
- Month PnL: **-$44k** — bad week but lifetime curve still elite

### Strategy hypothesis
Multi-sport **live buy-and-redeem bot** at scale — same structural pattern as dbdd4515 but 10× volume. Likely:
- Maker/taker buys on live match markets
- Redeem on resolution (minimal sells in recent window)
- Cross-sport diversification (baseball + soccer + esports)

### For your MM bot
Study for **scale and universe selection**, not entry timing (needs full autopsy).

---

## UpTheBlues (soccer expert?) — AUTOPSY QUEUED

**Wallet:** `0x2a69660046d7acc4ab204d7cc5ba78b0776cd2f7`  
**LB:** $1.14M · 79k markets traded

### Recent 90d tape
- 4,251 buys / 0 sells / 748 redeems
- **Not pure soccer:** heavy **tennis** (ITF Plovdiv, US Open), plus Arsenal, Dortmund, Villa O/U
- PolyData: 4,876 buys / 7,177 sells / 3,918 redeems lifetime — historical two-way activity

### Verdict
"Soccer expert" is **misleading** — this is a **live micro-sports bot** spanning tennis + soccer + misc. Profitable across many small markets (79k touched). Month: -$16k drawdown.

**Copy path:** Build a multi-league live scanner (tennis + soccer), buy-only + redeem exit, small clips across many simultaneous matches.

---

## dbdd4515 (YOUR TARGET) — DEEP DIVE RUNNING ⏳

**Wallet:** `0xdbdd45150249e229eb4ca8aa48a30dca21faa5de`  
**LB:** $1.21M rank 149 · 101k markets

### PolyData lifetime
- 20,195 buys / 8,825 sells / 9,297 redeems
- Win rate 52.4% · 15k markets in PolyData
- **Both sell AND redeem exits** — most MM-like wallet in this batch

### Recent 90d (5000 activity sample)
- 4,058 buys / 0 sells / 939 redeems
- **Esports CS:** 37% of trades (ESL Challenger BO3 matches)
- Sports match 27%, O/U 15%, other 20%
- Top markets: CS Rooster vs MARKandLARRY (60 fills), NM United ML (38)

### Why this matches what you're building
1. **High market count** (101k) — automated universe scanning
2. **Buy + redeem** recent pattern = inventory / hold-to-redeem MM on live markets
3. **Historical sells** = also runs spread-capture exits (like polika72/DrPufferfish hybrid)
4. **Cross-category** (esports + soccer + tennis) — one engine, many leagues

### vs polika72
| | polika72 | dbdd4515 |
|---|---|---|
| PnL | $57k | $1.21M |
| Markets | 5.4k | 101k |
| Sells | 10,901 (active) | 8,825 historical, 0 recent 90d |
| Focus | Soccer O/U Over scalps | Esports + multi-sport |
| Hold | 30s–2m | More redeem-heavy recently |

**dbdd4515 is the scaled-up operator version** — same live-sports infrastructure, broader universe, more redeem-style exits.

Full report landing in `samples/` when sync completes (~101k markets).

---

## polika72 — how the live engine works

See `samples/polika72/bot_playbook.md` for full spec.

### NOT classic MM
- 0.7% both-sides rate — **one-sided Over scalper** on soccer O/U
- BUY clip → SELL same outcome higher within **30s–2m** (86.7% WR, $42.8k in that bucket)

### Speed requirements (from latency_impulse data)
| Metric | Value |
|---|---|
| Median time to max favorable excursion | **64 seconds** |
| Big moves (≥10¢) within 60s | **54%** |
| Big moves within 30s | **8%** |
| Median winner spread (exit − entry) | **20¢** |
| Median hold | **66 seconds** |

**Interpretation:** polika72 does NOT need sub-100ms HFT. They need:
1. **Live match state faster than Polymarket mid updates** (Opta/Betfair anchor)
2. **Sub-5-second execution** to catch 60-second impulse windows
3. **Maker-first entries** (62% taker still — takes when impulse already moving)

### Build stack
```
Sportradar/Opta live events ──► fair value model
Betfair/Pinnacle odds ────────► anchor mid
Polymarket CLOB WebSocket ────► OBI + dip detection
Post-only bids + taker exit ──► clip ~$11, target +20¢
```

### What makes them "smoke" live deals
- Trade **Over** on O/U when attack momentum / goal threat reprices line
- Buy dips when ask-heavy OBI (microstructure, not prediction)
- Scale out into strength (many small sells, not one exit)
- **Cut losers fast** — losers have negative spread (-4¢ median vs +20¢ winners)

---

## Pending from prior session
- **RN1** — canonical sports MM (~$13M, 119k markets) — not yet synced on this branch
- **GamblingIsAllYouNeed** — scatter dip-buy taker — queued

Run: `polyanalyst analyze RN1 --full` and `polyanalyst analyze GamblingIsAllYouNeed --full`
