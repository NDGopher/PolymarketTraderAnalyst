# Strategy Dossier: ImJustKen

- **Wallet:** `0x9d84ce0306f8551e02efef1680475fc0f1dc1344`
- **History span:** 2022-12-12T20:58:21+00:00 → 2024-10-23T20:47:17+00:00 (680.99 days)
- **Trades:** 320,389 (buys 279,362 / sells 41,027)
- **Markets touched:** 5,257
- **Closed positions:** 17,542

## Headline performance

| Metric | Value |
|---|---|
| Realized cashflow (sells − buys + redeems + rebates) | -$43,822,026.87 |
| Core cashflow (ex-rebates) | -$44,806,140.80 |
| Closed-positions realized sum | -$27,767,466.73 |
| Win rate (closed) | 45.30% (7601W / 9179L) |
| Profit factor | 0.4002 |
| Gross wins / losses | $18,524,140.21 / -$46,291,606.94 |
| Equity max drawdown | -$3,669,479.03 |
| Polymarket leaderboard (ALL) | $3,291,874.41 PnL · vol $499,524,708.36 · rank 44 |

## Source validation

- **DRIFT** `polymarket_leaderboard_ALL` pnl: ours=-27767466.7259 ref=3291874.409581338 diff=-31059341.1355
- **DRIFT** `polydata` realized_pnl: ours=-27767466.7259 ref=3289074.81 diff=-31056541.5359
- **DRIFT** `polydata` n_trades: ours=320389 ref=606672 diff=-286283
- **DRIFT** `polydata` win_rate: ours=0.453 ref=0.6133 diff=-0.1603
- **DRIFT** `internal` cashflow_vs_closed: ours=-43822026.8674 ref=-27767466.7259 diff=-16054560.1415

## What kind of trader is this?

**Classification:** `hybrid_mm_directional` (score 35/100)

- Trades both outcomes in 83% of markets (inventory/MM signature)
- High-frequency cadence (median gap 40s)

Supporting rates — both-sides markets: 0.8273, fast round-trips: 0.0071, spread-capture rate: 0.2866.

## Exact edge thesis

ImJustKen looks more **directional**: edges concentrate in being right about outcomes rather than harvesting bid-ask. Study their win rate by category and entry timing relative to kickoff / resolution.

See `bot_playbook.md` for the full entry/management/exit autopsy and bot architecture.

## Where the money comes from

- **crypto**: -$36,485.84 across 640 closed legs
- **sports_totals**: -$103,374.22 across 575 closed legs
- **other**: -$2,020,177.57 across 9844 closed legs
- **politics**: -$7,063,659.57 across 3531 closed legs
- **sports_match**: -$18,543,769.53 across 2952 closed legs

## Timing

- Peak UTC hours: 7, 15, 14, 3, 8
- Peak weekdays (0=Mon): [2, 1, 3]
- Median inter-trade gap: 40s

## Sizing

- Median ticket $6.27, mean $278.37, p90 $364.18, max $257,495.53
- Share size median 100.0, mean 1017.5798

## Trade-by-trade pattern (representative winners)

These vignettes are reconstructed from fills: average entry, average exit, hold time, and closed realized PnL.

### No change in Fed interest rates after 2024 September meeting?
- Entries ≈ **0.676** · Exits ≈ **0.987** · Spread ≈ **0.311**
- Fills: 277 buys / 2 sells · hold 53d 2h · both-sides=True · realized $123,657.72

### Biden drops out of presidential race?
- Entries ≈ **0.496** · Exits ≈ **0.502** · Spread ≈ **0.007**
- Fills: 1104 buys / 437 sells · hold 301d 19h · both-sides=True · realized $89,816.48

### Fed decreases interest rates by 25 bps after November 2024 meeting?
- Entries ≈ **0.485** · Exits ≈ **0.860** · Spread ≈ **0.374**
- Fills: 127 buys / 2 sells · hold 79d 2h · both-sides=True · realized $65,890.56

### Will Erdoğan win the 2023 Turkish presidential election?
- Entries ≈ **0.623** · Exits ≈ **0.947** · Spread ≈ **0.324**
- Fills: 208 buys / 13 sells · hold 87d 1h · both-sides=True · realized $62,824.90

### Will there be between 16 and 20 named storms during Atlantic Hurricane Season?
- Entries ≈ **0.416** · Exits ≈ **0.424** · Spread ≈ **0.009**
- Fills: 171 buys / 9 sells · hold 163d 15h · both-sides=True · realized $50,754.96

### Will weed be rescheduled in 2024?
- Entries ≈ **0.555** · Exits ≈ **0.889** · Spread ≈ **0.334**
- Fills: 411 buys / 9 sells · hold 279d 12h · both-sides=True · realized $48,042.05

### Trump sentenced to no prison time?
- Entries ≈ **0.540** · Exits ≈ **0.961** · Spread ≈ **0.421**
- Fills: 390 buys / 5 sells · hold 144d 2h · both-sides=True · realized $45,639.95

### Will Israel invade Lebanon in September?
- Entries ≈ **0.447** · Exits ≈ **0.457** · Spread ≈ **0.010**
- Fills: 433 buys / 7 sells · hold 19d 3h · both-sides=True · realized $44,296.45

### Will Nicolas Maduro Win the 2024 Venezuela presidential election?
- Entries ≈ **0.331** · Exits ≈ **0.354** · Spread ≈ **0.024**
- Fills: 258 buys / 80 sells · hold 66d 13h · both-sides=True · realized $40,905.82

### CZ sentenced to less than 6 months in prison?
- Entries ≈ **0.305** · Exits ≈ **0.369** · Spread ≈ **0.064**
- Fills: 40 buys / 19 sells · hold 5d 23h · both-sides=True · realized $36,001.73

## Top closed winners / losers

**Winners**
- Will Kamala Harris win the 2024 Democratic Presidential Nomination?: $326,714.68 · bought $614,346.42 · sold $345,794.19 · hold 204d 17h
- Will JD Vance win the 2024 Republican VP nomination?: $232,267.78 · bought $70,812.22 · sold $63,162.62 · hold 154d 16h
- No change in Fed interest rates after 2024 September meeting?: $123,657.72 · bought $557,727.65 · sold $159,595.69 · hold 53d 2h
- Fed decreases interest rates by 50+ bps after September 2024 meeting?: $105,343.08 · bought $255,285.99 · sold $66,389.10 · hold 53d 9h
- Biden drops out of presidential race?: $89,816.48 · bought $864,637.44 · sold $412,414.99 · hold 301d 19h
- Will another candidate win the 2024 Republican VP nomination?: $89,328.73 · bought $14,511.04 · sold $0.00 · hold 66d 2h
- Will Fed cut interest rates 4 times in 2024?: $81,513.10 · bought $105,218.89 · sold $25,021.76 · hold 213d 20h
- Will 'Inside Out 2' gross most in 2024?: $71,576.93 · bought $108,825.66 · sold $930.05 · hold 256d 0h
- Fed decreases interest rates by 25 bps after November 2024 meeting?: $65,890.56 · bought $33,469.33 · sold $1,720.00 · hold 79d 2h
- Will Erdoğan win the 2023 Turkish presidential election?: $62,824.90 · bought $256,759.80 · sold $152,295.75 · hold 87d 1h

**Losers**
- Will Chris Christie win the 2024 US Presidential Election?: -$702,380.84 · bought $556.98 · sold $1,320.74
- Will Elizabeth Warren win the 2024 US Presidential Election?: -$702,031.32 · bought $2,481.03 · sold $3,420.78
- Will Bernie Sanders win the 2024 US Presidential Election?: -$701,513.72 · bought $2,632.66 · sold $1,562.34
- Will Vivek Ramaswamy win the 2024 US Presidential Election?: -$700,142.50 · bought $8,236.98 · sold $6,554.20
- Will Kanye West win the 2024 US Presidential Election?: -$698,953.42 · bought $5,865.82 · sold $2,441.10
- Will any other Republican Politician win the 2024 US Presidential Election?: -$693,213.93 · bought $9,231.40 · sold $13,154.06
- Will Hillary Clinton win the 2024 US Presidential Election?: -$688,153.04 · bought $41,642.24 · sold $3,925.09
- Will AOC win the 2024 US Presidential Election?: -$687,759.69 · bought $102,557.45 · sold $8,764.29
- Will Ron DeSantis win the 2024 US Presidential Election?: -$685,841.98 · bought $65,307.67 · sold $40,319.35
- Will any other Democratic Politician win the 2024 US Presidential Election?: -$680,019.60 · bought $58,680.77 · sold $29,439.18

## Replication playbook (how to copy the edge)

1. Restrict to their top categories by PnL contribution.
2. Mirror entry price percentiles and hold-time distribution rather than exact fills.
3. Enforce risk: their profit factor and max DD define a hard stop template.
4. Recompute weekly — edges decay when others copy the same tape.

## Cashflow anatomy

- Buys: $71,990,498.82
- Sells: $17,195,487.69
- Redeems: $9,988,870.32
- Maker rebates: $0.00
- Taker rebates: $0.00

_Generated 2026-08-28T14:44:11.295351+00:00_
