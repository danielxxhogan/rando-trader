# file: most_active.py
# author: Daniel Hogan

# This python script establishes a connection to the database and deletes all
# the contents of the most_active table. It then uses pandas.read_html to get
# all the tables from https://www.marketwatch.com/tools/screener/premarket?mod=side_nav,
# finds the one with data about all the most active stocks premarket and inserts
# and commits the data to the database.
# *****************************************************************************

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
cursor.execute('delete from most_active')

data = pd.read_html('https://www.marketwatch.com/tools/screener/premarket?mod=side_nav')
most_active = data[2]

for ticker in most_active.values:
    
    cursor.execute('insert into most_active (ticker, company, price, change, volume) \
                    values (%s, %s, %s, %s, %s)',
                    (ticker[0].split()[0], ticker[1], ticker[2], ticker[5], ticker[3]))


# *****************************************************************************
conn.commit()

cursor.close()
conn.close()