import Strategy as strg

class PricePressureStrategy(strg.Strategy):
    def __init__(self, stoploss, takeprofit, ticker, df, binance):
        super.__init__(stoploss, takeprofit)
        self._df = df
        self._ticker = ticker
        self.BINANCE = binance

    def get_pressure(self):
        order_book = self.BINANCE.fetch_order_book("BTC/USDT")
        
        up_pressure = 0
        for ask in order_book['asks']:
            up_pressure += ask[0] * ask [1]
            
        down_pressure = 0
        for bid in order_book['bids']:
            down_pressure += bid[0] * bid[1]
            
        return (up_pressure / (up_pressure + down_pressure), down_pressure / (up_pressure + down_pressure))
        
    def approve_buy(self, price = None, time = None):
        """Approve buy if upward pressure is significantly higher than downward pressure"""
        up_pressure, down_pressure = self.get_pressure()
        return up_pressure > down_pressure + 0.3
    
    def approve_sell(self, price = None, time = None):
        """Approve sell if downward pressure is significantly higher than upward pressure"""
        up_pressure, down_pressure = self.get_pressure()
        return down_pressure > up_pressure > 0.2