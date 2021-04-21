import pandas as pd
import psycopg2

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('delete from short_interest')

short_interest_df = pd.read_html('https://www.marketwatch.com/tools/screener/short-interest?mod=side_nav')[0]

for row in short_interest_df.values:
    print(row[0].split(' ')[0])
    
    ticker = row[0].split(' ')[0]
    company = row[1]
    price = float(row[2][1:])
    short_interest = row[5]
    float_ = row[7]
    float_shorted = float(row[8][:-1])
    
    cursor.execute('insert into short_interest (ticker, company, price, short_interest, float, float_shorted) \
                    values (%s, %s, %s, %s, %s, %s)',
                    (ticker, company, price, short_interest, float_, float_shorted))
    
    conn.commit()
    

cursor.close()
conn.close()
    
