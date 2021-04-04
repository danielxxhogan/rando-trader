import requests
import pandas as pd
import datetime as dt

from config import *


# This script will execute toward the end of the trading day. It will get all
# companies reporting earnings after market from the db.
# It will query polygon api for news about the stock.
# It will look at the number of articles written that day,
# get a sentiment score for the day if possible,
# get the overall sentiment score
# Then it will query the stocktwits api and get the number of mentions that day,
# get sentiment score for the day if possible,
# get overall sentiment score
# Then it will scrape stocktwits to get the sentiment from stocktwits
# and the change in mentions
# it will store all this data for each stock reporting earnings after market each day.


# GET ALL STOCKS REPORTING AFTER MARKET


# GET NEWS FOR EACH STOCK, CALCULATE CURRENT ARTICLES, CURRENT SENTIMENT, AND OVERALL SENTIMENT


# GET STOCKTWITS DATA, CALCULATE CURRENT MENTIONS, CURRENT SENTIMENT, AND OVERALL SENTIMENT


# GET STOCKTWITS SENTIMENT AND CHANGE IN MENTIONS





# GET NEWS FOR A GIVEN STOCK AND STORE IN DF
# *****************************************************************************
r = requests.get(f'https://api.polygon.io/v1/meta/symbols/AAPL/news?apiKey={POLYGON_API_KEY}')
r = r.json()

symbol = []
timestamp = []
title = []
url = []
source = []
summary = []
image = []

for row in r:
    symbol.append(row['symbols'][0])
    timestamp.append(row['timestamp'][:10])
    title.append(row['title'])
    url.append(row['url'])
    source.append(row['source'])
    summary.append(row['summary'])
    image.append(row['image'])
    
df = pd.DataFrame()
df['symbol'] = symbol
df['timestamp'] = timestamp
df['title'] = title
df['url'] = url
df['source'] = source
df['summary'] = summary
df['image'] = image

two_days_ago = dt.datetime.today() - dt.timedelta(days=2)





















