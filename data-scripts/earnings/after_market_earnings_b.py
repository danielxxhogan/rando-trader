from selenium import webdriver
import psycopg2

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
    if earnings[i+2] == 'PM' and earnings[i+6] != '-' and earnings[i+7] != '-':
        print(earnings[i+3])


        # here ill add the values to the db if theyve reported earnings and have
        # an estimate.



conn.commit()

cursor.close()
conn.close()