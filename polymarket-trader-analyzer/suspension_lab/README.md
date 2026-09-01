# Suspension Edge Lab

Manual click logger for correlating **book suspensions** (bet365 / FanDuel / DraftKings) with **Kalshi orderbook** moves during live soccer O/U.

## Quick start

```bash
cd polymarket-trader-analyzer
pip install -e .

# Paste your Kalshi O/U tickers (comma-separated)
export KALSHI_API_KEY_ID="your-key-id"
export KALSHI_PRIVATE_KEY_PATH="/path/to/kalshi.pem"

suspension-lab run "TICKER_O25,TICKER_O35,TICKER_O45" --game "Parma-Cremonese"
```

Without Kalshi credentials, REST polling works (no auth, ~200ms):

```bash
suspension-lab run "TICKER1,TICKER2" --game "Parma-Cremonese" --rest-only
```

## Controls

| Key | Action |
|-----|--------|
| **B** | Toggle bet365 UP ↔ DOWN |
| **F** | Toggle FanDuel UP ↔ DOWN |
| **D** | Toggle DraftKings UP ↔ DOWN |

Each toggle writes a row to `events.csv` with full orderbook snapshots for all tickers plus markouts at +1s, +3s, +5s, +10s, +30s.

Continuous 200ms book samples go to `books.csv`.

## Output

```
data/suspension_lab/sessions/<timestamp>_<game>/
  session.json
  events.csv    ← your B/F clicks + markouts
  books.csv     ← high-frequency book tape
```

Markets with mid ≥ 90% (or ≤ 10%) are flagged `[BOND — skip]` in the UI.

## WebSocket vs REST

- **WebSocket** (`orderbook_delta`): needs `KALSHI_API_KEY_ID` + PEM path. Millisecond deltas.
- **REST** (`--rest-only`): public orderbook endpoint, no auth. Good enough for manual research.
