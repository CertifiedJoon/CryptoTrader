import Strategy as strg
class Trader:
    with open("credential/api.txt") as f:
        lines = f.readlines()
        api_key = lines[0].strip() 
        secret = lines[1].strip() 
    
    BINANCE = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret
    })
    
    AVAILABLE_TICKER = set('BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT', 'DOGE/USDT')
    
    __slots__ = '_ticker', '_history', '_df', '_strategy'
    def __init__(self, ticker = None, history_file = None):
        """
        Initiates Trader,
        Instanciates _strategy using parameterized factory method
        """
        if ticker not in AVAILABLE_TICKER:
            raise RuntimeError(f"{ticker} is not available.\n")
        self._ticker = _ticker
        # Should Add file location check 
        self._history_file = history_file
        self._df = pd.read_csv(history_file).set_index('Date')

            
    def update_ohlcv(self):
        info = self.BINANCE.fetch_ticker(self._ticker)
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        new_row = [today, info['open'], info['high'], info['low'], info['close'], info['quoteVolume']]
        
        with open(self._filename,'a') as fd:
            writer_object = csv.writer(fd)
            writer_object.writerow(new_row)
            fd.close()
        
        self._df.loc[today] = pd.Series(new_row)
    
    def get_ask_price(self):
        """Return the current lowest ask price of _ticker"""
        return Trader.BINANCE.fetch_ticker(self._ticket)['ask']

    def get_bid_price(self):
        """Return the current highest bid price of _ticker"""
        return Trader.BINANCE.fetch_ticker(self._ticket)['bid']
        
    def get_balance(self):
        """Return balance in client's wallet"""
        balance = self.BINANCE.fetch_balance()
        return balance