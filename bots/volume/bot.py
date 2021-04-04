import alpaca_trade_api as tradeapi
import psycopg2
import talib as ta
import pandas as pd
import time
import math
import requests
import numpy as np
import statsmodels.api as sm
import json
import logging

from config import *

logging.basicConfig(filename='volume.log', filemode='w', level=logging.ERROR)

buying_power = 150000
max_trades = 10

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

cursor.execute('select * rvol_seperated')
ticker_data = cursor.fetchall()
cursor.close()
conn.close()

tickers = []
atrs = {}
side = {}

for data in ticker_data:
    tickers.append(data[0])
    side[data[0]] = data[1]
    atrs[data[0]] = float(data[2])
    # break
    
stop_prices = {}
for ticker in tickers:
    stop_prices[ticker] = 0.0


# ****************************************************************************************************************
def get_position_details(positions, ticker):
    l_s = ''
    entry_price = 0.0
    
    if (len(positions)) > 0:
        for position in positions:
            if position['symbol'] == ticker and position['side'] == 'long':
                l_s = 'long'
                entry_price = float(position['avg_entry_price'])
            elif position['symbol'] == ticker and position['side'] == 'short':
                l_s = 'short'
                entry_price = float(position['avg_entry_price'])
               
    return l_s, entry_price


# ****************************************************************************************************************
def slope(series, n):
    series = (series - series.min()) / (series.max() - series.min())
    x = np.array(range(len(series)))
    x = (x - x.min()) / (x.max() - x.min())
    slopes = [i*0 for i in range(n-1)]
    for i in range(n, len(series) + 1):
        y_scaled = series[i - n:i]
        x_scaled = x[i - n:i]
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    
    return np.array(slope_angle)
  

# ****************************************************************************************************************
def create_df(ticker):
    delay = 3
    max_period = 20
    slope_period = 30
    bars_list = api.get_barset(symbols=ticker, timeframe='minute', limit=30)
    ticker_bars = bars_list[ticker]
    
    ohlc_df = pd.DataFrame(columns = ['high', 'low', 'close', 'volume'])
    high_list = []
    low_list = []
    close_list = []
    volume_list = []
    
    for i in range(len(ticker_bars)):
        high_list.append(ticker_bars[i].h)
        low_list.append(ticker_bars[i].l)
        close_list.append(ticker_bars[i].c)
        volume_list.append(ticker_bars[i].v)
    
    ohlc_df['high'] = high_list
    ohlc_df['low'] = low_list
    ohlc_df['close'] = close_list
    ohlc_df['volume'] = volume_list
    ohlc_df['v_shift'] = ohlc_df['volume'].shift(delay)
    ohlc_df['av'] = ohlc_df['volume'].rolling(window=delay).max()
    ohlc_df['max'] = ohlc_df['v_shift'].rolling(window=max_period-delay).max()
    ohlc_df['slope'] = slope(ohlc_df['close'], slope_period)
    
    return ohlc_df
        

# ****************************************************************************************************************
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


# ****************************************************************************************************************
def trade_signal(ticker, df, l_s, entry_price=0.0):
    signal = ''
    v_multiplier = 1.0
    take_profit_pct = 0.10
    stop_loss_pct = 0.05
    atr = atrs[ticker]
    max_dd = stop_loss_pct*atr
    current_price = df['close'].iloc[-1]
    stop_price = calculate_stop(ticker, current_price, max_dd, l_s)
    
    if l_s != '':
        print(f'atr: {atr}\ncurrent price: {current_price} \
              \nmax drawdown: {max_dd}\nstop price: {stop_price}')
        logging.error(f'atr: {atr}\ncurrent price: {current_price} \
                      \nmax drawdown: {max_dd}\nstop price: {stop_price}')
    
    if l_s == '':
        if ((( df['close'].iloc[-1] - df['close'].iloc[-2] ) / df['close'].iloc[-2] ) > 0.03 and
            df['av'].iloc[-1] >= df['max'].iloc[-1]*v_multiplier and
            side[ticker] == 'buy'):
                
            current_volume = df['av'].iloc[-1]
            previous_max = df['max'].iloc[-1]
            
            print(f'\n{ticker} is currently uptrending \
                  \ncurrent volume: {current_volume} \
                  \nprevious max: {previous_max}')
            logging.error(f'\n{ticker} is currently uptrending \
                          \ncurrent volume: {current_volume} \
                          \nprevious max: {previous_max}')
                          
            stop_prices[ticker] = 0.0
            signal = 'buy'
            
        elif ((( df['close'].iloc[-1] - df['close'].iloc[-2] ) / df['close'].iloc[-2] ) < -0.03 and
            df['av'].iloc[-1] >= df['max'].iloc[-1]*v_multiplier and
            side[ticker] == 'sell'):
                
            current_volume = df['av'].iloc[-1]
            previous_max = df['max'].iloc[-1]
            
            print(f'\n{ticker} is currently downtrending \
                  \ncurrent volume: {current_volume} \
                  \nprevious max: {previous_max}')
            logging.error(f'\n{ticker} is currently downtrending \
                          \ncurrent volume: {current_volume} \
                          \nprevious max: {previous_max}')
                          
            stop_prices[ticker] = 0.0
            signal = 'sell'
        
    elif l_s == 'long':
        take_profit_price = entry_price + take_profit_pct*atr
        print(f'take profit price: {take_profit_price}')
        logging.error(f'take profit price: {take_profit_price}')
        if current_price >= take_profit_price or current_price <= stop_price:
            
            signal = 'close'
            
    elif l_s == 'short':
        take_profit_price = entry_price - (take_profit_pct*atr)
        print(f'take profit price: {take_profit_price}')
        logging.error(f'take profit price: {take_profit_price}')
        if current_price <= take_profit_price or current_price >= stop_price:
            
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


# ****************************************************************************************************************
def calculate_price(ticker, signal):
    last_quote = api.get_last_quote(symbol=ticker)
    last_bid_price = last_quote.bidprice - 0.00
    last_ask_price = last_quote.askprice + 0.00
    print(f'last bid price: {last_bid_price}\nlast ask price: {last_ask_price}')
    logging.error(f'last bid price: {last_bid_price}\nlast ask price: {last_ask_price}')
    
    if signal == 'buy':
        return last_bid_price
    elif signal == 'sell':
        return last_ask_price


# ****************************************************************************************************************
def main():
    orders = api.list_orders(status='open')
    for order in orders:
        api.cancel_order(order.id)
        
    positions = requests.get(url=POSITIONS_URL, headers=headers)
    positions = positions.json()
    
    for ticker in tickers:
        try:
            l_s, entry_price = get_position_details(positions, ticker)
            if l_s != '':
                print('\n', ticker, l_s)
                logging.error(f'\n--- {ticker} {l_s} ---')
            df = create_df(ticker)
            if l_s != '':
                print(df.tail())
                logging.error(f'\n{df.tail()}')
            signal = trade_signal(ticker, df, l_s, entry_price)
            if l_s != '' or signal != '':
                print(f'signal: {signal}')
                logging.error(f'signal: {signal}')
            
            if signal == "buy" and len(positions) < max_trades:
                api.submit_order(symbol=ticker,
                                 qty=calculate_qty(df),
                                 side='buy',
                                 type='limit',
                                 limit_price=calculate_price(ticker, signal),
                                 time_in_force='gtc',
                                 )
                print(f'\nNew long position initiated for {ticker} \n***************************************\n')
                logging.error(f'\nNew long position initiated for {ticker} \n***************************************\n')
            
            elif signal == "sell" and len(positions) < max_trades:
                api.submit_order(symbol=ticker,
                                 side='sell',
                                 qty=calculate_qty(df),
                                 type='limit',
                                 limit_price=calculate_price(ticker, signal),
             				     time_in_force='gtc',
             				     )
                print(f'\nNew short position initiated for {ticker}\n***************************************\n')
                logging.error(f'\nNew short position initiated for {ticker}\n***************************************\n')
                
            elif signal == 'close':
                api.close_position(symbol=ticker)
                print(f'\nAll positions closed for {ticker} \n***************************************\n')
                logging.error(f'\nAll positions closed for {ticker} \n***************************************\n')
                
        except:
            print(f'error encountered... skipping {ticker}')
            logging.error(f'error encountered... skipping {ticker}')


# START
# ********************************************************************************************************************************
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
        time.sleep(60 - ((time.time() - starttime) % 60.0))
        
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