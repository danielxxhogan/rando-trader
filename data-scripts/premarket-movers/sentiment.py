import requests
from bs4 import BeautifulSoup
import psycopg2
import pandas as pd
import datetime as dt

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
# cursor.execute('delete from gainers_sentiment')
# cursor.execute('delete from losers_sentiment')


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
        price = tds[2].text.replace('\n', '').replace(' ', '')
        change = tds[3].text.replace('\n', '').replace(' ', '')
        volume = tds[4].text.replace('\n', '').replace(' ', '')
        
        r = requests.get(f'https://api.polygon.io/v1/meta/symbols/{ticker}/news?apiKey={POLYGON_API_KEY}')
        articles = r.json()
        
        current_articles = []
        
        for article in articles:
            if article['timestamp'][:10] == dt.datetime.today().strftime('%Y-%m-%d'):
                current_articles.append(article)
                
            # here I will loop through all the articles and make a request to the
            # google language api. I will get a consolidated sentiment score for
            # the ticker.
                
        for article in current_articles:
            
            # here I will loop through all todays articles and make a request to
            # google language api using the python client. I will need to copy
            # my credentials.json file. I will need to set the env variable, and
            # I will have to add the command to export the env variable in the
            # cronjob.
            
            pass
        
        r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json')
        messages = r.json()['messages']
        
        current_messages = []
        
        for message in messages:
            if message['created_at'][:10] == dt.datetime.today().strftime('%Y-%m-%d'):
                current_messages.append(article)
            
            # here I will make a request to the google language api for each message
            # from the stocktwits api and get an aggregate sentiment score
            
        for message in current_messages:
            
            # here I will loop through all the messages from today and get a
            # sentiment score for the day
            
            pass
        
        # here I will scrape stocktwits api to get its sentiment score and the
        # change in mentions
        
        
        
        cursor.execute('insert into gainers_sentiment (ticker, price, change, \
                        volume, articles_today, sentiment_today, sentiment, \
                        messages_today, st_sentiment_today, messages_sentiment, \
                        st_sentiment, mentions) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                        (ticker, company, price, change, volume, len(current_articles),
                         sentiment_today, sentiment, len(messages_today),
                         st_sentiment_today, messages_sentiment, st_sentiment, mentions))











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


# BENZINGA PREMARKET MOVERS USING READ_HTML
# *****************************************************************************
# tickers = []

# premarket = pd.read_html('https://www.benzinga.com/premarket/')

# gainers = premarket[5]
# losers = premarket[6]

# for stock in gainers['Stock']:
#     tickers.append(stock)
    
# for stock in losers['Stock']:
#     tickers.append(stock)
    

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