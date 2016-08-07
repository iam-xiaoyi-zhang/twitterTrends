import os
import pymongo

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

enter1 = "United States"
enter2 = "Brazil"

# get trends we want from MongoDB
# Q: How to get United States in MongoDB Shell?
# A: db.newtrend.find({"locations.0.name":"United States"})
place1 = collection.find_one({"locations.0.name": enter1})
place2 = collection.find_one({"locations.0.name": enter2})

# data cleaning
trends1 = list()
trends2 = list()
for trend in place1["trends"]:
    trends1.append({"name": trend["name"], "volume": trend["tweet_volume"]})

for trend in place2["trends"]:
    trends2.append({"name": trend["name"], "volume": trend["tweet_volume"]})

#print(trends1)
#print(trends2)

# compare trends
# sorting
trends1name = [trend["name"] for trend in trends1]
trends1volume = [trend["volume"] for trend in trends1]
trends1zip = zip(trends1name, trends1volume)
trends1zip.sort(key=lambda x: x[1], reverse=True)

trends2name = [trend["name"] for trend in trends2]
trends2volume = [trend["volume"] for trend in trends2]
trends2zip = zip(trends2name, trends2volume)
trends2zip.sort(key=lambda x: x[1], reverse=True)

# get top 18 trends
trends1top = trends1zip[:18]
trends2top = trends2zip[:18]
trends1topname = [name for name, value in trends1top]
trends1topvalue = [value for name, value in trends1top]
trends2topname = [name for name, value in trends2top]
trends2topvalue = [value for name, value in trends2top]

print(trends1topname, trends1topvalue)
print(trends2topname, trends2topvalue)

# plotly barchart
# plotly.exceptions.PlotlyError: Plotly Offline mode has not been
# initialized in this notebook. Run:
# import plotly
# plotly.offline.init_notebook_mode()

import plotly as py
import plotly.graph_objs as go

py.offline.init_notebook_mode()

trace1 = go.Bar(
    x=trends1topname,
    y=trends1topvalue,
    name='United States'
)
trace2 = go.Bar(
    x=trends2topname,
    y=trends2topvalue,
    name='Brazil'
)

data = [trace1, trace2]
layout = go.Layout(
    barmode='group'
)

fig = go.Figure(data=data, layout=layout)
py.offline.plot(fig, filename='grouped-bar')


os.system("pause")
