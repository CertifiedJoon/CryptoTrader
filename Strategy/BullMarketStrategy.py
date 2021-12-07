import Strategy as strg

class BullMarketStrategy(strg.Strategy):
    def __init__(self, df):
        self._df = df
        
    def is_bullish()(self):
        self._df['ma5'] = self._df['Close'].rolling(window=5).mean().shift(1)
        return self._df['Open'].iloc[-1] > self._df['ma5'].iloc[-1]

    def approve_buy(self, price = None, time = None):
        """Approve sell if market is bullish"""
        return self.is_bullish()
    
    def approve_sell(self, bought_at, price = None, time = None):
        """Approve sell if market is no longer bullish or at stoploss or at profit taking level"""
        return not self.is_bullish or bought_at * self._stop_loss > price or bought_at * self._take_profit < price