import pymongo
from elasticsearch import Elasticsearch

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

# set instance of Elasticsearch
print("-----ELASTICSEARCH INSTANCE-----")
es = Elasticsearch()

# export data from mongodb
""" # for all data
data = collection.find()
for record in data:
    print(record)
"""

# # test
record = collection.find_one()
print(record)
print(type(record))

# possible data manipulation
print(type(record["_id"]))
print(str(record["_id"]))
del record["_id"]  # delete id in MongoDB

# insert data into elasticsearch
#doc = record
#res = es.index(index="woeid", doc_type='woeid-test', id=1, body=doc)  # index (insert)
#print('data inserted to elasticsearch')
