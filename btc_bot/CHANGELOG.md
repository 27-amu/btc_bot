# Changelog

## v1.1.0 — 2026-06-18
- Return type hints added to all functions
- Max drawdown tracking in portfolio stats
- CSV trade history export on shutdown
- Optional file logging via `LOG_FILE` env var
- API fetch retry with exponential backoff
- Win/loss streak tracking + best/worst trade
- Formatted summary table on shutdown
- `notify.py` — Slack/Discord webhook + Telegram alerts
- `backtest.py` — run strategy against historical OHLCV data
- Unit tests (`tests/test_bot.py`)
- `pyproject.toml` and `requirements-dev.txt`
- Expanded `Makefile` and `.gitignore`

## v1.0.0 — 2026-06-15
- Triple RSI (2, 7, 14) + MA200 trend filter strategy
- Hard stop-loss (-2%) + trailing stop-loss (-1.5%)
- Paper trading mode with full PnL tracking
- Binance exchange via ccxt
