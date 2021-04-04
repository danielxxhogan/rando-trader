import pandas as pd
import datetime as dt
import psycopg2

from config import *

now = dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('delete from after_market_earnings')

# GET ALL EARNINGS UP TO NOW
# *****************************************************************************
earnings = pd.read_html('https://www.marketwatch.com/tools/earningscalendar?mod=side_nav')

WEEKEND_DAYS = 2
START_INDEX = 5 + WEEKEND_DAYS

day_of_week = dt.datetime.today().weekday()
today_index = START_INDEX + day_of_week

today = earnings[today_index]
today.dropna(inplace=True)
today = today[today['Surprise'] != 'Met']

surprises = today['Surprise']
actuals = []
pcts = []

for i in range(len(surprises)):
    actuals.append(float(surprises.values[i].split()[0]))
    pcts.append(float(surprises.values[i].split()[1][1:-2]))
    
today['Actual Surprise'] = actuals
today['Surprise Pct'] = pcts

today = today[[column for column in today.columns if column != 'Surprise']]


# GET EARNINGS FROM THIS MORNING
# *****************************************************************************
cursor.execute('select * from morning_earnings')
morning_earnings = cursor.fetchall()

morning_tickers = []

for earning in morning_earnings:
    morning_tickers.append(earning[1])
    
    
# FILTER OUT ALL THE VALUES THAT WERE ALREADY RECORDED IN THE MORNING
# *****************************************************************************
after_market = []

for row in today.values:
    if row[1] in morning_tickers:
        continue
    after_market.append(row)
    
after_market = pd.DataFrame(after_market)
after_market.to_csv(f'after_market_earnings-{now}.csv')

for row in after_market.values:
    cursor.execute('insert into after_market_earnings (company, symbol, quarter, estimate, actual, actual_surprise, surprise_pct) \
                    values (%s, %s, %s, %s, %s, %s, %s)',
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))


conn.commit()

cursor.close()
conn.close()