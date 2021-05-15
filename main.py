import jumbo as cj
import ccxt
import datetime
import time

binance = ccxt.binance()
df = cj.get_df(binance, "BTC/USDT")

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

target_price = cj.get_target(df)

while True:
    now = datetime.datetime.now()
    if mid < now < mid + datetime.delta(seconds=10):
        target_price = cj.get_target(df)
        mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
        
    current_price = cj.get_price(binance, "BTC/USDT")
    print(current_price, target_price)
    
    time.sleep(1)