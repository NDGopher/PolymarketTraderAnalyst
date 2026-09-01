from __future__ import annotations

import re
import threading
from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class MarketLabel:
    ticker: str
    display: str
    competition: str
    matchup: str
    line: str

    @staticmethod
    def fallback(ticker: str) -> MarketLabel:
        suffix = ticker.rsplit("-", 1)[-1]
        line = ""
        if suffix.isdigit():
            n = int(suffix)
            line = f"Over {n - 1}.5" if "TOTAL" in ticker.upper() else f"Line {n}"
        return MarketLabel(
            ticker=ticker,
            display=ticker,
            competition="",
            matchup="",
            line=line,
        )


def _clean_matchup(title: str) -> str:
    text = title.strip()
    if ":" in text:
        text = text.split(":", 1)[0].strip()
    return text


def _line_from_market(market: dict) -> str:
    sub = (market.get("yes_sub_title") or market.get("no_sub_title") or "").strip()
    if sub:
        m = re.search(r"over\s+([\d.]+)", sub, re.I)
        if m:
            return f"Over {m.group(1)}"
        return sub
    strike = market.get("floor_strike")
    if strike is not None:
        return f"Over {strike}"
    title = market.get("title") or ""
    m = re.search(r"over\s+([\d.]+)", title, re.I)
    if m:
        return f"Over {m.group(1)}"
    return (market.get("title") or "").strip()


def fetch_market_label(ticker: str, *, rest_base: str, session: requests.Session | None = None) -> MarketLabel:
    http = session or requests.Session()
    try:
        m_resp = http.get(f"{rest_base}/markets/{ticker}", timeout=8)
        m_resp.raise_for_status()
        market = m_resp.json().get("market") or {}
    except Exception:  # noqa: BLE001
        return MarketLabel.fallback(ticker)

    event_ticker = market.get("event_ticker") or ""
    competition = ""
    matchup = ""
    if event_ticker:
        try:
            e_resp = http.get(f"{rest_base}/events/{event_ticker}", timeout=8)
            e_resp.raise_for_status()
            event = e_resp.json().get("event") or {}
            meta = event.get("product_metadata") or {}
            competition = (meta.get("competition") or event.get("series_ticker") or "").strip()
            matchup = _clean_matchup(event.get("title") or event.get("sub_title") or "")
        except Exception:  # noqa: BLE001
            pass

    line = _line_from_market(market)
    if not matchup:
        matchup = _clean_matchup(market.get("title") or ticker)

    parts = [p for p in (competition, matchup, line) if p]
    display = " — ".join(parts) if parts else ticker
    return MarketLabel(
        ticker=ticker,
        display=display,
        competition=competition,
        matchup=matchup,
        line=line,
    )


class MarketLabelCache:
    def __init__(self, tickers: list[str], *, rest_base: str) -> None:
        self._rest_base = rest_base
        self._labels: dict[str, MarketLabel] = {t: MarketLabel.fallback(t) for t in tickers}
        self._lock = threading.Lock()
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "suspension-lab/0.1"})

    def get(self, ticker: str) -> MarketLabel:
        with self._lock:
            return self._labels.get(ticker, MarketLabel.fallback(ticker))

    def load_all(self, on_update=None) -> None:
        for ticker in list(self._labels):
            label = fetch_market_label(ticker, rest_base=self._rest_base, session=self._session)
            with self._lock:
                self._labels[ticker] = label
            if on_update:
                on_update(ticker, label)

    def load_all_async(self, on_update=None) -> threading.Thread:
        thread = threading.Thread(
            target=self.load_all,
            kwargs={"on_update": on_update},
            name="market-label-loader",
            daemon=True,
        )
        thread.start()
        return thread
