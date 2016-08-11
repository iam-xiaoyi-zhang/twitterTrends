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
data = collection.find()
count = 1
for record in data:
    print("get data from mongodb"),
    print(record["country"]),
    print(count)
    count += 1

    # possible data manipulation
    id = record["_id"]
    del record["_id"]  # delete id in MongoDB

    # insert data into elasticsearch
    doc = record
    res = es.index(index="woeid", doc_type='woeid-with-auto-id', body=doc)  # index (insert) # POST
    """
    res = es.index(index="woeid", doc_type='woeid-with-simple-id', id=count, body=doc)  # index (insert) # PUT
    res = es.index(index="woeid", doc_type='woeid-with-mongo-id', id=str(id), body=doc)  # index (insert) # PUT
    """
    print('data inserted into elasticsearch')
