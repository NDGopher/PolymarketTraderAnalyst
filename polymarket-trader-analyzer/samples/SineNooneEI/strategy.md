# Strategy Dossier: SineNooneEI

- **Wallet:** `0x38337de21ff0bb0a11a40761507d51e318d633d1`
- **History span:** 2026-02-03T12:59:50+00:00 → 2026-08-24T17:11:52+00:00 (202.18 days)
- **Trades:** 16,603 (buys 16,599 / sells 4)
- **Markets touched:** 1,580
- **Closed positions:** 1,070

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | $541,301.28 |
| Core cashflow (ex-rebates) | $523,137.79 |
| Closed-positions realized sum | $3,761,463.08 |
| Win rate (closed) | 79.53% (851W / 219L) |
| Profit factor | 1.9658 |
| Gross wins / losses | $7,656,000.80 / -$3,894,537.72 |
| Equity max drawdown | -$470,522.99 |
| Polymarket leaderboard (ALL) | $639,212.87 PnL · vol $29,168,764.39 · rank 318 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=541301.2799 ref=639212.8736756515 diff=-97911.5938
- **MATCH** `polydata` realized_pnl: ours=523137.7892 ref=506308.1 diff=16829.6892
- **DRIFT** `polydata` n_trades: ours=16603 ref=14776 diff=1827
- **DRIFT** `polydata` win_rate: ours=0.7953 ref=0.5312 diff=0.2641
- **DRIFT** `internal` cashflow_vs_closed: ours=541301.2799 ref=3761463.0818 diff=-3220161.8019

## What kind of trader is this?

**Classification:** `hybrid_mm_directional` (score 30/100)

- Fast round-trips (<2h) in 100% of two-sided markets
- High-frequency cadence (median gap 12s)

Supporting rates — both-sides markets: 0.0101, fast round-trips: 1.0, spread-capture rate: 0.0.

## Exact edge thesis

SineNooneEI looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **sports_match**: $3,639,964.63 across 1053 closed legs
- **sports_totals**: $94,457.53 across 16 closed legs
- **other**: $27,040.92 across 1 closed legs

## Timing

- Peak UTC hours: 9, 8, 11, 10, 16
- Peak weekdays (0=Mon): [6, 5, 4]
- Median inter-trade gap: 12s

## Sizing

- Median ticket $29.11, mean $899.07, p90 $2,314.63, max $86,562.02
- Share size median 56.0, mean 1759.377

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

## Top closed winners / losers

**Winners**
- LoL: Fnatic vs SK Gaming - Game 2 Winner: $239,727.93 · bought $6,306.20 · sold $0.00 · hold 2s
- Dota 2: Aurora vs MOUZ (BO3) - DreamLeague Stage 2: $129,076.88 · bought $37,501.90 · sold $0.00 · hold 10h 20m
- LoL: T1 vs Dplus KIA (BO5) - LCK Cup Playoffs: $103,788.42 · bought $56,917.58 · sold $0.00 · hold 4h 7m
- LoL: Dplus KIA vs DRX - Game 3 Winner: $66,004.70 · bought $33,995.31 · sold $0.00 · hold 0s
- Toronto Blue Jays vs. Baltimore Orioles: O/U 7.5: $48,354.78 · bought $50,390.86 · sold $0.00 · hold 1h 2m
- Roland Garros ATP: Jakub Mensik vs Andrey Rublev: $47,048.83 · bought $39,905.08 · sold $0.00 · hold 3h 9m
- Roland Garros WTA: Marta Kostyuk vs Mirra Andreeva: $46,860.92 · bought $36,850.23 · sold $0.00 · hold 0s
- LoL: Cloud9 vs FlyQuest (BO3) - LCS Lock In Group Stage: $45,702.27 · bought $89,898.87 · sold $0.00 · hold 2h 13m
- LoL: DRX vs OKSavingsBank BRION - Game 2 Winner: $44,785.59 · bought $31,202.28 · sold $0.00 · hold 48s
- San Diego Padres vs. Washington Nationals: O/U 7.5: $44,401.63 · bought $46,298.03 · sold $0.00 · hold 2h 31m

**Losers**
- Spread: Pistons (-8.5): -$126,706.51 · bought $77,472.30 · sold $0.00
- Counter-Strike: paiN vs Passion UA (BO3) - ESL Pro League Stage 1: -$84,487.84 · bought $84,487.84 · sold $0.00
- Will Chelsea FC win on 2026-03-14?: -$81,935.18 · bought $81,938.94 · sold $0.00
- LoL: Cloud9 vs LYON - Game 2 Winner: -$69,220.58 · bought $69,220.67 · sold $0.00
- LoL: DRX vs Nongshim Red Force - Game 1 Winner: -$62,131.89 · bought $62,132.06 · sold $0.00
- Counter-Strike: FURIA vs Vitality (BO5) - IEM Krakow Playoffs: -$59,675.53 · bought $59,683.51 · sold $0.00
- LoL: Cloud9 vs LYON (BO5) - LCS Lock In Playoffs: -$52,198.45 · bought $52,198.51 · sold $0.00
- Counter-Strike: Vitality vs MOUZ (BO3) - IEM Krakow Playoffs: -$49,989.72 · bought $50,002.32 · sold $0.00
- LoL: Dplus KIA vs DN Freecs - Game 3 Winner: -$47,509.46 · bought $47,510.56 · sold $0.00
- LoL: JD Gaming vs Top Esports - Game 2 Winner: -$45,213.06 · bought $45,216.49 · sold $0.00

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $14,979,368.39
- Sells: $43,765.65
- Redeems: $15,458,740.52
- Maker rebates: $5,659.43
- Taker rebates: $12,275.99

_Generated 2026-08-25T21:55:39.321046+00:00_
