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
cursor.execute('delete from morning_earnings')

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
                (date, earnings[i+3],
                 float(earnings[i+6][1:]),
                 float(earnings[i+7][1:]),
                 float(earnings[i+8][:-1])*100))
        





# for i in range(0, len(earnings), 11):
#     print(earnings[i])
    
#     # right here I need to use a regular expression to check for a date. This
#     # will be used to determine the start of a new record. Copy the form I used
#     # in earnings_sentiment.
    
#     if earnings[i+2] == 'AM' and earnings[i+6] != '-' and earnings[i+7] != '-':
#         print(earnings[i+3])
        
#         date = dt.datetime.today().strftime('%Y-%m-%d')
        
#         cursor.execute('insert into morning_earnings (date, ticker, estimate, actual, surprise) \
#                         values (%s, %s, %s, %s, %s)',
#                         (date, earnings[i+3],
#                          float(earnings[i+6][1:]),
#                          float(earnings[i+7][1:]),
#                          float(earnings[i+8][:-1])*100))


conn.commit()

cursor.close()
conn.close()