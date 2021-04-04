import requests
from bs4 import BeautifulSoup
import psycopg2

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

r = requests.get(url='https://finviz.com/insidertrading.ashx?tc=1')

src = r.content
soup = BeautifulSoup(src, 'lxml')








# import requests
# from bs4 import BeautifulSoup

# r = requests.get(url='https://www.benzinga.com/premarket/')

# src = r.content
# soup = BeautifulSoup(src, 'lxml')

# tables = soup.find_all('table')
# gainers = tables[5]
# losers = tables[6]

# gainer_rows = gainers.find_all('tr')

# for row in gainer_rows:
#     tds = row.find_all('td')
#     if len(tds) > 0:
        
#         ticker = tds[0].text.replace('\n', '').replace(' ', '')
#         company = tds[1].text.replace('\n', '').replace(' ', '')
#         price = tds[2].text.replace('\n', '').replace(' ', '')
#         change = tds[3].text.replace('\n', '').replace(' ', '')
#         volume = tds[4].text.replace('\n', '').replace(' ', '')
        
#         print(f'ticker: {ticker}')
#         print(f'company: {company}')
#         print(f'price: {price}')
#         print(f'volume: {volume}')







# from selenium import webdriver

# chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-gpu")
# browser = webdriver.Chrome(options=chrome_options)

# try:
#     browser.get("https://www.google.com")
#     print("Page title was '{}'".format(browser.title))

# finally:
#     browser.quit()




# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Chrome()
# driver.get("http://www.python.org")

# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()