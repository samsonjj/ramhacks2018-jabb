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

import pymongo;
import dns;

import pprint;


app = Flask(__name__)
api = Api(app)
#mongodb+srv://<USERNAME>:<PASSWORD>@jabbcluster-sgjuz.mongodb.net/test?retryWrites=true
#client = pymongo.MongoClient("mongodb+srv://kay:myRealPassword@cluster0.mongodb.net/test");
client = pymongo.MongoClient("mongodb+srv://samsonjj:password123!@jabbcluster-sgjuz.mongodb.net/test?retryWrites=true");
db = client.sentiment;

tweetDetails = db.tweetDetails;

detail = {
    "author": "Jonathan Samson"
}

post_id = tweetDetails.insert_one(detail).inserted_id;

pprint.pprint(tweetDetails.find_one());



def hello(search_term):
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')


    consumer_key = '8lq8DnavidW7fMoVjY6TiW7sc'
    consumer_secret = 'rLuCHnjuwESC47fQlbWj8DXl8NEFTrDetatKSeaqUYc9VD4phM'
    access_token = '355312177-1FuYiscHJQ6ZXpuA2Dn9ETOreuqHwH0xIygAqAIu'
    access_token_secret = 'WoeVt1OfNvQrP5CM8Rbnvq3KaxLdsB5gqjSr2yYe2bu6J'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    public_tweets = api.search(search_term)

    print(len(public_tweets));

    someArray = [];


    for i in range(0, min(10, len(public_tweets))):
        #print("text: " + tweet.text)
        #analysis = TextBlob(tweet.text)
        #print("analysis: " + str(analysis))
        #rint("sentiment: " + str(analysis.sentiment))

        someArray.append((json.dumps(comprehend.detect_sentiment(Text=public_tweets[i].text, LanguageCode='en'), sort_keys=True, indent=4), public_tweets[i].text));

    return someArray;


class Thing(Resource):
    def get(self, search_term):
        result = {
            'data': hello(search_term)
        }
        return jsonify(result)


api.add_resource(Thing, '/sentiment/<search_term>')  # Route_1

if __name__ == '__main__':
    app.run(port='5002')

