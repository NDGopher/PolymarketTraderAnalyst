# Suspension Edge Lab — copy/paste this in PowerShell

## If you're stuck in a merge conflict (run once)

```powershell
cd C:\PolymarketTraderAnalyst
git merge --abort
git fetch origin main
git reset --hard origin/main
```

Or double-click / run: `RESET_AND_RUN.ps1` at the repo root.

---

## Every time you want to run the lab

```powershell
cd C:\PolymarketTraderAnalyst
git pull origin main
cd polymarket-trader-analyzer
.\START_SUSPENSION_LAB.ps1
```

**Important:** In PowerShell use `.\START_SUSPENSION_LAB.ps1` (with `.\` prefix), not bare `START_SUSPENSION_LAB.bat`.

---

## Your `.env` goes here

```
C:\PolymarketTraderAnalyst\polymarket-trader-analyzer\.env
```

Must include:
- `KALSHI_KEY_ID=...`
- `KALSHI_PRIVATE_KEY="-----BEGIN RSA PRIVATE KEY----- ..."`
- `LAB_TICKERS=...`
- `LAB_GAME=Parma-Cremonese`

---

## Keys during the match

| Key | Action |
|-----|--------|
| B | bet365 down/up |
| F | FanDuel down/up |
| D | DraftKings down/up |
