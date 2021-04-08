import requests
from bs4 import BeautifulSoup
import psycopg2
import pandas as pd

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('delete from premarket_gainers')
cursor.execute('delete from premarket_losers')


# BENZINGA PREMARKET MOVERS USING BS4
# *****************************************************************************
r = requests.get(url='https://www.benzinga.com/premarket/')

src = r.content
soup = BeautifulSoup(src, 'lxml')

tables = soup.find_all('table')
gainers = tables[5]
losers = tables[6]

gainer_rows = gainers.find_all('tr')

for row in gainer_rows:
    tds = row.find_all('td')
    
    if len(tds) > 0:
        ticker = tds[0].text.replace('\n', '').replace(' ', '')
        company = tds[1].text.replace('\n', '').replace(' ', '')
        price = tds[2].text.replace('\n', '').replace(' ', '')
        change = tds[3].text.replace('\n', '').replace(' ', '')
        volume = tds[4].text.replace('\n', '').replace(' ', '')
        
        cursor.execute('insert into premarket_gainers (ticker, company, price, change, volume) \
                        values (%s, %s, %s, %s, %s)',
                        (ticker, company, price, change, volume))

loser_rows = losers.find_all('tr')

for row in loser_rows:
    tds = row.find_all('td')
    
    if len(tds) > 0:
        ticker = tds[0].text.replace('\n', '').replace(' ', '')
        company = tds[1].text.replace('\n', '').replace(' ', '')
        price = tds[2].text.replace('\n', '').replace(' ', '')
        change = tds[3].text.replace('\n', '').replace(' ', '')
        volume = tds[4].text.replace('\n', '').replace(' ', '')
        
        cursor.execute('insert into premarket_losers (ticker, company, price, change, volume) \
                        values (%s, %s, %s, %s, %s)',
                        (ticker, company, price, change, volume))


conn.commit()
    

# MARKETWATCH PREMARKET MOVERS
# *****************************************************************************
# data = pd.read_html('https://www.marketwatch.com/tools/screener/premarket?mod=side_nav')
# gainers = data[0]
# losers = data[1]

# for gainer in gainers.values:
    
#     cursor.execute('insert into premarket_gainers (ticker, company, price, change, volume) \
#                     values (%s, %s, %s, %s, %s)',
#                     (gainer[0].split()[0], gainer[1], gainer[2], gainer[5], gainer[3]))
        
# for loser in losers.values:
    
#     cursor.execute('insert into premarket_losers (ticker, company, price, change, volume) \
#                     values (%s, %s, %s, %s, %s)',
#                     (loser[0].split()[0], loser[1], loser[2], loser[5], loser[3]))


# *****************************************************************************
conn.commit()

cursor.close()
conn.close()