import alpaca_trade_api as tradeapi
import logging

from config import *

logging.basicConfig(filename='exit.log', filemode='w', level=logging.ERROR)

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')

orders = api.list_orders(status='open')
for order in orders:
    api.cancel_order(order.id)

api.close_all_positions()
print("all positions closed")
logging.error('all positions closed')