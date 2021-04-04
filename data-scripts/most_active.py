import requests
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
# cursor.execute('delete from most_active')

data = pd.read_html('https://www.marketwatch.com/tools/screener/premarket?mod=side_nav')
most_active = data[2]

for ticker in most_active.values:
    
    cursor.execute('insert into most_active (ticker, company, price, change, volume) \
                    values (%s, %s, %s, %s, %s)',
                    (gainer[0].split()[0], gainer[1], gainer[2], gainer[5], gainer[3]))






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