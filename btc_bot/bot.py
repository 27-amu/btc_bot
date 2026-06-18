"""
BTC/USDT Automated Trading Bot
Strategy: Triple RSI (2, 7, 14) + MA200 Trend Filter
Protection: Hard Stop-Loss + Trailing Stop-Loss
Documented win rate: ~91% (backtested)
Mode: PAPER TRADING (no real money)
"""

import ccxt
import pandas as pd
import ta as ta_lib
import time
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG — tweak these
# ─────────────────────────────────────────────
SYMBOL        = 'BTC/USDT'
TIMEFRAME     = '15m'
PAPER_BALANCE = 10_000
TRADE_SIZE    = 0.95        # fraction of balance per trade
CHECK_EVERY   = 60          # seconds between checks

# Triple RSI thresholds
RSI2_BUY   = 15
RSI7_BUY   = 35
RSI14_BUY  = 40
RSI2_SELL  = 85
MA_PERIOD  = 200

# Stop-loss settings
STOP_LOSS_PCT      = 2.0
TRAILING_STOP_PCT  = 1.5

# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────
exchange = ccxt.binance({
    'apiKey':  os.getenv('BINANCE_API_KEY'),
    'secret':  os.getenv('BINANCE_SECRET_KEY'),
    'enableRateLimit': True,
})

portfolio = {
    'usdt':         float(PAPER_BALANCE),
    'btc':          0.0,
    'in_trade':     False,
    'entry_price':  0.0,
    'peak_price':   0.0,
    'wins':         0,
    'losses':       0,
    'stop_hits':    0,
    'trades':       [],
    'peak_balance': float(PAPER_BALANCE),
    'max_drawdown': 0.0,
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def log(msg: str) -> None:
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{ts}] {msg}")

def fetch_candles() -> pd.DataFrame:
    ohlcv = exchange.fetch_ohlcv(SYMBOL, TIMEFRAME, limit=250)
    df = pd.DataFrame(ohlcv, columns=['ts', 'open', 'high', 'low', 'close', 'volume'])
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df['rsi2']  = ta_lib.momentum.RSIIndicator(df['close'], window=2).rsi()
    df['rsi7']  = ta_lib.momentum.RSIIndicator(df['close'], window=7).rsi()
    df['rsi14'] = ta_lib.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['ma200'] = ta_lib.trend.EMAIndicator(df['close'], window=MA_PERIOD).ema_indicator()
    return df

def get_signals(df: pd.DataFrame) -> tuple:
    r = df.iloc[-1]
    buy = (
        r['close'] > r['ma200']
        and r['rsi2']  < RSI2_BUY
        and r['rsi7']  < RSI7_BUY
        and r['rsi14'] < RSI14_BUY
    )
    sell = r['rsi2'] > RSI2_SELL
    return buy, sell, r

def check_stops(price: float) -> tuple:
    entry = portfolio['entry_price']
    peak  = portfolio['peak_price']

    hard_stop     = entry * (1 - STOP_LOSS_PCT / 100)
    trailing_stop = peak  * (1 - TRAILING_STOP_PCT / 100)

    if price <= hard_stop:
        return True, f"HARD STOP (entry ${entry:,.2f} → stop ${hard_stop:,.2f})"
    if price <= trailing_stop:
        return True, f"TRAILING STOP (peak ${peak:,.2f} → stop ${trailing_stop:,.2f})"
    return False, ""

# ─────────────────────────────────────────────
# PAPER TRADE EXECUTION
# ─────────────────────────────────────────────
def execute_buy(price: float) -> None:
    spend = portfolio['usdt'] * TRADE_SIZE
    btc   = spend / price
    portfolio['usdt']        -= spend
    portfolio['btc']         += btc
    portfolio['in_trade']     = True
    portfolio['entry_price']  = price
    portfolio['peak_price']   = price

    hard_stop    = price * (1 - STOP_LOSS_PCT / 100)
    trailing_ref = price * (1 - TRAILING_STOP_PCT / 100)

    log(f"BUY      >> Price ${price:>10,.2f} | BTC {btc:.6f} | USDT left ${portfolio['usdt']:,.2f}")
    log(f"STOPS SET   Hard stop ${hard_stop:,.2f} (-{STOP_LOSS_PCT}%) | Trailing kicks in at ${trailing_ref:,.2f} (-{TRAILING_STOP_PCT}% from peak)")

def execute_sell(price: float, reason: str = "RSI SIGNAL") -> None:
    usdt_back = portfolio['btc'] * price
    cost      = portfolio['btc'] * portfolio['entry_price']
    pnl       = usdt_back - cost
    pct       = (pnl / cost) * 100

    portfolio['usdt']      += usdt_back
    portfolio['btc']        = 0.0
    portfolio['in_trade']   = False
    portfolio['peak_price'] = 0.0

    if pnl >= 0:
        portfolio['wins'] += 1
        outcome = "WIN"
    else:
        portfolio['losses'] += 1
        outcome = "LOSS"
        if "STOP" in reason:
            portfolio['stop_hits'] += 1

    portfolio['trades'].append({
        'entry':  portfolio['entry_price'],
        'exit':   price,
        'pnl':    pnl,
        'pct':    pct,
        'reason': reason,
    })

    total    = portfolio['wins'] + portfolio['losses']
    win_rate = (portfolio['wins'] / total * 100) if total else 0.0

    # Update peak balance and max drawdown
    if portfolio['usdt'] > portfolio['peak_balance']:
        portfolio['peak_balance'] = portfolio['usdt']
    dd = (portfolio['peak_balance'] - portfolio['usdt']) / portfolio['peak_balance'] * 100
    if dd > portfolio['max_drawdown']:
        portfolio['max_drawdown'] = dd

    log(f"SELL     >> Price ${price:>10,.2f} | PnL ${pnl:+,.2f} ({pct:+.2f}%) | {outcome} | {reason}")
    log(f"STATS       Balance ${portfolio['usdt']:>10,.2f} | Trades {total} | Win Rate {win_rate:.1f}% | W:{portfolio['wins']} L:{portfolio['losses']} | Stops hit: {portfolio['stop_hits']} | MaxDD {portfolio['max_drawdown']:.2f}%")

# ─────────────────────────────────────────────
# SUMMARY & EXPORT
# ─────────────────────────────────────────────
def _print_summary() -> None:
    total    = portfolio['wins'] + portfolio['losses']
    win_rate = (portfolio['wins'] / total * 100) if total else 0.0
    log(f"Final Balance  : ${portfolio['usdt']:,.2f} USDT")
    log(f"Total Trades   : {total}  |  Win Rate: {win_rate:.1f}%  |  Stops hit: {portfolio['stop_hits']}  |  Max Drawdown: {portfolio['max_drawdown']:.2f}%")

def _export_trades_csv() -> None:
    if not portfolio['trades']:
        return
    import csv
    filename = f"trades_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['entry', 'exit', 'pnl', 'pct', 'reason'])
        writer.writeheader()
        writer.writerows(portfolio['trades'])
    log(f"Trade history saved → {filename}")

# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
def run() -> None:
    log("=" * 70)
    log("  BTC/USDT Triple RSI + MA200 Bot  —  PAPER TRADING")
    log(f"  Symbol     : {SYMBOL}  |  Timeframe : {TIMEFRAME}")
    log(f"  Buy when   : RSI(2)<{RSI2_BUY} + RSI(7)<{RSI7_BUY} + RSI(14)<{RSI14_BUY} + Price>MA({MA_PERIOD})")
    log(f"  Sell when  : RSI(2)>{RSI2_SELL}  OR  hard stop -{STOP_LOSS_PCT}%  OR  trailing stop -{TRAILING_STOP_PCT}%")
    log(f"  Balance    : ${PAPER_BALANCE:,} USDT (paper)")
    log("=" * 70)

    while True:
        try:
            df              = fetch_candles()
            df              = add_indicators(df)
            buy, sell, last = get_signals(df)
            price           = last['close']

            if portfolio['in_trade'] and price > portfolio['peak_price']:
                portfolio['peak_price'] = price

            if portfolio['in_trade']:
                entry       = portfolio['entry_price']
                peak        = portfolio['peak_price']
                unrealised  = ((price - entry) / entry) * 100
                trail_level = peak * (1 - TRAILING_STOP_PCT / 100)
                status_line = (
                    f"IN TRADE | ${price:>10,.2f} | Entry ${entry:,.2f} | "
                    f"Unrealised {unrealised:+.2f}% | Trail stop ${trail_level:,.2f}"
                )
            else:
                status_line = (
                    f"WAITING  | ${price:>10,.2f} | MA200 ${last['ma200']:,.2f} | "
                    f"RSI2 {last['rsi2']:>5.1f} | RSI7 {last['rsi7']:>5.1f} | RSI14 {last['rsi14']:>5.1f}"
                )
            log(status_line)

            if not portfolio['in_trade']:
                if buy:
                    execute_buy(price)
            else:
                stopped, stop_reason = check_stops(price)
                if stopped:
                    execute_sell(price, reason=stop_reason)
                elif sell:
                    execute_sell(price, reason="RSI SIGNAL")

        except KeyboardInterrupt:
            log("Bot stopped.")
            _print_summary()
            _export_trades_csv()
            break
        except Exception as e:
            log(f"ERROR: {e}")

        time.sleep(CHECK_EVERY)

if __name__ == '__main__':
    run()
