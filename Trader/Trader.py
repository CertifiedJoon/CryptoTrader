# I used to have use Binance's API to trade crypto. But i am thinking of shifting to Stock Market API
# So i have commented out the binance code.
# This class takes care of fetching information needed in trading

import datetime
import Strategy as strg
import ccxt
import numpy as np
import pandas as pd

class Trader:
    # Bring in Credential File
    with open("credentials/api.txt") as f:
        lines = f.readlines()
        api_key = lines[0].strip() 
        secret = lines[1].strip() 
    # Save as a public variable
    
    __slots__ = '_ticker', '_history', '_df', '_strategy'
    def __init__(self, ticker = None, history_file = None):
        """
        Initiates Trader,
        Instanciates _strategy using parameterized factory method
        """
        if self.ticker_valid(ticker):
            raise RuntimeError(f"{ticker} is not available.\n")
        self._ticker = ticker
        # Should Add file location check 
        self._history_file = history_file
        self._df = pd.read_csv(history_file).set_index('Date')

    def ticker_valid(self, ticker):
        raise NotImplementedError("Sorry, not implemented yet!")
            
    def update_ohlcv(self):
        """Fetch Ticker from external API"""
        # info = self.BINANCE.fetch_ticker(self._ticker)
        raise NotImplementedError("Sorry, not implemented yet.")
        
        # today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        # new_row = [today, info['open'], info['high'], info['low'], info['close'], info['quoteVolume']]
        
        # with open(self._filename,'a') as fd:
        #     writer_object = csv.writer(fd)
        #     writer_object.writerow(new_row)
        #     fd.close()
        
        # self._df.loc[today] = pd.Series(new_row)
    
    def get_ask_price(self):
        """Return the current lowest ask price of _ticker"""
        raise NotImplementedError("Sorry, not implemented yet.")

    def get_bid_price(self):
        """Return the current highest bid price of _ticker"""
        raise NotImplementedError("Sorry, not implemented yet.")
        
    def get_balance(self):
        """Return balance in client's wallet"""
        raise NotImplementedError("Sorry, not implemented yet.")