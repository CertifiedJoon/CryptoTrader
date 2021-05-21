from Trader import Trader
import ccxt
import datetime
import time
import pause
import csv
import Phone
import pprint

bitcoin = Trader('BTC/USDT', 'log/BTCUSDT.csv')

current_price = bitcoin.get_price()
now = datetime.datetime.now()
start_time = datetime.datetime.now()
start_time -= datetime.timedelta(hours = start_time.hour, minutes = start_time.minute, seconds = start_time.second, microseconds = start_time.microsecond)
end_time = start_time + datetime.timedelta(days=1)
target_price = bitcoin.get_target()
rating = 0.75

info = bitcoin.BINANCE.fetch_ticker(bitcoin._ticker)
pprint.pprint(info)
print(start_time)
new_row = [start_time, info['open'], info['high'], info['low'], info['close'], info['quoteVolume'], target_price, rating, bitcoin.get_price()]
print(new_row)
with open('trades_made.csv','a') as fd:
    writer_object = csv.writer(fd)
    writer_object.writerow(new_row)
    fd.close()
Phone.post_message("BTC sell : " +str(new_row[-1]))
pause.until(end_time - datetime.timedelta(seconds=10))