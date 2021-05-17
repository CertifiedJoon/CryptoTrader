import ccxt
import pprint
import datetime

with open('api.txt') as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()
    
binance = ccxt.binance(config={
    'apiKey' : api_key,
    'secret' : secret
})

balance = binance.fetch_balance()
pprint.pprint(balance)

start_time = datetime.datetime.now()
start_time -= datetime.timedelta(hours = start_time.hour, minutes = start_time.minute, seconds = start_time.second, microseconds = start_time.microsecond)
end_time = start_time + datetime.timedelta(days=1)
now = datetime.datetime.utcnow()
print(start_time, now ,end_time)