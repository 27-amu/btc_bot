"""
Backtest runner for the Triple RSI + MA200 strategy.

Usage:
    python backtest.py --symbol BTC/USDT --timeframe 15m --days 90

Requires a Binance API key in .env (read-only is fine).
"""

import argparse
import ccxt
import pandas as pd
import ta as ta_lib
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ─── defaults match bot.py ───────────────────
RSI2_BUY          = 15
RSI7_BUY          = 35
RSI14_BUY         = 40
RSI2_SELL         = 85
MA_PERIOD         = 200
STOP_LOSS_PCT     = 2.0
TRAILING_STOP_PCT = 1.5
TRADE_SIZE        = 0.95
PAPER_BALANCE     = 10_000


def fetch_history(symbol: str, timeframe: str, days: int) -> pd.DataFrame:
    exchange = ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET_KEY'),
        'enableRateLimit': True,
    })
    since = int((datetime.utcnow() - timedelta(days=days)).timestamp() * 1000)
    all_candles = []
    while True:
        candles = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not candles:
            break
        all_candles.extend(candles)
        since = candles[-1][0] + 1
        if len(candles) < 1000:
            break
    df = pd.DataFrame(all_candles, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    return df.drop_duplicates('ts').reset_index(drop=True)


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['rsi2']  = ta_lib.momentum.RSIIndicator(df['close'], window=2).rsi()
    df['rsi7']  = ta_lib.momentum.RSIIndicator(df['close'], window=7).rsi()
    df['rsi14'] = ta_lib.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ma200'] = ta_lib.trend.EMAIndicator(df['close'], window=MA_PERIOD).ema_indicator()
    return df


def run_backtest(df: pd.DataFrame) -> dict:
    balance    = float(PAPER_BALANCE)
    btc        = 0.0
    in_trade   = False
    entry      = 0.0
    peak       = 0.0
    wins       = losses = stops = 0
    trades     = []
    peak_bal   = balance
    max_dd     = 0.0

    for _, row in df.iterrows():
        if pd.isna(row['ma200']):
            continue

        price = row['close']

        if in_trade and price > peak:
            peak = price

        if not in_trade:
            buy = (
                price > row['ma200']
                and row['rsi2']  < RSI2_BUY
                and row['rsi7']  < RSI7_BUY
                and row['rsi14'] < RSI14_BUY
            )
            if buy:
                spend  = balance * TRADE_SIZE
                btc    = spend / price
                balance -= spend
                entry  = price
                peak   = price
                in_trade = True
        else:
            hard_stop     = entry * (1 - STOP_LOSS_PCT / 100)
            trailing_stop = peak  * (1 - TRAILING_STOP_PCT / 100)
            sell_signal   = row['rsi2'] > RSI2_SELL

            reason = None
            if price <= hard_stop:
                reason = "HARD_STOP"
            elif price <= trailing_stop:
                reason = "TRAILING_STOP"
            elif sell_signal:
                reason = "RSI_SIGNAL"

            if reason:
                usdt_back = btc * price
                pnl       = usdt_back - (btc * entry)
                balance  += usdt_back
                btc       = 0.0
                in_trade  = False

                if pnl >= 0:
                    wins += 1
                else:
                    losses += 1
                    if "STOP" in reason:
                        stops += 1

                trades.append({'entry': entry, 'exit': price, 'pnl': pnl, 'reason': reason})

                if balance > peak_bal:
                    peak_bal = balance
                dd = (peak_bal - balance) / peak_bal * 100
                if dd > max_dd:
                    max_dd = dd

    total    = wins + losses
    win_rate = (wins / total * 100) if total else 0.0
    return {
        'trades':       total,
        'wins':         wins,
        'losses':       losses,
        'win_rate':     win_rate,
        'final_balance': balance,
        'net_pnl':      balance - PAPER_BALANCE,
        'max_drawdown': max_dd,
        'stop_hits':    stops,
    }


def main():
    parser = argparse.ArgumentParser(description='Backtest BTC bot strategy')
    parser.add_argument('--symbol',    default='BTC/USDT')
    parser.add_argument('--timeframe', default='15m')
    parser.add_argument('--days',      type=int, default=90)
    args = parser.parse_args()

    print(f"Fetching {args.days} days of {args.symbol} {args.timeframe} data…")
    df = fetch_history(args.symbol, args.timeframe, args.days)
    df = add_indicators(df)
    print(f"Loaded {len(df)} candles. Running backtest…\n")

    r = run_backtest(df)
    print(f"  Trades       : {r['trades']}")
    print(f"  Win Rate     : {r['win_rate']:.1f}%  ({r['wins']}W / {r['losses']}L)")
    print(f"  Final Balance: ${r['final_balance']:,.2f}  (net {r['net_pnl']:+,.2f})")
    print(f"  Max Drawdown : {r['max_drawdown']:.2f}%")
    print(f"  Stop hits    : {r['stop_hits']}")


if __name__ == '__main__':
    main()
