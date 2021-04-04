import pandas as pd
import psycopg2
import datetime as dt

from config import *

one_week_ago = (dt.datetime.today() - dt.timedelta(days=4))

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('delete from insider_trading')

insider_trading = pd.read_html('http://openinsider.com/insider-purchases-25k')[11]
rm_columns = ['X', 'Trade Type', '1d', '1w', '1m', '6m'] 
insider_trading = insider_trading[[column for column in insider_trading.columns if column not in rm_columns]]

for row in insider_trading.values:
    cursor.execute('insert into insider_trading (filing_date, trade_date, ticker, company, insider, title, price, qty, owned, change, value) \
                   values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   (row[0][:10], row[1], row[2], row[3], row[4], row[5],
                    float(row[7][1:].replace(',', '')),
                    float(row[8].replace(',', '')),
                    row[9], row[10],
                    float(row[11].replace(',', '').replace('$', ''))
                    ))


conn.commit()

cursor.close()
conn.close()