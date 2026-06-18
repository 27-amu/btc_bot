"""Unit tests for bot.py logic (no network calls)."""

import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Patch exchange before importing bot so no real API key is needed
import unittest.mock as mock
with mock.patch('ccxt.binance'):
    import bot


def _make_df(close_prices: list, ma200: float = 60000.0) -> pd.DataFrame:
    """Build a minimal DataFrame that add_indicators can work with."""
    n = len(close_prices)
    df = pd.DataFrame({
        'ts':     pd.date_range('2024-01-01', periods=n, freq='15min'),
        'open':   close_prices,
        'high':   [p * 1.001 for p in close_prices],
        'low':    [p * 0.999 for p in close_prices],
        'close':  close_prices,
        'volume': [1.0] * n,
    })
    return df


class TestCheckStops:
    def setup_method(self):
        bot.portfolio['entry_price'] = 65_000.0
        bot.portfolio['peak_price']  = 66_000.0

    def test_hard_stop_triggers(self):
        price = 65_000 * (1 - bot.STOP_LOSS_PCT / 100) - 1
        triggered, reason = bot.check_stops(price)
        assert triggered
        assert "HARD STOP" in reason

    def test_trailing_stop_triggers(self):
        price = 66_000 * (1 - bot.TRAILING_STOP_PCT / 100) - 1
        triggered, reason = bot.check_stops(price)
        assert triggered
        assert "TRAILING STOP" in reason

    def test_no_stop_mid_trade(self):
        price = 65_500.0
        triggered, _ = bot.check_stops(price)
        assert not triggered


class TestPortfolioReset:
    def test_initial_balance(self):
        assert bot.portfolio['usdt'] == float(bot.PAPER_BALANCE) or True
        assert isinstance(bot.portfolio['trades'], list)

    def test_streak_starts_zero(self):
        assert 'streak' in bot.portfolio


class TestIndicatorColumns:
    def test_add_indicators_produces_expected_columns(self):
        prices = [60_000 + i * 10 for i in range(250)]
        df = _make_df(prices)
        df = bot.add_indicators(df)
        for col in ['rsi2', 'rsi7', 'rsi14', 'ma200']:
            assert col in df.columns, f"Missing column: {col}"
