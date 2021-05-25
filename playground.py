from Trader import Trader
import ccxt
import datetime
import time
import pause
import csv
import Phone
import pandas as pd
import pprint

bitcoin = Trader('BTC/USDT', 'log/BTCUSDT.csv')

info = bitcoin.BINANCE.fetch_ticker(bitcoin._ticker)
today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
new_row = [today, info['open'], info['high'], info['low'], info['close'], info['quoteVolume']]
        
with open(bitcoin._filename,'a') as fd:
    writer_object = csv.writer(fd)
    writer_object.writerow(new_row)
    fd.close()
        
bitcoin._df.loc[today] = pd.Series(new_row)