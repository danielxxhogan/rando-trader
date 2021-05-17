# file: ma.py
# author: Daniel Hogan

# This python script establishes a connection with the database and deletes all
# the contents of the ma_sentiment table. It then uses selenium to navagiate to
# the benzinga page for recent mergers and acqusitions. It gets all the tickers
# for companies with announcements today and feeds each one into the sentiment
# method which returns a dictionary of data about each ticker. The dictionary
# data is inserted and commited into the database.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import psycopg2
import datetime as dt
import re
import sentiment

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )
cursor = conn.cursor()
cursor.execute('delete from ma_sentiment')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.benzinga.com/m-a')
ma = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ma-calendar"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')
browser.quit()

for line in ma:
    if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', line):
        date = f'{line[6:10]}-{line[0:2]}-{line[3:5]}'
        
        if date == dt.datetime.today().strftime('%Y-%m-%d'):
            today = True
        else:
            today = False
    
    ticker = re.search(r'\(([A-Za-z0-9_]+)\)', line)
    if ticker and today == True:
        ticker = line[ticker.start()+1:ticker.end()-1]
        print(ticker)
        
        ticker_sentiment = sentiment.calculate_sentiment(f'{ticker}')
        print(ticker_sentiment)
        
        cursor.execute('insert into ma_sentiment (ticker, articles, sentiment, \
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