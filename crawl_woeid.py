import os
import re
import urllib2
from bs4 import BeautifulSoup
import pymongo

# set root url
rooturl = 'http://woeid.rosselliot.co.nz/lookup/'

# set connection to mongodb
MONGODB_SERVER = "1-PC"  # does "localhost" work?
MONGODB_PORT = 27017
MONGODB_DB = "test"
MONGODB_COLLECTION_WOEID = "newwoeid"

print("-----CONNECTINGTO MONGODB-----")
connection = pymongo.MongoClient(
    MONGODB_SERVER,
    MONGODB_PORT
)
db = connection[MONGODB_DB]
collection = db[MONGODB_COLLECTION_WOEID]

# import country names
countries = open('countriesoftheworld.txt', 'r')
_ = countries.readline()  # get rid of column name
for country in countries:
    country = re.sub('[^\w|\s|\\-]|\\n', '', country)  # obay the input form
    uri = country
    print(uri)

    # set url
    url = rooturl + uri

    # send request and get response from website
    print("-----SENDING REQUEST-----")
    try:
        response=urllib2.urlopen(url)
    except urllib2.URLError,e:
        continue

    html = response.read()

    # get woeid and other info from html doc
    soup = BeautifulSoup(html, 'html.parser')
    infoList = []  # save possible more-than-one woeid for the same origin name
    # example, China the country and China a small town in US
    for line in soup.find_all('tr')[1:]:
        info = {"city": line['data-city'],
                "district_county": line['data-district_county'],
                "province_state": line['data-province_state'],
                "country": line['data-country'],
                "woeid": line['data-woeid']}
        infoList.append(info)

    # check data in pymongo and then insert new data
    for info in infoList:
        # check if info with the woeid exists
        if not collection.find_one({"woeid": info['woeid']}):
            # insert
            collection.insert(info)
            print("info added to MongoDB database!")


os.system('pause')
