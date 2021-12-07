import Strategy as strg

class PriceDirection(strg.Strategy):
    def __init(self, stoploss, take_profit, df):
        super.__init__(stoploss, take_profit)
        self._df = df 
    
    def get_daily_price_direction(self):
        yesterday = self._df.iloc[-2]
        yesterday_high = yesterday['High']
        yesterday_low = yesterday['Low']
        yesterday_open = yesterday['Open']
        yesterday_close = yesterday['Close']
        
        op = (yesterday_open - yesterday_low) - (yesterday_high - yesterday_open)
        cl = (yesterday_close - yesterday_low) - (yesterday_high - yesterday_close)
        
        return (cl - op) / abs(yesterday_high - yesterday_low)

    def approve_buy(self, price = None, time = None):
        """Approve buy if yesterday's price direction was upward by margin"""
        return self.get_daily_price_direction() > 0.3

    def approve_sell(self, bought_at, price = None, time = None):
        """Approve sell if it is midnight"""
        if isistance(price, datetime.datetime()):
            time = price
        
        start = time - datetime.timedelta(hours = time.hours,
                                         minutes = time.minutes,
                                         seconds = time.seconds)
        return start + datetime.timedelta(days = 1) - datetime.timedelta(seconds = 10) < time < start + datetime.timedelta(days = 1)        