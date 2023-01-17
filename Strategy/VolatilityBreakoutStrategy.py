import Strategy as strg

class VolatilityBreakoutStrategy(strg.Strategy):
    """
    VBS. Check Wikipedia for details of strategy
    """
    def __init__(self, stoploss, takeprofit, df):
        super.__init__(stoploss, takeprofit)
        self._buy_price = -1  # midnight caching
        self._df = df 
    
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
        
    def approve_buy(self, price = None, time = None):
        """
        Calls get_buy_price every midnight.
        if current price is higher than _buy_price, approve buy
        Midnight caching enabled
        """
        
        start = time - datetime.timedelta(hours = time.hours,
                                         minutes = time.minutes,
                                         seconds = time.seconds)
        if start + datetime.timedelta(days = 1) < time < start + datetime.timedelta(days=1, seconds = 10):
            self._buy_price = -1
        
        if self._buy_price == -1:
            self._buy_price = self.get_buy_price()
        
        return price > self._buy_price
            
    def approve_sell(self, boughtat, price = None, time = None):
        """Approve at stoploss or takeprofit level.
        Also Approve sell at midnight"""
        if start + datetime.timedelta(hours = 23, minutes = 59) < time < start + datetime.timedelta(days=1):
            return True
        elif price > boughtat * self._take_profit:
            return True
        elif price < boughtat * self._stop_loss:
            return True
        return False
    