from selenium import webdriver
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

browser = webdriver.Chrome()
browser.get('https://www.benzinga.com/news/earnings')
earnings = browser.find_element_by_class_name('ag-center-cols-container').text.split('\n')
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