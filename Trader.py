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
#"BTC/USDT"

class Trader():
    BINANCE = ccxt.binance()
    
    def __init__(self, ticker, file):
        self._ticker = ticker
        self._filename = file
        df = pd.read_csv(file)
        self._df = df.set_index('Date')
        
    def get_df():
        return self._df

    def get_price(): #market is a class from ccxt
        price = BINANCE.fetch_ticker(ticker)
        return price['ask']

    def get_target():
        yesterday = self._df.iloc[-2]
        today_open = yesterday['close']
        yesterday_high = yesterday['high']
        yesterday_low = yesterday['low']
        k = self.get_bestk()
        target = today_open + (yesterday_high - yesterday_low) * k
        return target

    def get_bestk():
        max_ror = 0
        best_k = 0.5
        for k in np.arange(0.1, 1.0, 0.05):
            ror = _get_ror(k)
            if ror > maxi:
                maxi = ror
                best_k = k
        return best_k

    def _get_ror(k):
        self._df['range'] = (self._df['high'] - self._df['low']) * k
        self._df['target'] = self._df['open'] + self._df['range'].shift(1)

        fee = 0.0032
        self._df['ror'] = np.where(self._df['high'] > self._df['target'],
                             self._df['close'] / self._df['target'] - fee,
                             1)

        ror = self._df['ror'].cumprod()[-2]
        return ror

    def update_ohlcv():
        info = BINANCE.fetch_ticker(self._ticker)
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        new_row = [today, info['open'], info['high'], info['low'], info['close'], info['volume']]
        
        with open(self._filename,'a') as fd:
            writer_object = writer(fd)
            wrtier_object.writerow(new_row)
            fd.close()
        
        self._df.loc[today] = Series(new_row)

    def get_prediction(): #get prediction price for next day, return predicted price and accuracy.
        df['HL_PCT'] = df['HL_PCT'] = (df['High'] - df['Low'])/df['Close'] * 100.0
        df['PCT_change'] = (df['Close'] - df['Open'])/df['Open'] * 100.0
        df.fillna(-99999, inplace=True)
        forecast_col = 'High'
        forecast_out = 30
        df['label'] = df[forecast_col].shift(-forecast_out)
        df.dropna(inplace=True)
        X = df.drop(['label'], axis = 1).to_numpy()
        y = df['label'].to_numpy()

        X = preprocessing.scale(X)


        prediction_size = 100

        X_train = X[:-prediction_size]
        y_train = y[:-prediction_size]

        X_test = X[-prediction_size:]
        y_test = y[-prediction_size:]

        regr = svm.SVR(kernel = 'rbf')
        regr.fit(X_train, y_train)

        #forecasting the future with a proven regression method after regr.score()
        forecast_set = regr.predict(X_test)
        df['Forecast'] = np.nan

        #linked list like thinking,,, get last date --> find next date using unix and timestamp
        last_date = df.iloc[-1].name
        last_unix = last_date.timestamp()
        one_day = 86400
        next_unix = last_unix + float(one_day)
        #looping thru the forecaseset of length predictionsize and adding that with index(next_date) and other columns being np.nan
        for i in forecast_set:
            next_date = datetime.datetime.fromtimestamp(next_unix)
            next_unix += float(one_day)
            df.append(pd.DataFrame(index =[next_date]))
            df.at[next_date, 'Forecast'] = i
