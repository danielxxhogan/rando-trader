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
cursor.execute('delete from upgrades_sentiment')
cursor.execute('delete from downgrades_sentiment')


# UPGRADES
# *****************************************************************************
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.benzinga.com/analyst-ratings/upgrades')
upgrades = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="analyst-calendar"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')

row_string = ''
for line in upgrades:
    
    if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', line):
        if len(row_string.split()) > 1:
            ticker = row_string.split()[1]
            print(ticker)
            
            ticker_sentiment = sentiment.calculate_sentiment(f'{ticker}')
            print(ticker_sentiment)
            
            cursor.execute('insert into upgrades_sentiment (ticker, articles, sentiment, \
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
            
        row_string = line
        
    else:
        row_string += (f' {line}')


# DOWNGRADES
# *****************************************************************************
browser.get('https://www.benzinga.com/analyst-ratings/downgrades')
downgrades = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="analyst-calendar"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')

row_string = ''

for line in downgrades:
    if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', line):
        if len(row_string.split()) > 1:
            ticker = row_string.split()[1]
            print(ticker)
            
            ticker_sentiment = sentiment.calculate_sentiment(f'{ticker}')
            print(ticker_sentiment)
            
            cursor.execute('insert into downgrades_sentiment (ticker, articles, sentiment, \
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
            
        row_string = line
        
    else:
        row_string += f' {line}'
        
    
browser.quit()
      
cursor.close()
conn.close()