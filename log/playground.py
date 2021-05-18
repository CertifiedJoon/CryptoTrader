#Description: This program gets the sentiment of Bitcoin from Twitter
import tweepy
from textblob import TextBlob
import pandas as pd
import numpy as np
import re

CONSUMER_KEY= 'thtCNwOql2tuWs6EvSAUUTBXg'
CONSUMER_KEY_SECRET = 'WNxdctkNdkpIyVQQGTY82CZBRZZNaBoviZwO9n5fEEP6GiUdG6'

ACCESS_TOKEN = '1394225479775756289-cFGjGk0sE7DxtjWrsmKujlApPmzjqM'
ACCESS_TOKEN_SECRET = 'Q3U2AK2b5vVsthJX2edm2ugQJrPa5wERS9L7n3G6Cy6zo'

print("authenticating tweetpy")
#create authentication object
authenticate = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_KEY_SECRET)

print("set access")
#Set the access tokens
authenticate.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
#Create the API object
print("creating api")
api = tweepy.API(authenticate, wait_on_rate_limit=True)

print("gathering tweets")
#Gather 2000 tweets about Bitcoin and filer out any retweets 'RT'
search_term = '#bitcoin -filter:retweets'

print("searching cursor")
#Create a cursor object
tweets = tweepy.Cursor(api.search, q=search_term, lang='en', since='2021-05-10', tweet_mode='extended').items(2000)
#Store the tweets in a variable and get the full text
all_tweets = [tweet.full_text for tweet in tweets]

print("creating dataframe")
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


print("clearning tweets")
#Clean tweets gathered
df['CleanTweets'] = df['Tweets'].apply(cleanTwt)
#Create a function to get the subjectivity
def get_subjectivity(twt):
  return TextBlob(twt).sentiment.subjectivity

#Create a function to get the polarity
def get_polarity(twt):
  return TextBlob(twt).sentiment.polarity

print("get subjectivity")
#Create two new columns called 'subjectivity' and 'polarity'
df['Subjectivity'] = df['CleanTweets'].apply(get_subjectivity) 
df['Polarity'] = df['CleanTweets'].apply(get_polarity)

print(pd.mean(df['Polarity']))