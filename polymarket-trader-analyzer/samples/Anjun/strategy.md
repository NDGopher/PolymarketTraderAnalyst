# Strategy Dossier: Anjun

- **Wallet:** `0x43372356634781eea88d61bbdd7824cdce958882`
- **History span:** 2022-12-12T21:33:03+00:00 → 2026-08-25T21:15:19+00:00 (1351.99 days)
- **Trades:** 293,079 (buys 240,328 / sells 52,751)
- **Markets touched:** 13,442
- **Closed positions:** 17,499

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$16,535,033.07 |
| Core cashflow (ex-rebates) | -$16,744,017.33 |
| Closed-positions realized sum | $4,747,733.59 |
| Win rate (closed) | 59.65% (9331W / 6312L) |
| Profit factor | 1.7058 |
| Gross wins / losses | $11,474,831.54 / -$6,727,097.94 |
| Equity max drawdown | -$2,074,745.64 |
| Polymarket leaderboard (ALL) | $861,718.32 PnL · vol $180,326,675.11 · rank 229 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=4747733.5925 ref=861718.3206124196 diff=3886015.2719
- **DRIFT** `polydata` realized_pnl: ours=4747733.5925 ref=736777.34 diff=4010956.2525
- **DRIFT** `polydata` n_trades: ours=293079 ref=353745 diff=-60666
- **MATCH** `polydata` win_rate: ours=0.5965 ref=0.5994 diff=-0.0029
- **DRIFT** `internal` cashflow_vs_closed: ours=-16535033.0665 ref=4747733.5925 diff=-21282766.659

## What kind of trader is this?

**Classification:** `hybrid_mm_directional` (score 35/100)

- Trades both outcomes in 40% of markets (inventory/MM signature)
- High-frequency cadence (median gap 42s)

Supporting rates — both-sides markets: 0.4023, fast round-trips: 0.1669, spread-capture rate: 0.4265.

## Exact edge thesis

Anjun looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $4,118,459.37 across 5003 closed legs
- **sports_totals**: $608,556.17 across 1400 closed legs
- **other**: $106,382.15 across 8034 closed legs
- **crypto**: $61,741.66 across 1277 closed legs
- **politics**: -$147,405.76 across 1785 closed legs

## Timing

- Peak UTC hours: 19, 16, 17, 15, 18
- Peak weekdays (0=Mon): [3, 5, 2]
- Median inter-trade gap: 42s

## Sizing

- Median ticket $4.69, mean $324.24, p90 $304.22, max $332,666.33
- Share size median 36.0, mean 553.486

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### Will Spain win the 2026 FIFA World Cup?
- Entries ≈ **0.675** · Exits ≈ **0.835** · Spread ≈ **0.160**
- Fills: 534 buys / 29 sells · hold 98d 13h · both-sides=True · realized $80,652.18

### No change in Fed interest rates after June 2025 meeting?
- Entries ≈ **0.630** · Exits ≈ **0.914** · Spread ≈ **0.283**
- Fills: 27 buys / 3 sells · hold 18d 17h · both-sides=True · realized $49,111.57

### LoL: Nongshim Red Force vs Hanwha Life Esports (BO3)
- Entries ≈ **0.116** · Exits ≈ **0.509** · Spread ≈ **0.393**
- Fills: 29 buys / 7 sells · hold 4h 50m · both-sides=True · realized $31,876.04

### LoL: Team WE vs EDward Gaming (BO3)
- Entries ≈ **0.472** · Exits ≈ **0.736** · Spread ≈ **0.263**
- Fills: 50 buys / 33 sells · hold 21h 44m · both-sides=False · realized $23,508.37

### Will Liverpool FC win on 2026-01-01?
- Entries ≈ **0.335** · Exits ≈ **0.340** · Spread ≈ **0.005**
- Fills: 2 buys / 4 sells · hold 27m 50s · both-sides=False · realized $20,919.07

### Will T1 win LoL Worlds 2025?
- Entries ≈ **0.535** · Exits ≈ **0.553** · Spread ≈ **0.019**
- Fills: 1355 buys / 146 sells · hold 18d 7h · both-sides=True · realized $20,709.51

### LoL: EDward Gaming vs Oh My God (BO5) - LPL Knights Rivals
- Entries ≈ **0.346** · Exits ≈ **0.573** · Spread ≈ **0.227**
- Fills: 112 buys / 2 sells · hold 7h 28m · both-sides=True · realized $19,581.62

### LoL: Weibo Gaming vs Anyone's Legend (BO5) - LPL Playoffs
- Entries ≈ **0.190** · Exits ≈ **0.200** · Spread ≈ **0.011**
- Fills: 67 buys / 40 sells · hold 7h 57m · both-sides=False · realized $15,599.06

### LoL: Dplus KIA vs Nongshim Red Force (BO3) - LCK Rounds 1-2
- Entries ≈ **0.211** · Exits ≈ **0.240** · Spread ≈ **0.029**
- Fills: 2 buys / 67 sells · hold 20h 49m · both-sides=False · realized $14,984.88

### LoL: Movistar KOI vs G2 Esports (BO3) - LEC Regular Season
- Entries ≈ **0.250** · Exits ≈ **0.272** · Spread ≈ **0.022**
- Fills: 62 buys / 7 sells · hold 5h 1m · both-sides=True · realized $13,881.24

## Top closed winners / losers

**Winners**
- No change in Fed interest rates after July 2025 meeting?: $131,664.69 · bought $2,199.78 · sold $0.00 · hold 10h 18m
- Will China invade Taiwan by end of 2026?: $105,113.49 · bought $489,512.26 · sold $3,224.19 · hold 394d 19h
- Will "Avatar: Fire and Ash" Opening Weekend Box Office be less than 90m?: $103,563.83 · bought $38,939.01 · sold $3,488.19 · hold 2d 9h
- Will 'Lilo & Stitch' gross between $140-150m opening weekend?: $89,971.60 · bought $8,698.58 · sold $0.00 · hold 2d 16h
- Will A Minecraft Movie be the top grossing movie of 2025?: $89,804.85 · bought $60,857.79 · sold $3,284.38 · hold 313d 18h
- Will Spain win the 2026 FIFA World Cup?: $80,652.18 · bought $239,840.81 · sold $74,198.90 · hold 98d 13h
- Fed decreases interest rates by 25 bps after September 2025 meeting?: $79,370.24 · bought $65,613.44 · sold $0.00 · hold 8h 29m
- Khamenei out as Supreme Leader of Iran by March 31?: $63,091.56 · bought $249,002.53 · sold $981.48 · hold 20d 16h
- Will Nigeria vs. Morocco end in a draw?: $55,574.03 · bought $14,832.66 · sold $0.00 · hold 2h 45m
- No change in Fed interest rates after June 2025 meeting?: $49,111.57 · bought $48,382.50 · sold $70,054.55 · hold 18d 17h

**Losers**
- Will Arsenal FC win on 2026-05-30?: -$138,693.38 · bought $58,431.38 · sold $277.94
- Will Jake Paul win his boxing match against Anthony Joshua?: -$101,960.43 · bought $0.00 · sold $204.33
- Will "Avatar: Fire and Ash" Opening Weekend Box Office be between 101m and 112m?: -$99,899.08 · bought $12,969.76 · sold $3,295.01
- Will Zootopia 2 be the top grossing movie of 2025?: -$89,994.77 · bought $3,467.23 · sold $193.19
- Will 'Lilo & Stitch' gross between $150-160m opening weekend?: -$79,233.38 · bought $5,084.02 · sold $2,031.33
- Will 'Lilo & Stitch' gross less than $140m opening weekend?: -$75,431.42 · bought $38,764.25 · sold $338.19
- US strikes Iran by February 28, 2026?: -$48,324.87 · bought $85,173.84 · sold $5,427.27
- No change in Fed interest rates after September 2025 meeting?: -$45,405.66 · bought $66,498.34 · sold $858.18
- Fed decreases interest rates by 25 bps after May 2025 meeting?: -$41,271.80 · bought $0.00 · sold $141.34
- Exact Score: Norway 2 - 1 England?: -$40,920.17 · bought $61,006.30 · sold $0.00

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $85,976,733.36
- Sells: $9,062,410.82
- Redeems: $60,170,305.21
- Maker rebates: $34,651.76
- Taker rebates: $816.95

_Generated 2026-08-25T21:56:17.950815+00:00_
