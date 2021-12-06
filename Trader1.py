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
    def __init__(self, ticker = None, history_file = None ,strategyID = None):
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
        self._strategy = None
        if strategyID == "VolatilityBreakout":
            
    def get_ask_price(self):
        """Return the current lowest ask price of _ticker"""
        return Trader.BINANCE.fetch_ticker(self._ticket)['ask']

    def get_bid_price(self):
        """Return the current highest bid price of _ticker"""
        return Trader.BINANCE.fetch_ticker(self._ticket)['bid']
    
    def change_strategy(self, strategyID):
        """Dynamically change trading strategy"""
        raise NotImplementedError("Sorry not implemented yet!")
        
    def get_balance(self):
        """Return balance in client's wallet"""
        balance = self.BINANCE.fetch_balance()
        return balance