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

browser = webdriver.Chrome()
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