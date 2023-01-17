# Variables that contain user credentials
CONSUMER_KEY= 'thtCNwOql2tuWs6EvSAUUTBXg'
CONSUMER_KEY_SECRET = 'WNxdctkNdkpIyVQQGTY82CZBRZZNaBoviZwO9n5fEEP6GiUdG6'

BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAD7uPgEAAAAAP8WpOnGwQ82%2BroasL5RPWYA4K%2FA%3DEZ6uuMnm1czaCI4GLb9uX028x6xJ6x2eDcdEdc2fB2qdh4LXeL'

ACCESS_TOKEN = '1394225479775756289-cFGjGk0sE7DxtjWrsmKujlApPmzjqM'
ACCESS_TOKEN_SECRET = 'Q3U2AK2b5vVsthJX2edm2ugQJrPa5wERS9L7n3G6Cy6zo'

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor

class TwitterClient():
    
    def __init__(self):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        
    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline).items(num_tweets):
            tweets.append(tweet)
        return tweets

class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        return auth

class TwitterStreamer():
    """
    Class for streaming and processing live tweets
    """
    
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
    
    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()        
        stream = Stream(auth, listener)
        stream.filter(track = hash_tag_list)


class TwitterListener(StreamListener):
    """
    Basic Listener class taht just prints received tweets to stdout
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
    
    def on_data(self, data): # take in the stream of tweets
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as f:
                f.write(data)
            return True
        except Exception as e:
            print("Error on_data: {}".format(str(e)))
        return True
    
    def on_error(self, status): # do smt when errored
        if status == 420:
            # returning false to terminate on_data method in case rate limit is encountered.
            return False
        print(status)
    
if __name__ == '__main__':
    """Hash Tag to be set dynamically"""
    hash_tags = ['Bitcoin', 'bitcoin', 'crypto', 'Crypto']
    tweets_file = 'tweets.json'
    twitter_client = TwitterClient()
    print(twitter_client.get_user_timeline_tweets(5))
#    twitter_streamer = TwitterStreamer()
#    twitter_streamer.stream_tweets(tweets_file, hash_tags)