import Strategy as strg

class SentimentStrategy(strg.Strategy):
    TICKER_KEYWORD_MAPPING = {'BTC/USDT': 'Bitcoin', 'ETH/USDT': 'Ethereum', 'BNB/USDT': 'Binance', 'ADA/USDT':'ADA', 'XRP/USDT': 'Ripple', 'DOGE/USDT': 'Doge'}
    def __init__(self, ticker):
        # Add midnight Optimization
        self._ticker = ticker
    
    def get_sentiment(self):
        #Description: This program gets the sentiment of Bitcoin from Twitter
        import tweepy
        from textblob import TextBlob
        import re
        
        with open("credential/api.txt") as f:
            lines = f.readlines()
            CONSUMER_KEY= lines[0].strip()
            CONSUMER_KEY_SECRET = lines[1].strip()
            ACCESS_TOKEN = lines[2].strip()
            ACCESS_TOKEN_SECRET = lines[3].strip()

        #create authentication object
        authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)

        #Set the access tokens
        authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        
        #Create the API object
        api = tweepy.API(authenticate, wait_on_rate_limit=True)

        #Gather 2000 tweets about Bitcoin and filer out any retweets 'RT'
        search_term = f"#{SentimentStrategy.TICKER_KEYWORD_MAPPING[self._ticker]} -filter:retweets"

        #Create a cursor object
        tweets = tweepy.Cursor(api.search, q=search_term, lang='en', since='2021-05-10', tweet_mode='extended').items(500)
        #Store the tweets in a variable and get the full text
        all_tweets = [tweet.full_text for tweet in tweets]

        #Create a dataframe to store the tweets with a column called 'Tweets'
        df = pd.DataFrame(all_tweets, columns=['Tweets'])

        #Create a function to clean the tweets
        def cleanTwt(twt):
            twt = re.sub('#' + SentimentStrategy.TICKER_KEYWORD_MAPPING[self._ticker], SentimentStrategy.TICKER_KEYWORD_MAPPING[self._ticker], twt) #removes the hashtag from #bitcoin
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
    
    def approve_buy(self, price = None, time = None):
        return self.get_sentiment() > 0.4
    
    def approve_sell(self, bought_at, price = None, time = None):
        return self.get_sentiment() < 0.4 or bought_at * self._stop_loss > price or bought_at * self._take_profit < price