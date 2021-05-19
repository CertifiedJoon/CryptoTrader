from Trader import Trader
import ccxt
import datetime
import time
import ccxt 
import pause
import pprint

bitcoin = Trader('BTC/USDT', 'log/BTCUSDT.csv')
rating = bitcoin.get_rating()
bought = False
bought_at = 0
while True:
    try:
        print(bitcoin.get_price())
        now = datetime.datetime.now()
        start_time = datetime.datetime.now()
        start_time -= datetime.timedelta(hours = start_time.hour, minutes = start_time.minute, seconds = start_time.second, microseconds = start_time.microsecond)
        end_time = start_time + datetime.timedelta(days=1)
        target_price = bitcoin.get_target()
        
        x = 0.7
        
        if start_time < now < end_time - datetime.timedelta(seconds=10) and current_price < target_price * 1.1: # need some work on buying and selling condition
            if not bought and target_price < current_price and rating > x:
                bought_at = current_price
                bought = True

        else:
            bitcoin.update_ohlcv()
            info = self.BINANCE.fetch_ticker(self._ticker)
            today = datetime.datetime.utcnow()
            new_row = [today, info['open'], info['high'], info['low'], info['close'], info['volume'], current_price, rating, bitcoin.get_price()]

            with open('trades_made.csv','a') as fd:
                writer_object = writer(fd)
                wrtier_object.writerow(new_row)
                fd.close()
                
            bought = False
            rating = bitcoin.get_rating()
            pause.until(end_time)
            
        time.sleep(1)
        
    except Exception as e:
        with open('log/error.txt', 'a') as f:
            f.write(str(e))
        time.sleep(1)