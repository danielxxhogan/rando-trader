# file: premarket_sentiment.py
# author: Daniel Hogan

# This python script establishes a connection to the database and deletes all
# the contents of the premarket_sentiment table. It then queries the database
# for all the tickers in the premarket_gainers, premarket_losers, and most_active
# tables. It feeds each one into the sentiment.py function which returns a dictionary
# of data about that ticker. The dictionary data is inserted and commited into
# the database.
# *****************************************************************************

import psycopg2
import sentiment

from config import *

conn = psycopg2.connect(user=PG_USER,
                  password=PG_PASSWORD,
                  host=PG_HOST,
                  port=PG_PORT,
                  dbname=PG_DATABASE,
                  )

cursor = conn.cursor()
cursor.execute('delete from premarket_sentiment')

tickers = []

cursor.execute('select * from premarket_gainers')
gainers = cursor.fetchall()
for gainer in gainers:
    tickers.append(gainer[0])

cursor.execute('select * from premarket_losers')
losers = cursor.fetchall()
for loser in losers:
    tickers.append(loser[0])
    
cursor.execute('select * from most_active')
premarket_active = cursor.fetchall()
for active in premarket_active:
    tickers.append(active[0])
    
temp = []
temp2 = []
for ticker in tickers:
    if ticker not in temp:
        temp2.append(ticker)
    temp.append(ticker)

tickers = temp2

for ticker in tickers:
    print(ticker)
    ticker_sentiment = sentiment.calculate_sentiment(f'{ticker}')
    print(ticker_sentiment)
    
    cursor.execute('insert into premarket_sentiment (ticker, articles, sentiment, \
        today_sentiment, messages, today_sentiment_st, sentiment_st, \
        press_releases, contracts, lobbying, congress_buys, \
        congress_sells, senate_buys, senate_sells, house_buys, \
        house_sells, insider_trades, upgrades, downgrades) \
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                %s, %s, %s, %s, %s, %s, %s)',
        (ticker, ticker_sentiment['articles'], ticker_sentiment['sentiment'],
        ticker_sentiment['today_sentiment'], ticker_sentiment['messages'],
        ticker_sentiment['today_sentiment_st'], ticker_sentiment['sentiment_st'],
        ticker_sentiment['press_releases'], ticker_sentiment['contracts'],
        ticker_sentiment['lobbying'], ticker_sentiment['congress_buys'],
        ticker_sentiment['congress_sales'], ticker_sentiment['senate_buys'],
        ticker_sentiment['senate_sales'], ticker_sentiment['house_buys'],
        ticker_sentiment['house_sales'], ticker_sentiment['insider_trades'],
        ticker_sentiment['upgrades'], ticker_sentiment['downgrades']))
    
    conn.commit()


cursor.close()
conn.close()