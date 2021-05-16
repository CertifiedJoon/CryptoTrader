import ccxt
import numpy as np
import pandas as pd
import Series
import time
import datetime
import math
from datetime import timedelta
import numpy as np
from sklearn import preprocessing, svm
from sklearn.svm import SVR


class Trader():
    with open("api.txt") as f:
        lines = f.readlines()
        api_key = lines[0].strip() 
        secret = lines[1].strip() 
    
    BINANCE = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret
    })
    
    def __init__(self, ticker, file):
        self._ticker = ticker
        self._filename = file
        df = pd.read_csv(file)
        self._df = df.set_index('Date')
        
    def get_df(self):
        return self._df

    def get_price(self): #market is a class from ccxt
        price = BINANCE.fetch_ticker(ticker)
        return price['ask']

    def get_target(self):
        yesterday = self._df.iloc[-2]
        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        k = self.get_bestk()
        target = today_open + (yesterday_high - yesterday_low) * k
        return target

    def get_bestk(self):
        max_ror = 0
        best_k = 0.5
        for k in np.arange(0.1, 1.0, 0.05):
            ror = _get_ror(k)
            if ror > maxi:
                maxi = ror
                best_k = k
        return best_k

    def _get_ror(self, k):
        self._df['range'] = (self._df['high'] - self._df['low']) * k
        self._df['target'] = self._df['open'] + self._df['range'].shift(1)

        fee = 0.0032
        self._df['ror'] = np.where(self._df['high'] > self._df['target'],
                             self._df['close'] / self._df['target'] - fee,
                             1)

        ror = self._df['ror'].cumprod()[-2]
        return ror

    def update_ohlcv(self):
        info = BINANCE.fetch_ticker(self._ticker)
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        new_row = [today, info['open'], info['high'], info['low'], info['close'], info['volume']]
        
        with open(self._filename,'a') as fd:
            writer_object = writer(fd)
            wrtier_object.writerow(new_row)
            fd.close()
        
        self._df.loc[today] = Series(new_row)
        
    def get_sentiment(self): #get prediction price for next day, return predicted price and accuracy.
        
        
    def get_pressure(self):
        order_book = BINANCE.fetch_order_book("BTC/USDT")
        
        up_pressure = 0
        for ask in order_book['asks']:
            up_pressure += ask[0] * ask [1]
            
        down_pressure = 0
        for bid in order_book['bids']:
            down_pressure += bid[0] * bid[1]
            
        return (up_pressure / (up_pressure + down_pressure), down_pressure / (up_pressure + down_pressure))
    
    def is_bull(self):
        ma5 = sum(i['Close'] for i in self._df.tail()) / 5
        return self._df['Open'].iloc[-1] > ma5
    
    
    