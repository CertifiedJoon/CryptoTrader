import Strategy as strg

class CompositeRatingStrategy(strg.Strategy):
    MINIMUM_RATING = 0.75
    def __init__(self):
        # Add midnight caching of rating!
        self._strategies = []
        self._rating = 0
    
    def add_strategy(self):
        raise NotImplementedError("Oops not implemented yet")
    
    def get_rating(self):
        """
        this is pseudo code
        """
        # raise NotImplementedError("OOPS not implemented yet")
        # pressure = self.get_pressure()     
        # rating = 0.9 if self.is_bull() else 0
        # rating += pressure[0] - pressure[1]
        # rating += self.get_daily_price_direction()
        # rating += 0.2 if self.get_sentiment() > 0.4 else 0     
        # return rating
    
    def best_crypto(self):
        """
        This is pseudocode
        """
        
        raise NotImplementedError("Ooops not implemented yet")
        
        # markets = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT', 'DOGE/USDT']

        # for i in range(len(markets)):
        #     j = markets[i].find('/')
        #     markets[i] = markets[i][:j] + markets[i][j+1:]
        #     markets[i] = Trader(markets[i], "log/{}.csv".format(markets[i]))

        # max_rating = 0

        # def rating(market):
        #     return market.get_rating()

        # coin_to_trade = max(markets, key=rating)

        # return coin_to_trade.get_ticker()
    
    def approve_buy(self, price = None, time = None):
        """Approve buy if composite rating is satisfactory"""
        return self.get_rating() > CompositeRatingStrategy.MINIMUM_RATING
    
    def approve_sell(self, bought_at, price = None, time = None):
        return self.get_rating() > 0.75 or bought_at * self._stop_loss > price or bought_at * self._take_profit < price