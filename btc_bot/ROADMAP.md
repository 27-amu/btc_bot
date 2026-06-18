# Roadmap

## v1.1 (current)
- [x] Triple RSI + MA200 strategy
- [x] Hard stop-loss + trailing stop
- [x] Paper trading with full PnL tracking
- [x] Max drawdown tracking
- [x] CSV trade history export
- [x] File-based logging via `LOG_FILE` env var
- [x] Win/loss streak tracking
- [x] API retry with exponential backoff

## v1.2 (planned)
- [ ] Telegram / Discord trade notifications
- [ ] Persist portfolio state to JSON (resume after restart)
- [ ] Configurable RSI thresholds via `.env`
- [ ] Support multiple timeframes (4h, 1h)

## v2.0 (future)
- [ ] Backtest engine with historical OHLCV data
- [ ] Multi-pair support (ETH/USDT, SOL/USDT)
- [ ] Web dashboard for live trade monitoring
- [ ] Live trading mode (opt-in, with confirmation prompt)
