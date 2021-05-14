import ccxt
import numpy as np
import pandas as pd
import time
import datetime
#"BTC/USDT"

def get_df(binance, ticker):
    btc_ohlcv = binance.fetch_ohlcv(ticker, '1d')
    df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    return df

def get_price(binance, ticker): #market is a class from ccxt
    price = binance.fetch_ticker(ticker)
    return price['ask']

def get_target(df):
    yesterday = df.iloc[-2]
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def get_bestk(df):
    maxi = 0
    for k in np.arange(0.1, 1.0, 0.05):
        ror = _get_ror(k, df)
        if ror > maxi:
            maxi = ror
    return maxi
    
def _get_ror(k, df):
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror

binance = ccxt.binance()
df = get_df(binance, "BTC/USDT")

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

target_price = get_target(df)

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.delta(seconds=10):
        target_price = get_target(df)
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        
    current_price = get_price(binance, "BTC/USDT")
    print(current_price, target_price)
    
    time.sleep(1)