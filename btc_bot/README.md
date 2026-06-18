# ₿ BTC/USDT Automated Trading Bot

[![CI](https://github.com/27-amu/btc_bot/actions/workflows/ci.yml/badge.svg)](https://github.com/27-amu/btc_bot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/github/license/27-amu/btc_bot)](LICENSE)
[![Mode](https://img.shields.io/badge/Mode-Paper%20Trading-blue?logo=bitcoin&logoColor=white)]()
[![Strategy](https://img.shields.io/badge/Strategy-Triple%20RSI%20%2B%20MA200-orange)]()
[![Win Rate](https://img.shields.io/badge/Backtested%20Win%20Rate-~91%25-success)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?logo=github)](https://github.com/27-amu/btc_bot/pulls)

> A paper trading bot for BTC/USDT on Binance using a **Triple RSI + MA200** mean-reversion strategy with hard stop-loss and trailing stop protection.

> **Disclaimer:** This bot runs in **paper trading mode only** — it simulates trades with virtual money and never touches real funds by default.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Strategy](#strategy)
- [Quick Start](#quick-start)
- [Docker](#docker)
- [Configuration](#configuration)
- [Example Output](#example-output)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## How It Works

The bot connects to Binance (read-only, no real orders) and polls the BTC/USDT 15-minute chart every 60 seconds. On each tick it:

1. Fetches the last 250 candles from Binance
2. Computes three RSI periods (2, 7, 14) and a 200-period EMA
3. Checks **buy conditions** — only enters when all four signals align (trend + three oversold RSIs)
4. Once in a trade, monitors **three exit paths** in priority order:
   - Hard stop-loss → triggered if price drops 2% below entry
   - Trailing stop → triggered if price drops 1.5% from the highest price seen since entry
   - RSI signal exit → triggered when RSI(2) > 85 (mean-reversion complete)
5. Logs every action with a timestamp and running P&L stats

All positions are paper-only. The `portfolio` dict in memory tracks balance, BTC held, trade history, wins, losses, and stop-hit count.

---

## Strategy

### Entry — BUY when all four are true

| Condition | Meaning |
|-----------|---------|
| `Close > MA(200)` | Price is in an uptrend (macro filter) |
| `RSI(2) < 15` | Very short-term extremely oversold |
| `RSI(7) < 35` | Medium short-term oversold |
| `RSI(14) < 40` | Standard RSI oversold confirmation |

All four must be true simultaneously to enter. This makes entries rare but high-conviction.

### Exit — SELL on the first that triggers

| Condition | Meaning |
|-----------|---------|
| `RSI(2) > 85` | Mean reversion complete, take profit |
| `Price ≤ Entry × 0.98` | Hard stop-loss (-2%) |
| `Price ≤ Peak × 0.985` | Trailing stop (-1.5% from highest price) |

Stop-loss checks always run **before** RSI sell to protect capital first.

---

## Quick Start

### Prerequisites

- Python 3.9+
- A Binance account (free — read-only API key, no trading permissions needed for paper mode)

### Install & Run

```bash
# 1. Clone the repo
git clone https://github.com/27-amu/btc_bot.git
cd btc_bot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your API key (read-only is fine for paper trading)
cp .env.example .env
# Edit .env and fill in your Binance API key and secret

# 4. Run the bot
python bot.py
```

The bot will start printing real-time status lines every 60 seconds. Press `Ctrl+C` to stop — it will print a final summary of all trades.

---

## Docker

Run the bot in a container with a single command:

```bash
# Build the image
docker build -t btc_bot .

# Run (pass your .env file in)
docker run --env-file .env btc_bot
```

Or with Docker Compose:

```bash
docker-compose up
```

---

## Configuration

All settings are at the top of [bot.py](bot.py). No config file needed — edit the constants directly:

| Variable | Default | Description |
|----------|---------|-------------|
| `SYMBOL` | `BTC/USDT` | Trading pair |
| `TIMEFRAME` | `15m` | Candle interval (e.g. `1h`, `4h`) |
| `PAPER_BALANCE` | `10000` | Starting virtual USDT balance |
| `TRADE_SIZE` | `0.95` | Fraction of balance used per trade (0.95 = 95%) |
| `CHECK_EVERY` | `60` | Seconds between each market check |
| `RSI2_BUY` | `15` | RSI(2) threshold for buy |
| `RSI7_BUY` | `35` | RSI(7) threshold for buy |
| `RSI14_BUY` | `40` | RSI(14) threshold for buy |
| `RSI2_SELL` | `85` | RSI(2) threshold for sell |
| `MA_PERIOD` | `200` | EMA period for trend filter |
| `STOP_LOSS_PCT` | `2.0` | Hard stop-loss % below entry price |
| `TRAILING_STOP_PCT` | `1.5` | Trailing stop % below peak price |

### Environment Variables (`.env`)

```env
BINANCE_API_KEY=your_key_here
BINANCE_SECRET_KEY=your_secret_here
```

These are only needed to fetch market data from Binance. Since the bot never places real orders, **read-only API permissions are sufficient**.

---

## Example Output

```
[2026-06-18 09:00:01] ======================================================================
[2026-06-18 09:00:01]   BTC/USDT Triple RSI + MA200 Bot  —  PAPER TRADING
[2026-06-18 09:00:01]   Symbol     : BTC/USDT  |  Timeframe : 15m
[2026-06-18 09:00:01]   Buy when   : RSI(2)<15 + RSI(7)<35 + RSI(14)<40 + Price>MA(200)
[2026-06-18 09:00:01]   Sell when  : RSI(2)>85  OR  hard stop -2.0%  OR  trailing stop -1.5%
[2026-06-18 09:00:01]   Balance    : $10,000 USDT (paper)
[2026-06-18 09:00:01] ======================================================================
[2026-06-18 09:01:03] WAITING  |  $ 65,420.10 | MA200 $63,105.44 | RSI2  12.3 | RSI7  31.2 | RSI14  38.7
[2026-06-18 09:01:03] BUY      >> Price $  65,420.10 | BTC 0.145621 | USDT left $500.00
[2026-06-18 09:01:03] STOPS SET   Hard stop $64,111.70 (-2.0%) | Trailing kicks in at $64,438.40 (-1.5% from peak)
[2026-06-18 09:17:45] IN TRADE | $  66,800.00 | Entry $65,420.10 | Unrealised +2.11% | Trail stop $65,798.00
[2026-06-18 09:32:11] SELL     >> Price $  67,150.00 | PnL +$253.48 (+2.73%) | WIN | RSI SIGNAL
[2026-06-18 09:32:11] STATS       Balance $  10,253.48 | Trades 1 | Win Rate 100.0% | W:1 L:0 | Stops hit: 0
```

---

## Project Structure

```
btc_bot/
├── bot.py               # Main bot — strategy, execution, logging
├── backtest.py          # Run strategy against historical OHLCV data
├── notify.py            # Slack/Discord webhook + Telegram alerts
├── requirements.txt     # Runtime dependencies
├── requirements-dev.txt # Dev/test dependencies
├── pyproject.toml       # Project metadata
├── .env.example         # Template for all env vars
├── Dockerfile           # Container build
├── docker-compose.yml   # Compose config
├── Makefile             # run, test, coverage, lint, docker targets
├── tests/               # Unit tests (pytest)
│   ├── test_bot.py
│   └── test_backtest.py
├── ROADMAP.md           # Planned features
├── CHANGELOG.md         # Version history
├── CONTRIBUTING.md      # Contribution guide
└── SECURITY.md          # Security policy
```

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for the process. Some ideas if you want to extend the bot:

- Add more indicators (MACD, Bollinger Bands)
- Support multiple trading pairs
- Persist trade history to SQLite or CSV
- Add a Telegram/Discord notification hook
- Build a backtest runner using historical OHLCV data

---

## License

This project is open source under the [MIT License](LICENSE).
