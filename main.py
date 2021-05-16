import Trader
import ccxt
import datetime
import time
import ccxt 

bitcoin = Trader('BTC/USDT', 'BTCUSDT.csv')

while True:
    try:
        now = datetime.datetime.now()
        start_time = datetime.datetime.utcnow().strftime('%Y-%m-%d 00:00:00')
        end_time = start_time + datetime.timedelta(days=1)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = bitcoin.get_target()
            current_price = bitcoin.get_price()
            if target_price < current_price:
                usdt = bitcoin.fetch_balance()['free']
                if usdt > 10:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        with open('error.txt', 'a') as f:
            f.write(e)
        time.sleep(1)