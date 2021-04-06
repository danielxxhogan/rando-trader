import psycopg2
import alpaca_trade_api as tradeapi
import logging
import math

from config import *

logging.basicConfig(filename='premarket-movers.log', filemode='w', level=logging.ERROR)

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')

orders = api.list_orders(status='open')
for order in orders:
    api.cancel_order(order.id)
api.close_all_positions()
print("all positions closed")
logging.error('all positions closed')

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('select * from premarket_gainers')
gainers = cursor.fetchall()
cursor.execute('select * from premarket_losers')
losers = cursor.fetchall()

buying_power = 80000
max_trades = len(gainers) + len(losers)

# ****************************************************************************************************************
def calculate_qty(bars):
    close = bars[row[0]][-1].c
    amt_to_spend = buying_power / max_trades
    qty = math.floor(amt_to_spend / close)
    
    print(f'\nclose price 1 min in: {close}\nquantity: {qty}\n')
    logging.error(f'\nclose price 1 min in: {close}\nquantity: {qty}\n')
    
    return qty


for row in gainers:
    print(f'\n{row[0]} was a top gainer\n')
    logging.error(f'\n{row[0]} was a top gainer\n')
    
    try:
        bars = api.get_barset(symbols=row[0], timeframe='minute', limit=30)

        api.submit_order(symbol=row[0],
                      qty=calculate_qty(bars),
                      side='sell',
                      type='market',
                      time_in_force='gtc',
                      )
        
        print(f'\nNew short position initiated for {row[0]}\n***************************************\n')
        logging.error(f'\nNew short position initiated for {row[0]}\n***************************************\n')
        
    except:
        print(f'error encountered... skipping {row[0]}')
        logging.error(f'error encountered... skipping {row[0]}')
    
for row in losers:
    print(f'\n{row[0]} was a top loser')
    logging.error(f'\n{row[0]} was a top loser')
    
    try:
        bars = api.get_barset(symbols=row[0], timeframe='minute', limit=30)
        
        api.submit_order(symbol=row[0],
                      qty=calculate_qty(bars),
                      side='buy',
                      type='market',
                      time_in_force='gtc',
                      )
        
        print(f'\nNew long position initiated for {row[0]} \n***************************************\n')
        logging.error(f'\nNew long position initiated for {row[0]} \n***************************************\n')
        
    except:
        print(f'error encountered... skipping {row[0]}')
        logging.error(f'error encountered... skipping {row[0]}')
        
                    
                    
                    
                    
                    
                    
                    
                    