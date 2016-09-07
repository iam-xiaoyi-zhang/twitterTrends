import os
import time
import tweepy
import pymongo
from api import *

# set connection to mongodb
MONGODB_SERVER = "1-PC"  # does "localhost" work?
MONGODB_PORT = 27017
MONGODB_DB = "test"
MONGODB_COLLECTION_TREND = "newtrend"
MONGODB_COLLECTION_WOEID = "newwoeid"

print("-----CONNECTION TO MONGODB-----")
connection = pymongo.MongoClient(
    MONGODB_SERVER,
    MONGODB_PORT
)
db = connection[MONGODB_DB]
collection = db[MONGODB_COLLECTION_TREND]
collection_woeid = db[MONGODB_COLLECTION_WOEID]

# connect to twitter api
print("-----CONNECTING TO TWITTER API-----")
auth = tweepy.OAuthHandler(twitter_consumer_key,
                           twitter_consumer_secret)
auth.set_access_token(twitter_access_token,
                      twitter_access_secret)
api = tweepy.API(auth)

"""
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
    # trendInfo = dict()
    # trendInfo['twitterTrends'] = response.pop('trends')
    # trendInfo['twitterTrendsInfo'] = response
    trendList.append(trendInfo)

# check data in pymongo and then insert new data
for trend in trendList:
    collection.insert(trend)
    print("info added to MongoDB database!")

"""
# extract all woeids from mongodb and then request trends for each one of them
woeids = collection_woeid.find()
for ea in woeids:
	#print ea['woeid'].encode('ascii'), type(ea['woeid'].encode('ascii'))
	#response = api.trends_place(ea['woeid'].encode('ascii'))[0]
	#print respone
	response = ''
	while response=='':
		print ea['country']
		try:
			response = api.trends_place(ea['woeid'].encode('ascii'))[0]
		except tweepy.error.RateLimitError:
			print("sleeping")
			time.sleep(60*15)
			break
		except tweepy.error.TweepError:
			print "Sorry, this page does not exists (" + ea['country'] + ")"
			break
		#so except TweepError will catch a RateLimitError too
	
		
	try:
		print response['created_at'], response['locations']
	except:
		print response
	"""
	# tweepy.error.RateLimitError
	# twitter api rate limit: 15mins periods.
	

# each trend has 5 keys:
# _id : index
# created_at : a time
# trends : 50 trends
# as_of : a time
# locations : location name and woeid

os.system("pause")


