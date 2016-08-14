from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()

# Query in Elasticsearch
print("-----Query in Elasticsearch-----")
print("-----Places in China-----")
response = client.search(
    index="woeid",
    body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"country": "China"}},
                    {"match": {"_type": "woeid-with-mongo-id"}}
                ]
            }
        }
    }
)

for hit in response["hits"]["hits"]:
    print(hit["_source"]["province_state"],
          hit["_source"]["district_county"],
          hit["_source"]["city"])

print("-----Places in China but outside Sichuan province-----")
response = client.search(
    index="woeid",
    doc_type="woeid-with-simple-id",
    body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"country": "China"}},
                    # {"match": {"country": "Argentina"}},
                ],
                "must_not": {"match": {"province_state": "Sichuan"}}
            }
        }
    }
)

for hit in response["hits"]["hits"]:
    print(hit["_source"]["province_state"],
          hit["_source"]["district_county"],
          hit["_source"]["city"])

print("-----Places in United States, descending order by woeid and province_state-----")
response = client.search(
    index="woeid",
    doc_type="woeid-with-mongo-id",
    body={
        "query": {
            "bool": {
                "must": [
                    {"match": {"country": "United States"}},
                ]
            }
        },
        "sort": [
            {"woeid": {"order": "desc"}},
            {"province_state": {"order": "asc"}}
        ]
    }
)

for hit in response["hits"]["hits"]:
    print(hit["_source"]["woeid"],
          hit["_source"]["province_state"],
          hit["_source"]["city"])

print("----- -----")



# Query in Elasticsesarch_dsl
print("-----Query in Elasticsearch-----")
print("-----Places in China-----")

s = Search(using=client, index="woeid") \
    .query("match", country="China") \
    .query("match", _type="woeid-with-mongo-id")

response = s.execute()

for hit in response:
    print(hit.city, hit.district_county, hit.province_state)


"""
print("-----Places in China but outside Sichuan province-----")

s = Search(using=client, index="woeid", doc_type="woeid-with-mongo-id") \
    .query("match", country="United States") \
    .sort({"woeid": {"order": "dec"}})

response = s.execute()

for hit in response:
    print(hit.district_county, hit.province_state, hit.country, hit.woeid)
"""