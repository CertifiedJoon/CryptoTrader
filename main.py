from Trader import Trader
import ccxt
import datetime
import time
import ccxt 
import pprint
bitcoin = Trader('BTC/USDT', 'BTCUSDT.csv')
pprint.pprint(bitcoin.get_balance())
while True:
    try:
        print(bitcoin.get_price())
        now = datetime.datetime.now()
        start_time = datetime.datetime.now()
        start_time -= datetime.timedelta(hours = start_time.hour, minutes = start_time.minute, seconds = start_time.second, microseconds = start_time.microsecond)
        end_time = start_time + datetime.timedelta(days=1)
        target_price = bitcoin.get_target()
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            print('target {}'.format(target_price))
            current_price = bitcoin.get_price()
            if target_price < current_price:
                usdt = bitcoin.get_balance()
                if usdt['free'] > 10:
                    print('bought')
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                print('sold')
        time.sleep(1)
    except Exception as e:
        with open('error.txt', 'a') as f:
            f.write(str(e))
        time.sleep(1)