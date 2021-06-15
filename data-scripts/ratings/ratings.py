# file: ratings.py
# author: Daniel Hogan

# This python script establishes a connection with the database and deletes all
# the contents of the upgrades_sentiment and downgrades_sentiment tables. It
# then uses selenium to navigate to the benzinga pages for analyst upgrades and
# downgrades. It gets all data from the table for the current day and feeds it
# into the get_sentiment function which finds each ticker, creates a Sentiment
# object for the ticker and invokes all methods. The data returned by the methods
# is inserted and commited into the database.
# *****************************************************************************

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import psycopg2
import datetime as dt
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
cursor.execute('delete from upgrades_sentiment')
cursor.execute('delete from downgrades_sentiment')


def get_sentiment(ratings, table_name):
    
    # this function takes in a list of strings and a string. It loops through
    # the list of strings and uses a regular expression to search for a date.
    # When it finds one, it takes the next element in the list as the ticker.
    # It creates a Sentiment object with the ticker and invokes all methods. It
    # then inserts and commits this data to the database
    
    for i in range(len(ratings)):
        if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', ratings[i]):
            ticker = ratings[i+1]
            print(ticker)
            
            s = Sentiment(ticker)
            news = s.get_news()
            stocktwits = s.get_stocktwits()
            press_releases = s.get_press_releases()
            analyst_ratings = s.get_analyst_ratings()
            insider_trading = s.get_insider_trading()
            quiver_data = s.get_quiver_data()
            
            cursor.execute(f'insert into {table_name} (ticker, articles, sentiment, \
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
        
            conn.commit()


# UPGRADES
# *****************************************************************************
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.benzinga.com/analyst-ratings/upgrades')
upgrades = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="analyst-calendar"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')

get_sentiment(upgrades, 'upgrades_sentiment')


# DOWNGRADES
# *****************************************************************************
browser.get('https://www.benzinga.com/analyst-ratings/downgrades')
downgrades = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="analyst-calendar"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')

get_sentiment(downgrades, 'downgrades_sentiment')

    
browser.quit()
      
cursor.close()
conn.close()
            
            
            
            
