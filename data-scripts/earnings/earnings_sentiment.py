# file: earnings_sentiment.py
# author: Daniel Hogan

# This python script establishes a connection to the database and deletes all
# the contents of the earnings_sentiment table. It then uses Selenium to open
# a browser and navigates to https://www.benzinga.com/news/earnings. It gets all
# data that has a value of 'PM' in the Time column and passes each ticker into the
# sentiment function imported from the local sentiment.py file. The sentiment
# function takes in a ticker and returns a dictionary of data about the ticker.
#  All this data is inserted and commited to the database.
# *****************************************************************************

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import psycopg2
import re
from sentiment import Sentiment

from config import *

conn = psycopg2.connect(user=PG_USER,
                  password=PG_PASSWORD,
                  host=PG_HOST,
                  port=PG_PORT,
                  dbname=PG_DATABASE,
                  )

cursor = conn.cursor()
cursor.execute('delete from earnings_sentiment')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.benzinga.com/news/earnings')
earnings = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="earnings-calendar"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')
browser.quit()

for i in range(len(earnings)):
    if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', earnings[i]) and earnings[i+1] == 'PM':
        
        ticker = earnings[i+2]
        print(ticker)
        
        s = Sentiment(ticker)
        news = s.get_news()
        print(news)
        stocktwits = s.get_stocktwits()
        print(stocktwits)
        press_releases = s.get_press_releases()
        print(press_releases)
        analyst_ratings = s.get_analyst_ratings()
        print(analyst_ratings)
        insider_trading = s.get_insider_trading()
        print(insider_trading)
        quiver_data = s.get_quiver_data()
        print(quiver_data)
        # break
        
        # ticker_sentiment = sentiment.calculate_sentiment(f'{ticker}')
        # print(ticker_sentiment)
        
        cursor.execute('insert into earnings_sentiment (ticker, articles, sentiment, \
            today_sentiment, messages, today_sentiment_st, sentiment_st, \
            press_releases, contracts, lobbying, congress_buys, \
            congress_sells, senate_buys, senate_sells, house_buys, \
            house_sells, insider_trades, upgrades, downgrades) \
            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, \
                    %s, %s, %s, %s, %s, %s, %s)',
            (ticker, news['articles_today'], news['total_sentiment'],
             news['today_total_sentiment'], stocktwits['articles_today'],
             stocktwits['today_total_sentiment'], stocktwits['total_sentiment'],
             press_releases, quiver_data['contracts'], quiver_data['lobbying'],
             quiver_data['congress_buys'], quiver_data['congress_sales'],
             quiver_data['senate_buys'], quiver_data['senate_sales'],
             quiver_data['house_buys'], quiver_data['house_sales'],
             insider_trading, analyst_ratings['upgrades'], analyst_ratings['downgrades']))
    
    
            # (ticker, ticker_sentiment['articles'], ticker_sentiment['sentiment'],
            # ticker_sentiment['today_sentiment'], ticker_sentiment['messages'],
            # ticker_sentiment['today_sentiment_st'], ticker_sentiment['sentiment_st'],
            # ticker_sentiment['press_releases'], ticker_sentiment['contracts'],
            # ticker_sentiment['lobbying'], ticker_sentiment['congress_buys'],
            # ticker_sentiment['congress_sales'], ticker_sentiment['senate_buys'],
            # ticker_sentiment['senate_sales'], ticker_sentiment['house_buys'],
            # ticker_sentiment['house_sales'], ticker_sentiment['insider_trades'],
            # ticker_sentiment['upgrades'], ticker_sentiment['downgrades']))
        
        conn.commit()


cursor.close()
conn.close()