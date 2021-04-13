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
browser.get('https://www.benzinga.com/analyst-ratings/upgrades')
upgrades = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="analyst-calendar"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')
browser.quit()

row_string = ''
for line in upgrades:
    
    if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', line):
        if len(row_string.split()) > 1:
            ticker = row_string.split()[1]
            print(ticker)
            
        row_string = line    
    else:
        row_string += (f' {line}')


browser = webdriver.Chrome()
browser.get('https://www.benzinga.com/analyst-ratings/downgrades')
downgrades = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="analyst-calendar"]/div/div[2]/div/div/div[2]/div[2]/div[3]/div[2]/div/div'))).text.split('\n')
browser.quit()

row_string = ''
for line in downgrades:
    
    if re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', line):
        if len(row_string.split()) > 1:
            ticker = row_string.split()[1]
            print(ticker)
            
        row_string = line    
    else:
        row_string += (f' {line}')
        
    
        
        
        