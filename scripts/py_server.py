#8lq8DnavidW7fMoVjY6TiW7sc (API key)
#rLuCHnjuwESC47fQlbWj8DXl8NEFTrDetatKSeaqUYc9VD4phM (API secret key)
#355312177-1FuYiscHJQ6ZXpuA2Dn9ETOreuqHwH0xIygAqAIu (Access token)
#WoeVt1OfNvQrP5CM8Rbnvq3KaxLdsB5gqjSr2yYe2bu6J (Access token secret)

from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import tweepy
from textblob import TextBlob

import boto3
import json

import pymongo
import dns

import pprint

from bson import json_util, ObjectId

app = Flask(__name__)
api = Api(app)
client = pymongo.MongoClient("mongodb+srv://samsonjj:password123!@jabbcluster-sgjuz.mongodb.net/test?retryWrites=true");
db = client.sentiment

tweetDetails = db.tweetDetails

def hello(search_term):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


    consumer_key = '8lq8DnavidW7fMoVjY6TiW7sc'
    consumer_secret = 'rLuCHnjuwESC47fQlbWj8DXl8NEFTrDetatKSeaqUYc9VD4phM'
    access_token = '355312177-1FuYiscHJQ6ZXpuA2Dn9ETOreuqHwH0xIygAqAIu'
    access_token_secret = 'WoeVt1OfNvQrP5CM8Rbnvq3KaxLdsB5gqjSr2yYe2bu6J'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    #public_tweets = api.search(search_term, rpp=100, geocode=("37.5400,77.53000,1000km"))
    public_tweets = api.search(search_term)

    print(len(public_tweets))

    someArray = []



    for i in range(0, min(100, len(public_tweets))):
        #print("text: " + tweet.text)
        #analysis = TextBlob(tweet.text)
        #print("analysis: " + str(analysis))
        #rint("sentiment: " + str(analysis.sentiment))+

        pprint.pprint(public_tweets[i]);
        sentiment = json.loads(json.dumps(comprehend.detect_sentiment(Text=public_tweets[i].text, LanguageCode='en'), sort_keys=True, indent=4))

        pprint.pprint(sentiment.keys())

        object = {
            'sentiment_data': {
                'positive': sentiment['SentimentScore']['Positive'],
                'neutral': sentiment['SentimentScore']['Neutral'],
                'negative': sentiment['SentimentScore']['Negative'],
                'mixed': sentiment['SentimentScore']['Mixed'],
                'sentiment': sentiment['Sentiment']
            },
            'tid': public_tweets[i].id,
            'text': public_tweets[i].text
        }

        tweetExists = tweetDetails.find_one({'tid': object['tid']})

        if tweetExists == None:
            print("this one was none")
            tweetDetails.insert_one(object)

        someArray.append(object);

    return someArray


class Get(Resource):
    def get(self, search_term):
        result = {
            'data': hello(search_term)
        }
        return json.loads(json_util.dumps(result))

class Store(Resource):
    def get(self, search_term):
        result = {
            'data': hello(search_term)
        }
        return jsonify(result)


api.add_resource(Get, '/sentiment/<search_term>')  # Route_1
api.add_resource(Store, '/sentiment/store/<search_term>')

if __name__ == '__main__':
    app.run(port='5002')

