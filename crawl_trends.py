import os
import tweepy
import pymongo
from .api import *

# connect to twitter api
print("-----CONNECTING TO TWITTER API-----")
auth = tweepy.OAuthHandler(twitter_consumer_key,
                           twitter_consumer_secret)
auth.set_access_token(twitter_access_token,
                      twitter_access_secret)
api = tweepy.API(auth)

# choose countries we are interested in
woeid1 = "23424977"  # United States
woeid2 = "23424768"  # Brazil

# get trends
print("-----GETTING TRENDS-----")
response1 = api.trends_place(woeid1)[0]
response2 = api.trends_place(woeid2)[0]
trendList = []
for response in [response1, response2]:
    trendInfo = response
    #trendInfo = dict()
    #trendInfo['twitterTrends'] = response.pop('trends')
    #trendInfo['twitterTrendsInfo'] = response
    trendList.append(trendInfo)

# check data in pymongo and then insert new data
MONGODB_SERVER = "1-PC" # does "localhost" work?
MONGODB_PORT = 27017
MONGODB_DB = "test"
MONGODB_COLLECTION_TREND = "newtrend"

print("-----CONNECTION TO MONGODB-----")
connection = pymongo.MongoClient(
    MONGODB_SERVER,
    MONGODB_PORT
)
db = connection[MONGODB_DB]
collection = db[MONGODB_COLLECTION_TREND]

for trend in trendList:
    collection.insert(trend)
    print("info added to MongoDB database!")

# each trend has 5 keys:
# _id : index
# created_at : a time
# trends : 50 trends
# as_of : a time
# locations : location name and woeid

os.system("pause")


