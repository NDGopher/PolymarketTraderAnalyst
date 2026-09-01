# Windows quick start — Suspension Edge Lab

## 1. Get the code on your PC

**Option A — Git (recommended)**

Open **Command Prompt** or **PowerShell**:

```bat
cd %USERPROFILE%\Documents
git clone -b cursor/suspension-edge-lab-35c6 https://github.com/NDGopher/PolymarketTraderAnalyst.git
cd PolymarketTraderAnalyst\polymarket-trader-analyzer
```

**Option B — Download ZIP (no Git)**

1. Open: https://github.com/NDGopher/PolymarketTraderAnalyst/tree/cursor/suspension-edge-lab-35c6
2. Click **Code → Download ZIP**
3. Extract the ZIP
4. Open folder: `PolymarketTraderAnalyst-main\polymarket-trader-analyzer`

---

## 2. Add your `.env` file

Copy your `.env` from your Kalshi project into:

```
polymarket-trader-analyzer\.env
```

Or copy the template:

```bat
copy .env.example .env
notepad .env
```

Your `.env` should look like:

```env
KALSHI_KEY_ID=your-key-id
KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY-----
...your key...
-----END RSA PRIVATE KEY-----"

LAB_TICKERS=YOUR_O35_TICKER,YOUR_O45_TICKER
LAB_GAME=Parma-Cremonese
```

---

## 3. One-click run

Double-click:

```
START_SUSPENSION_LAB.bat
```

First run installs Python dependencies automatically, then opens the lab window.

You can also double-click `START_SUSPENSION_LAB.bat` at the **repo root** (one folder up) — it forwards into the right directory.

---

## 4. During the match

| Key | Action |
|-----|--------|
| **B** | bet365 down / up toggle |
| **F** | FanDuel down / up toggle |
| **D** | DraftKings down / up toggle |

Logs save to:

```
polymarket-trader-analyzer\data\suspension_lab\sessions\<timestamp>_<game>\
```

---

## Requirements

- **Windows 10/11**
- **Python 3.11+** — https://www.python.org/downloads/ (check **Add to PATH**)
- Kalshi API key in `.env`

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Python not found` | Reinstall Python with "Add to PATH" checked |
| `No .env file` | Copy `.env.example` → `.env` and fill in credentials |
| Window doesn't open | Run bat from Command Prompt to see error text |
| WS fails, REST works | Check `KALSHI_KEY_ID` and `KALSHI_PRIVATE_KEY` in `.env |

Pull updates later:

```bat
cd PolymarketTraderAnalyst
git pull origin cursor/suspension-edge-lab-35c6
```
