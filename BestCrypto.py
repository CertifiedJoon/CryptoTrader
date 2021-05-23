from Trader import Trader
import ccxt

markets = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT', 'DOGE/USDT']

for i in range(len(markets)):
    j = markets[i].find('/')
    markets[i] = markets[i][:j] + markets[i][j+1:]
    markets[i] = Trader(markets[i], "log/{}.csv".format(markets[i]))

max_rating = 0

def rating(market):
    return market.get_rating()

coin_to_trade = max(markets, key=rating)

print(coin_to_trade.get_ticker())