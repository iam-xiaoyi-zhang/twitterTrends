import os
import urllib, urllib2
from bs4 import BeautifulSoup
import pymongo

rooturl = 'http://woeid.rosselliot.co.nz/lookup/'
url = rooturl + 'United States'

# send request and get response from website
print("-----SENDING REQUEST-----")
response = urllib2.urlopen(url)
html = response.read()

# get woeid and other info from html doc
soup = BeautifulSoup(html, 'html.parser')
infoList = []
for line in soup.find_all('tr')[1:]:
    info = {"city": line['data-city'],
            "district_county": line['data-district_county'],
            "province_state": line['data-province_state'],
            "country": line['data-country'],
            "woeid": line['data-woeid']}
    infoList.append(info)

# check data in pymongo and then insert new data
MONGODB_SERVER = "1-PC" # does "localhost" work?
MONGODB_PORT = 27017
MONGODB_DB = "test"
MONGODB_COLLECTION_WOEID = "newwoeid"

print("-----CONNECTION TO MONGODB-----")
connection = pymongo.MongoClient(
    MONGODB_SERVER,
    MONGODB_PORT
)
db = connection[MONGODB_DB]
collection = db[MONGODB_COLLECTION_WOEID]

for info in infoList:
    # check if info with the woeid exists
    if not collection.find_one({"woeid": info['woeid']}):
        # insert
        collection.insert(info)
        print("info added to MongoDB database!")

os.system('pause')
