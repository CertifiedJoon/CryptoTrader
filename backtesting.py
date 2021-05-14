import ccxt
import get_k

binance = ccxt.binance()
#backtesting
btc_ohlcv = binance.fetch_ohlcv("BTC/USDT", '1d')
df = pd.DataFrame(btc_ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
df.set_index('datetime', inplace=True)
k = 0.5
df['range'] = (df['high'] - df['low']) * k
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0032
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())