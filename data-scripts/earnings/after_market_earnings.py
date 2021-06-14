# file: after_market_earnings.py
# author: Daniel Hogan

# This python script establishes a connection to the database and deletes all
# the contents of the after_market_earnings table. It then uses Selenium to open
# a browser and navigates to https://www.benzinga.com/news/earnings. It gets all
# data that has a value of 'PM' in the Time column and has reported earnings with
# a surprise. All this data is inserted and commited to the database.
# *****************************************************************************

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import datetime as dt
import re

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('delete from after_market_earnings')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.benzinga.com/news/earnings')
earnings = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="earnings-calendar"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')
browser.quit()



for i in range(len(earnings)):
    if (re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', earnings[i]) and
        earnings[i+1] == 'PM' and
        earnings[i+6] != '-' and
        earnings[i+7] != '-'):
        
        ticker = earnings[i+2]
        print(ticker)
        date = dt.datetime.today().strftime('%Y-%m-%d')
        
        cursor.execute('insert into morning_earnings (date, ticker, estimate, actual, surprise) \
                values (%s, %s, %s, %s, %s)',
                (date, earnings[i+2],
                 float(earnings[i+5][1:]),
                 float(earnings[i+6][1:]),
                 float(earnings[i+7][:-1])*100))
            
            
conn.commit()

cursor.close()
conn.close()