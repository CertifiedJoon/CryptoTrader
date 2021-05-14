import ccxt
import pprint
import pandas as pd

# get ticker info
binance = ccxt.binance()
btc = binance.fetch_ticker("BTC/USDT")
pprint.pprint(btc)

# get history for every minute
btc_ohlcv = binance.fetch_ohlcv("BTC/USDT")

df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
print(df)

#get daily history
btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1d')

df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
print(df)

#get current price
while True:
    price = binance.fetch_ticker("BTC/USDT")
    print(price['ask'])
    time.sleep(0.2)

