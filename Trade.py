import sys
import time
import datetime
import math
import csv
from datetime import timedelta

sys.path.append("C:\\Users\\mjypa\\OneDrive\\Documents\\Codebase\\CryptoTrader\\Notifier\\")
sys.path.append("C:\\Users\\mjypa\\OneDrive\\Documents\\Codebase\\CryptoTrader\\Strategy\\")
sys.path.append("C:\\Users\\mjypa\\OneDrive\\Documents\\Codebase\\CryptoTrader\\Trader\\")
sys.path.append("C:\\Users\\mjypa\\OneDrive\\Documents\\Codebase\\CryptoTrader\\log\\")
sys.path.append("C:\\Users\\mjypa\\OneDrive\\Documents\\Codebase\\CryptoTrader\\credentials\\")

import Notifier as notifier
import Trader as trader
import BullMarketStrategy as bull
import VolatilityBreakoutStrategy as vbs
import PriceDirectionStrategy as prd
import PricePressureStrategy as prp
import CompositeRatingStrategy as comp

class Trade:
    def __init__(self, ticker, history_file, stoploss, takeprofit):
        self._trader = trader.Trader(ticker, history_file)
        self._notifier = notifier.Notifier()
        self._start = None
        self._bought_price = None
        self._strategy = None
        # Parameterized factory for strategy subclasses
        self.change_strategy()
            
    
    def store_trade(self, now, rating):
        """Store each transaction made"""
        raise NotImplementedError("Sorry not implemented yet!")
    
    def change_strategy(self):
        """Dynamically change trading strategy"""
        if self._strategy == None:
            # Set Strategy
            ()
        else:
            # Recaliberate Stragety
            ()
        raise NotImplementedError("Sorry not implemented yet!")
    
    def trade(self):
        """Trading Algorithm"""
        # while True:
        #     try:
        #         current_price = self._trader.get_ask_price()
        #         now = datetime.datetime.now()
        #         self._start = datetime.datetime.now()
        #         self._start -= datetime.timedelta(hours = self._start.hour, minutes = self._start.minute, seconds = self._start.second, microseconds = self._start.microsecond)
        #         end_time = self._start + datetime.timedelta(days=1)

        #         if self._strategy.approve_buy():
        #             self._bought_price = current_price
        #             bought = True
        #             self._notifier.post_message("BTC buy : " + str(self._bought_price))

                
        #         current_price = self._trader.get_bid_price()
        #         if self._strategy.approve_sell(): 
        #             self.store_trade(now, 1)
        #             self._notifier.post_message("BTC sell : " + str(current_price))
        #             bought = False
        #             pause.until(end_time - datetime.timedelta(seconds=10))

        #             self._trader.update_ohlcv()
        #             time.sleep(5)

        #         time.sleep(1)

        #     except Exception as e:
        #         with open('log/error.txt', 'a') as f:
        #             f.write(str(e))
        #         time.sleep(1)