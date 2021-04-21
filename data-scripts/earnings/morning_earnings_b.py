from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import psycopg2
import datetime as dt

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
browser.get('https://www.benzinga.com/news/earnings')
earnings = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="earnings-calendar"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')
browser.quit()

for i in range(0, len(earnings), 11):
    if earnings[i+2] == 'AM' and earnings[i+6] != '-' and earnings[i+7] != '-':
        print(earnings[i+3])
        
        date = dt.datetime.today().strftime('%Y-%m-%d')
        
        cursor.execute('insert into morning_earnings (date, ticker, estimate, actual, surprise) \
                        values (%s, %s, %s, %s, %s)',
                        (date, earnings[i+3],
                         float(earnings[i+6][1:]),
                         float(earnings[i+7][1:]),
                         float(earnings[i+8][:-1])*100))


conn.commit()

cursor.close()
conn.close()