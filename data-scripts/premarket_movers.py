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
cursor.execute('delete from premarket_gainers')
cursor.execute('delete from premarket_losers')

# BENZINGA PREMARKET MOVERS
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



# tickers = []


# # ----- PREMARKET MOVERS -----
# premarket = pd.read_html('https://www.benzinga.com/premarket/')

# gainers = premarket[5]
# losers = premarket[6]

# for stock in gainers['Stock']:
#     tickers.append(stock)
    
# for stock in losers['Stock']:
#     tickers.append(stock)
    
    
    
    

# MARKETWATCH PREMARKET MOVERS
# *****************************************************************************



conn.commit()

cursor.close()
conn.close()


