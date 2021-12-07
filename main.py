import Trade as trd
client = trd.Trade("BTC/USDT", "log/BTCUSDT.csv", "VolatilityBreakOut", 0.7, 1.3)
client.trade()