import ccxt
import numpy as np
import pandas as pd
import time
import datetime
import math
from datetime import timedelta
import numpy as np
from sklearn import preprocessing, svm
from sklearn.svm import SVR


class Trader:
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
        price = self.BINANCE.fetch_ticker(self._ticker)
        return price['ask']

    def get_target(self):
        yesterday = self._df.iloc[-2]
        today_open = yesterday['Close']
        yesterday_high = yesterday['High']
        yesterday_low = yesterday['Low']
        k = self.get_bestk()
        target = today_open + (yesterday_high - yesterday_low) * k
        return target

    def get_bestk(self):
        max_ror = 0
        best_k = 0.5
        for k in np.arange(0.1, 1.0, 0.05):
            ror = self._get_ror(k)
            if ror > max_ror:
                max_ror = ror
                best_k = k
        return best_k

    def _get_ror(self, k):
        self._df['Range'] = (self._df['High'] - self._df['Low']) * k
        self._df['Target'] = self._df['Open'] + self._df['Range'].shift(1)

        fee = 0.0032
        self._df['ror'] = np.where(self._df['High'] > self._df['Target'],
                             self._df['Close'] / self._df['Target'] - fee,
                             1)

        ror = self._df['ror'].cumprod()[-2]
        return ror

    def update_ohlcv(self):
        info = self.BINANCE.fetch_ticker(self._ticker)
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        new_row = [today, info['open'], info['high'], info['low'], info['close'], info['volume']]
        
        with open(self._filename,'a') as fd:
            writer_object = writer(fd)
            wrtier_object.writerow(new_row)
            fd.close()
        
        self._df.loc[today] = pd.Series(new_row)
        
    def get_sentiment(self): #get prediction price for next day, return predicted price and accuracy.
        pass
    
    def get_pressure(self):
        order_book = self.BINANCE.fetch_order_book("BTC/USDT")
        
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
    
    def get_balance(self):
        balance = self.BINANCE.fetch_balance()
        return balance
    
    