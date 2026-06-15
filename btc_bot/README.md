# ₿ BTC/USDT Automated Trading Bot

<!-- ═══════════════════════════════════════════════════════════════════════
     CI / CD
════════════════════════════════════════════════════════════════════════ -->
[![CI](https://github.com/27-amu/btc_bot/actions/workflows/ci.yml/badge.svg)](https://github.com/27-amu/btc_bot/actions/workflows/ci.yml)

<!-- ═══════════════════════════════════════════════════════════════════════
     GITHUB STATS
════════════════════════════════════════════════════════════════════════ -->
[![Stars](https://img.shields.io/github/stars/27-amu/btc_bot?style=social)](https://github.com/27-amu/btc_bot/stargazers)
[![Forks](https://img.shields.io/github/forks/27-amu/btc_bot?style=social)](https://github.com/27-amu/btc_bot/network/members)
[![Watchers](https://img.shields.io/github/watchers/27-amu/btc_bot?style=social)](https://github.com/27-amu/btc_bot/watchers)
[![GitHub followers](https://img.shields.io/github/followers/27-amu?style=social&label=Follow)](https://github.com/27-amu)

<!-- ═══════════════════════════════════════════════════════════════════════
     REPO META
════════════════════════════════════════════════════════════════════════ -->
[![Last Commit](https://img.shields.io/github/last-commit/27-amu/btc_bot?color=brightgreen)](https://github.com/27-amu/btc_bot/commits)
[![Commit Activity](https://img.shields.io/github/commit-activity/m/27-amu/btc_bot)](https://github.com/27-amu/btc_bot/graphs/commit-activity)
[![Contributors](https://img.shields.io/github/contributors/27-amu/btc_bot)](https://github.com/27-amu/btc_bot/graphs/contributors)
[![Open Issues](https://img.shields.io/github/issues/27-amu/btc_bot)](https://github.com/27-amu/btc_bot/issues)
[![Closed Issues](https://img.shields.io/github/issues-closed/27-amu/btc_bot?color=red)](https://github.com/27-amu/btc_bot/issues?q=is%3Aissue+is%3Aclosed)
[![Open PRs](https://img.shields.io/github/issues-pr/27-amu/btc_bot)](https://github.com/27-amu/btc_bot/pulls)
[![Closed PRs](https://img.shields.io/github/issues-pr-closed/27-amu/btc_bot?color=red)](https://github.com/27-amu/btc_bot/pulls?q=is%3Apr+is%3Aclosed)
[![License](https://img.shields.io/github/license/27-amu/btc_bot)](LICENSE)
[![Repo Size](https://img.shields.io/github/repo-size/27-amu/btc_bot)](https://github.com/27-amu/btc_bot)
[![Code Size](https://img.shields.io/github/languages/code-size/27-amu/btc_bot)](https://github.com/27-amu/btc_bot)

<!-- ═══════════════════════════════════════════════════════════════════════
     LANGUAGE & TECH STACK
════════════════════════════════════════════════════════════════════════ -->
[![Top Language](https://img.shields.io/github/languages/top/27-amu/btc_bot?color=3572A5)](https://github.com/27-amu/btc_bot)
[![Language Count](https://img.shields.io/github/languages/count/27-amu/btc_bot)](https://github.com/27-amu/btc_bot)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![ccxt](https://img.shields.io/badge/ccxt-4.2%2B-00D4AA?logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PC9zdmc+)](https://github.com/ccxt/ccxt)
[![Binance](https://img.shields.io/badge/Exchange-Binance-F0B90B?logo=binance&logoColor=white)](https://www.binance.com/)

<!-- ═══════════════════════════════════════════════════════════════════════
     BOT STATUS & STRATEGY
════════════════════════════════════════════════════════════════════════ -->
[![Mode](https://img.shields.io/badge/Mode-Paper%20Trading-blue?logo=bitcoin&logoColor=white)]()
[![Strategy](https://img.shields.io/badge/Strategy-Triple%20RSI%20%2B%20MA200-orange)]()
[![Win Rate](https://img.shields.io/badge/Backtested%20Win%20Rate-~91%25-success)]()
[![Symbol](https://img.shields.io/badge/Symbol-BTC%2FUSDT-F7931A?logo=bitcoin&logoColor=white)]()
[![Timeframe](https://img.shields.io/badge/Timeframe-15m-blueviolet)]()

<!-- ═══════════════════════════════════════════════════════════════════════
     PROJECT STATUS
════════════════════════════════════════════════════════════════════════ -->
[![Maintenance](https://img.shields.io/badge/Maintained-yes-green)](https://github.com/27-amu/btc_bot)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?logo=github)](https://github.com/27-amu/btc_bot/pulls)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red)](https://github.com/27-amu/btc_bot)
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-ff69b4)]()

<!-- ═══════════════════════════════════════════════════════════════════════
     VISITOR COUNTER
════════════════════════════════════════════════════════════════════════ -->
![Visitor Count](https://komarev.com/ghpvc/?username=27-amu&repo=btc_bot&label=Profile%20Views&color=brightgreen&style=flat)

---

## Overview

A fully automated **BTC/USDT paper trading bot** powered by a **Triple RSI (2, 7, 14) + MA200 trend filter** strategy with hard stop-loss and trailing stop-loss protection.

> **Disclaimer:** This bot is for educational/paper trading purposes only. It does not trade real money by default.

---

## Strategy

| Signal | Condition |
|--------|-----------|
| **BUY**  | Price > MA(200) AND RSI(2) < 15 AND RSI(7) < 35 AND RSI(14) < 40 |
| **SELL** | RSI(2) > 85 OR Hard Stop (-2%) OR Trailing Stop (-1.5% from peak) |

---

## Quick Start

```bash
# Clone
git clone https://github.com/27-amu/btc_bot.git
cd btc_bot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "BINANCE_API_KEY=your_key_here" > .env
echo "BINANCE_SECRET_KEY=your_secret_here" >> .env

# Run (paper trading — no real money)
python bot.py
```

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SYMBOL` | `BTC/USDT` | Trading pair |
| `TIMEFRAME` | `15m` | Candle interval |
| `PAPER_BALANCE` | `10,000` | Starting USDT (paper) |
| `TRADE_SIZE` | `0.95` | Fraction of balance per trade |
| `STOP_LOSS_PCT` | `2.0` | Hard stop-loss % below entry |
| `TRAILING_STOP_PCT` | `1.5` | Trailing stop % below peak |

---

## Dependencies

```
ccxt>=4.2.0
pandas>=2.0.0
ta>=0.11.0
python-dotenv>=1.0.0
```

---

## License

This project is open source. See [LICENSE](LICENSE) for details.
