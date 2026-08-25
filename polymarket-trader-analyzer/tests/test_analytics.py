from polyanalyst.analytics import compute_cashflow, compute_closed_pnl


def test_cashflow_polydata_style():
    activity = [
        {"type": "TRADE", "side": "BUY", "usdcSize": 100},
        {"type": "TRADE", "side": "SELL", "usdcSize": 140},
        {"type": "REDEEM", "usdcSize": 10},
        {"type": "MAKER_REBATE", "usdcSize": 2},
    ]
    cf = compute_cashflow(activity)
    assert cf.buys_usdc == 100
    assert cf.sells_usdc == 140
    assert cf.redeems_usdc == 10
    assert cf.realized_core == 50
    assert cf.realized_cashflow == 52


def test_closed_pnl_win_rate():
    closed = [
        {"realizedPnl": 10, "totalBought": 5},
        {"realizedPnl": -4, "totalBought": 4},
        {"realizedPnl": 0, "totalBought": 1},
    ]
    cp = compute_closed_pnl(closed)
    assert cp.wins == 1
    assert cp.losses == 1
    assert cp.flat == 1
    assert abs(cp.win_rate - 0.5) < 1e-9
    assert abs(cp.realized_sum - 6) < 1e-9
