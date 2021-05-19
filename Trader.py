import ccxt
import numpy as np
import pandas as pd
import time
import datetime
import math
from datetime import timedelta

class Trader:
    with open("log/api.txt") as f:
        lines = f.readlines()
        api_key = lines[0].strip() 
        secret = lines[1].strip() 
    
    BINANCE = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret
    })
    
    def __init__(self, ticker, file):
        self._ticker = ticker
        self._filename = file
        df = pd.read_csv(file)
        self._df = df.set_index('Date')
        
    def get_df(self):
        return self._df

    def get_price(self): #market is a class from ccxt
        price = self.BINANCE.fetch_ticker(self._ticker)
        return price['ask']

    def get_target(self):
        yesterday = self._df.iloc[-2]
        today_open = yesterday['Close']
        yesterday_high = yesterday['High']
        yesterday_low = yesterday['Low']
        k = self.get_bestk()
        target = today_open + (yesterday_high - yesterday_low) * k
        return target

    def get_bestk(self):
        max_ror = 0
        best_k = 0.5
        for k in np.arange(0.1, 1.0, 0.05):
            ror = self._get_ror(k)
            if ror > max_ror:
                max_ror = ror
                best_k = k
        return best_k

    def _get_ror(self, k):
        self._df['Range'] = (self._df['High'] - self._df['Low']) * k
        self._df['Target'] = self._df['Open'] + self._df['Range'].shift(1)

        fee = 0.0032
        self._df['ror'] = np.where(self._df['High'] > self._df['Target'],
                             self._df['Close'] / self._df['Target'] - fee,
                             1)

        ror = self._df['ror'].cumprod()[-2]
        return ror

    def update_ohlcv(self):
        info = self.BINANCE.fetch_ticker(self._ticker)
        today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        new_row = [today, info['open'], info['high'], info['low'], info['close'], info['volume']]
        
        with open(self._filename,'a') as fd:
            writer_object = writer(fd)
            wrtier_object.writerow(new_row)
            fd.close()
        
        self._df.loc[today] = pd.Series(new_row)
    
    def get_pressure(self):
        order_book = self.BINANCE.fetch_order_book("BTC/USDT")
        
        up_pressure = 0
        for ask in order_book['asks']:
            up_pressure += ask[0] * ask [1]
            
        down_pressure = 0
        for bid in order_book['bids']:
            down_pressure += bid[0] * bid[1]
            
        return (up_pressure / (up_pressure + down_pressure), down_pressure / (up_pressure + down_pressure))
    
    def is_bull(self):
        self._df['ma5'] = self._df['Close'].rolling(window=5).mean().shift(1)
        return self._df['Open'].iloc[-1] > self._df['ma5'].iloc[-1]
    
    def get_daily_price_direction(self):
        yesterday = self._df.iloc[-2]
        yesterday_high = yesterday['High']
        yesterday_low = yesterday['Low']
        yesterday_open = yesterday['Open']
        yesterday_close = yesterday['Close']
        
        op = (yesterday_open - yesterday_low) - (yesterday_high - yesterday_open)
        cl = (yesterday_close - yesterday_low) - (yesterday_high - yesterday_close)
        
        return (cl - op) / abs(yesterday_high - yesterday_low)
    
    def get_balance(self):
        balance = self.BINANCE.fetch_balance()
        return balance
    
    def get_sentiment(self):
        #Description: This program gets the sentiment of Bitcoin from Twitter
        import tweepy
        from textblob import TextBlob
        import re

        CONSUMER_KEY= 'thtCNwOql2tuWs6EvSAUUTBXg'
        CONSUMER_KEY_SECRET = 'WNxdctkNdkpIyVQQGTY82CZBRZZNaBoviZwO9n5fEEP6GiUdG6'

        ACCESS_TOKEN = '1394225479775756289-cFGjGk0sE7DxtjWrsmKujlApPmzjqM'
        ACCESS_TOKEN_SECRET = 'Q3U2AK2b5vVsthJX2edm2ugQJrPa5wERS9L7n3G6Cy6zo'

        #create authentication object
        authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)

        #Set the access tokens
        authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        
        #Create the API object
        api = tweepy.API(authenticate, wait_on_rate_limit=True)

        #Gather 2000 tweets about Bitcoin and filer out any retweets 'RT'
        search_term = '#bitcoin -filter:retweets'

        #Create a cursor object
        tweets = tweepy.Cursor(api.search, q=search_term, lang='en', since='2021-05-10', tweet_mode='extended').items(2000)
        #Store the tweets in a variable and get the full text
        all_tweets = [tweet.full_text for tweet in tweets]

        #Create a dataframe to store the tweets with a column called 'Tweets'
        df = pd.DataFrame(all_tweets, columns=['Tweets'])

        #Create a function to clean the tweets
        def cleanTwt(twt):
          twt = re.sub('#bitcoin', 'bitcoin', twt) #removes the hashtag from #bitcoin
          twt = re.sub('#Bitcoin', 'Bitcoin', twt) #removes the hashtag from #Bitcoin
          twt = re.sub('#[A-Za-z0-9]+', '', twt) #removes anything with hashtag
          twt = re.sub('@[A-Za-z0-9]+', '', twt)
          twt = re.sub('\\n','',twt) #removes newlines
          twt = re.sub('https?:\/\/\S+', '', twt) #removes any hyperlinks
          return twt

        #Clean tweets gathered
        df['CleanTweets'] = df['Tweets'].apply(cleanTwt)
        #Create a function to get the subjectivity
        def get_subjectivity(twt):
          return TextBlob(twt).sentiment.subjectivity

        #Create a function to get the polarity
        def get_polarity(twt):
          return TextBlob(twt).sentiment.polarity

        #Create two new columns called 'subjectivity' and 'polarity'
        df['Subjectivity'] = df['CleanTweets'].apply(get_subjectivity) 
        df['Polarity'] = df['CleanTweets'].apply(get_polarity)

        return df['Polarity'].mean()
    
    def get_rating(self):
        pressure = self.get_pressure()
        
        rating = 0.9 if self.is_bull() else 0
        rating += pressure[0] - pressure[1]
        rating += self.get_daily_price_direction()
        rating += 0.2 if self.get_sentiment() > 0.4 else 0     
        
        return rating