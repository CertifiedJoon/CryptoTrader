#Add sys path

class Trade:
    def __init__(self, ticker, history_file, strategyID, stoploss, takeprofit):
        self._trader = Trader(ticker, history_file)
        self._notifier = Notifier()
        self._start = None
        self._bought_price = None
        self._strategy = None
        # Parameterized factory for strategy subclasses
        if strategyID == "VolatilityBreakout":
            self._strategy = vbs.VolatilityBreakoutStrategy(stoploss, takeprofit, self._trader.get_df())
        elif strategyID == "Bull":
            self._strategy = bull.BullMarketStrategy(stoploss, takeprofit, self._trader.get_df())
        elif strategyID == "PriceDirection":
            self._strategy = prd.PriceDirectionStrategy(stoploss, takeprofit, self._trader.get_df())
        elif strategyID == "PricePressure":
            self._strategy = prp.PricePressureStrategy(stoploss, takeprofit, self._trader.get_def(), ticker, Trader.BINANCE)
        else:
            self._strategy = comp.Composite(stoploss, takeprofit, self._trader.get_df())
            
    
    def store_trade(self, now, self._bought_price, rating):
        info = self.BINANCE.fetch_ticker(self._ticker)
        new_row = [now, self._bought_price, rating, self.get_price()]

        with open('log/trades_made.csv','a') as fd:
            writer_object = csv.writer(fd)
            writer_object.writerow(new_row)
            fd.close()
    
    def change_strategy(self, strategyID):
        """Dynamically change trading strategy"""
        raise NotImplementedError("Sorry not implemented yet!")
    
    def trade(self):
        while True:
            try:
                current_price = self._trader.get_ask_price()
                now = datetime.datetime.now()
                self._start = datetime.datetime.now()
                self._start -= datetime.timedelta(hours = self._start.hour, minutes = self._start.minute, seconds = self._start.second, microseconds = self._start.microsecond)
                end_time = self._start + datetime.timedelta(days=1)

                if self._strategy.approve_buy():
                    self._bought_price = current_price
                    bought = True
                    self._notifier.post_message("BTC buy : " + str(self._bought_price))

                
                current_price = self._trader.get_bid_price()
                elif self._strategy.approve_sell(): 
                    self.store_trade(now, self._bought_price, rating)
                    self._notifier.post_message("BTC sell : " + str(current_price))
                    bought = False
                    pause.until(end_time - datetime.timedelta(seconds=10))

                    self._trader.update_ohlcv()
                    time.sleep(5)

                time.sleep(1)

            except Exception as e:
                with open('log/error.txt', 'a') as f:
                    f.write(str(e))
                time.sleep(1)