class Strategy:
    __slots__ = '_stop_loss', '_max_profit'
    def __init__(self, stop_loss, take_profit):
        """
        Parent class for strategy subclasses
        Stores stoploss % and take_profit%
        """
        self._stop_loss = stop_loss
        self._take_profit = take_profit
    
    def approve_buy(self, price = None, time = None):
        """Grant approval to buy at certain conditions"""
        None
    
    def approve_sell(self, bought_at = None, price = None, time = None):
        """Grand approval to sell at certain conditions"""
        None
    
    def _take_progit_price(self, bought_at):
        """Given price bought, return target price"""
        return bought_at * self._take_profit
    
    def _stoploss_price(self, bought_at):
        """Given price bought, return stoploss price"""
        return bought_at *  self._stop_loss