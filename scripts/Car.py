#8lq8DnavidW7fMoVjY6TiW7sc (API key)
#rLuCHnjuwESC47fQlbWj8DXl8NEFTrDetatKSeaqUYc9VD4phM (API secret key)
#355312177-1FuYiscHJQ6ZXpuA2Dn9ETOreuqHwH0xIygAqAIu (Access token)
#WoeVt1OfNvQrP5CM8Rbnvq3KaxLdsB5gqjSr2yYe2bu6J (Access token secret)

import tweepy
from textblob import TextBlob

import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


consumer_key = '8lq8DnavidW7fMoVjY6TiW7sc'
consumer_secret = 'rLuCHnjuwESC47fQlbWj8DXl8NEFTrDetatKSeaqUYc9VD4phM'
access_token = '355312177-1FuYiscHJQ6ZXpuA2Dn9ETOreuqHwH0xIygAqAIu'
access_token_secret = 'WoeVt1OfNvQrP5CM8Rbnvq3KaxLdsB5gqjSr2yYe2bu6J'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

public_tweets = api.search('Nike')

print(len(public_tweets));

for i in range(0, min(10, len(public_tweets))):
    #print("text: " + tweet.text)
    #analysis = TextBlob(tweet.text)
    #print("analysis: " + str(analysis))
    #rint("sentiment: " + str(analysis.sentiment))

    print(json.dumps(comprehend.detect_sentiment(Text=public_tweets[i].text, LanguageCode='en'), sort_keys=True, indent=4));

