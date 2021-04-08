import psycopg2
import alpaca_trade_api as tradeapi
import logging
import math

from config import *

logging.basicConfig(filename='open-range.log', filemode='w', level=logging.ERROR)

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('select * from most_active')
most_active = cursor.fetchall()

tickers = []
side = {}

for row in most_active:
    tickers.append(row[0])
    
buying_power = 80000
max_trades = len(tickers)
    
take_profits = {}
    
stop_prices = {}
for ticker in tickers:
    stop_prices[ticker] = 0.0
    
positions_taken = []

# CALCULATE OPENING RANGES
# *****************************************************************************
opening_ranges = {}

for ticker in tickers:
    bars = api.get_barset(symbols=ticker, timeframe='15Min', limit=26)
    
    for bar in bars[ticker]:
        if bar.t.strftime('%H:%M') == '09:30':
            opening_ranges[ticker] = {'high': bar.h,
                                      'low': bar.l}
    

# *****************************************************************************
def get_position_details(positions, ticker):
    l_s = ''
    entry_price = 0.0
    
    if (len(positions)) > 0:
        for position in positions:
            if position['symbol'] == ticker and position['side'] == 'long':
                l_s = 'long'
            elif position['symbol'] == ticker and position['side'] == 'short':
                l_s = 'short'
               
    return l_s


# *****************************************************************************
def calculate_stop(ticker, current_price, max_dd, l_s):
    last_stop = stop_prices[ticker]
    
    if l_s == 'long':
        new_stop = current_price - max_dd
        if new_stop > last_stop:
            stop_prices[ticker] = new_stop
            return new_stop

    elif l_s == 'short':
        new_stop = current_price + max_dd
        if new_stop < last_stop or last_stop == 0.0:
            stop_prices[ticker] = new_stop
            return new_stop

    return last_stop


# *****************************************************************************
def trade_signal(ticker, l_s):
    signal = ''
    
    last_bar = api.get_barset(symbols=ticker, timeframe='15Min', limit=1)[ticker][0]
    opening_range = opening_ranges[ticker]['high'] - opening_ranges[ticker]['low']
    
    if l_s == '':
        if (side[ticker] == 'buy' and
            last_bar.c > opening_ranges[ticker]['high'] and
            ticker not in positions_taken):
                
            print(f'\n{ticker} has bullish daily pattern and has broken above the \
                  high of the opening range\ncurrent_price: {last_bar.c}\n')
            logging.error(f'\n{ticker} has bullish daily pattern and has broken \
                          above the high of the opening range\ncurrent_price: {last_bar.c}\n')
                          
            positions_taken.append(ticker)
            take_profits[ticker] = opening_ranges[ticker]['high'] + opening_range
            signal = 'buy'
                          
        elif (side[ticker] == 'sell' and
              last_bar.c < opening_ranges[ticker]['low'] and
              ticker not in positions_taken):
            
            print(f'{ticker} has bearish daily pattern and has broken below the \
                  low of the opening range\ncurrent_price: {last_bar.c}\n')
            logging.error(f'{ticker} has bearish daily pattern and has broken \
                          below the low of the opening range\ncurrent_price: {last_bar.c}\n')
            
            positions_taken.append(ticker)
            take_profits[ticker] = opening_ranges[ticker]['low'] - opening_range
            signal = 'sell'
            
            
    elif l_s == 'long':
        stop_price = calculate_stop(ticker, last_bar.c, opening_range, l_s)
        
        print(f'\ncurrent price: {last_bar.c} \
              \nstop_price: {stop_price} \
              \ntake_profit: {take_profits[ticker]}\n')
        
        if (last_bar.c > take_profits[ticker] or
            last_bar.c < stop_price):
            
            signal = 'close'
        
    elif l_s == 'short':
        stop_price = calculate_stop(ticker, last_bar.c, opening_range, l_s)
        
        print(f'\ncurrent price: {last_bar.c} \
              \nstop_price: {stop_price} \
              \ntake_profit: {take_profits[ticker]}\n')
        
        if (last_bar.c < take_profits[ticker] or
            last_bar.c > stop_price):
            
            signal = 'close'
            
    return signal


# ****************************************************************************************************************
def calculate_qty(df):
    close = df['close'].iloc[-1]
    amt_to_spend = buying_power / max_trades
    qty = math.floor(amt_to_spend / close)
    print(f'quantity: {qty}')
    logging.error(f'quantity: {qty}')
    
    return qty


# *****************************************************************************
def main():
    positions = requests.get(url=POSITIONS_URL, headers=headers)
    positions = positions.json()
    
    for ticker in tickers:
        try:
            l_s = get_position_details(positions, ticker)
            if l_s != '':
                print(f'\n{ticker}, {l_s}\n')
                logging.error(f'\n--- {ticker} {l_s} ---\n')
                
            signal = trade_signal(ticker, l_s)
            if l_s != '' or signal != '':
                print(f'signal: {signal}')
                logging.error(f'signal: {signal}')
                
            if signal == "buy" and len(positions) < max_trades:
                api.submit_order(symbol=ticker,
                                 qty=calculate_qty(df),
                                 side='buy',
                                 type='market',
                                 time_in_force='gtc',
                                 )
                print(f'\nNew long position initiated for {ticker} \
                      \n***************************************\n')
                logging.error(f'\nNew long position initiated for {ticker} \
                              \n***************************************\n')
            
            elif signal == "sell" and len(positions) < max_trades:
                api.submit_order(symbol=ticker,
                                 side='sell',
                                 qty=calculate_qty(df),
                                 type='market',
             				     time_in_force='gtc',
             				     )
                print(f'\nNew short position initiated for {ticker} \
                      \n***************************************\n')
                logging.error(f'\nNew short position initiated for {ticker} \
                              \n***************************************\n')
                
            elif signal == 'close':
                api.close_position(symbol=ticker)
                print(f'\nAll positions closed for {ticker} \
                      \n***************************************\n')
                logging.error(f'\nAll positions closed for {ticker} \
                              \n***************************************\n')
                
                
        except:
            print(f'error encountered... skipping {ticker}')
            logging.error(f'error encountered... skipping {ticker}')


# START
# *****************************************************************************
starttime=time.time()
timeout = time.time() + 60*60*4.0

starting_equity = float(requests.get(url=ACCOUNT_URL, headers=headers).json()['equity'])
daily_take_profit = 1.10
daily_stop_loss = .95

def daily_pct():
    return float(requests.get(url=ACCOUNT_URL, headers=headers).json()['equity']) / starting_equity

while time.time() <= timeout and daily_pct() < daily_take_profit and daily_pct() > daily_stop_loss:
    try:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print("\n----- passthrough at ",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '-----')
        logging.error(f'\n######## PASSTHROUGH AT {current_time} ########')
        main()
        time.sleep(900 - ((time.time() - starttime) % 60.0))
        
    except KeyboardInterrupt:
        print('\n\nKeyboard exception received. Exiting.')
        orders = api.list_orders(status='open')
        for order in orders:
            api.cancel_order(order.id)
        api.close_all_positions()
        print("all positions closed")
        logging.error('all positions closed')
        exit()
        
    except:
        orders = api.list_orders(status='open')
        for order in orders:
            api.cancel_order(order.id)
        api.close_all_positions()
        print("all positions closed")
        logging.error('all positions closed')
        exit()
        
        
orders = api.list_orders(status='open')
for order in orders:
    api.cancel_order(order.id)

api.close_all_positions()
print("all positions closed")
logging.error('all positions closed')