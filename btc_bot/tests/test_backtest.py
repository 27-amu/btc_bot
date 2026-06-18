"""Tests for the backtest engine."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pandas as pd
import unittest.mock as mock

with mock.patch('ccxt.binance'):
    import backtest


def _make_df_with_indicators(n: int = 300, base: float = 65_000.0) -> pd.DataFrame:
    prices = [base + i * 5 for i in range(n)]
    df = pd.DataFrame({
        'ts':     pd.date_range('2024-01-01', periods=n, freq='15min'),
        'open':   prices,
        'high':   [p * 1.001 for p in prices],
        'low':    [p * 0.999 for p in prices],
        'close':  prices,
        'volume': [1.0] * n,
    })
    return backtest.add_indicators(df)


class TestBacktestEngine:
    def test_returns_expected_keys(self):
        df = _make_df_with_indicators()
        result = backtest.run_backtest(df)
        for key in ['trades', 'wins', 'losses', 'win_rate', 'final_balance', 'net_pnl', 'max_drawdown']:
            assert key in result

    def test_final_balance_positive(self):
        df = _make_df_with_indicators()
        result = backtest.run_backtest(df)
        assert result['final_balance'] > 0

    def test_wins_plus_losses_equals_trades(self):
        df = _make_df_with_indicators()
        r = backtest.run_backtest(df)
        assert r['wins'] + r['losses'] == r['trades']

    def test_win_rate_within_bounds(self):
        df = _make_df_with_indicators()
        r = backtest.run_backtest(df)
        assert 0.0 <= r['win_rate'] <= 100.0
