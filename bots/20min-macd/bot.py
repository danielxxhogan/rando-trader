import alpaca_trade_api as tradeapi
import pandas as pd
import logging
import requests
import talib as ta
import math

from config import *

logging.basicConfig(filename='20min.log', filemode='w', level=logging.ERROR)

tickers = pd.read_csv('tickers.csv')['0'].tolist()
buying_power = 150000
max_trades = len(tickers)

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')


# ****************************************************************************************************************
def get_position_details(positions, ticker):
    l_s = ''
    
    if (len(positions)) > 0:
        for position in positions:
            if position['symbol'] == ticker and position['side'] == 'long':
                l_s = 'long'
            elif position['symbol'] == ticker and position['side'] == 'short':
                l_s = 'short'
               
    return l_s


# ****************************************************************************************************************
def create_df(ticker):
    bars_list = api.get_barset(symbols=ticker, timeframe='minute', limit=34)
    ticker_bars = bars_list[ticker]
    
    ohlc = pd.DataFrame()
    close_list = []
    volume_list = []
    
    for i in range(len(ticker_bars)):
        close_list.append(ticker_bars[i].c)
        volume_list.append(ticker_bars[i].v)
    
    ohlc['close'] = close_list
    (ohlc['macd'],
      ohlc['signal'],
      ohlc['hist']) = ta.MACD(ohlc['close'])

    return ohlc


# ****************************************************************************************************************
def calculate_qty(df):
    close = df['close'].iloc[-1]
    amt_to_spend = buying_power / max_trades
    qty = math.floor(amt_to_spend / close)
    
    print(f'quantity: {qty}')
    logging.error(f'quantity: {qty}')
    
    return qty


# ****************************************************************************************************************
def trade_signal(ticker, df, l_s):
    signal = ''
    
    if l_s == '':
        if (df['macd'].iloc[-1] > df['signal'].iloc[-1]):
            print(f'\n{ticker} macd above signal\n')
            logging.error(f'\n{ticker} macd above signal\n')
            
            signal = 'buy'
        
        elif (df['macd'].iloc[-1] < df['signal'].iloc[-1]):
            print(f'\n{ticker} macd below signal\n')
            logging.error(f'\n{ticker} macd below signal\n')
        
            signal = 'sell'
            
    elif l_s == 'long':
        if (df['macd'].iloc[-1] < df['signal'].iloc[-1]):
            print(f'\n{ticker} macd was above signal now below signal\n \
                  closing long position opening short position')
            logging.error(f'\n{ticker} macd was above signal now below signal\n \
                          closing long position opening short position')

            signal = 'close-sell'
            
    elif l_s == 'short':
        if (df['macd'].iloc[-1] > df['signal'].iloc[-1]):
            print(f'\n{ticker} macd was below signal now above signal\n \
                  closing short position opening long position')
            logging.error(f'\n{ticker} macd was below signal now above signal\n \
                          closing short position opening long position')

            signal = 'close-buy'
            
    
    return signal


# ****************************************************************************************************************
def main():
    positions = requests.get(url=POSITIONS_URL, headers=headers)
    positions = positions.json()
    
    for ticker in tickers:
        print(f'\n{ticker}')
        logging.error(f'/n{ticker}')
        
        try:
            l_s = get_position_details(positions, ticker)
            print(f'\n{l_s}')
            logging.error(f'\n{l_s}')
            
            df = create_df(ticker)
            print(df.tail())
            logging.error(f'\n{df.tail()}')
                
            signal = trade_signal(ticker, df, l_s)
            print(f'signal: {signal}')
            logging.error(f'signal: {signal}')


            if signal == 'buy' and len(positions) < max_trades:
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


            elif signal == 'sell':
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
                
            elif signal == 'close-sell' and len(positions) <= max_trades:
                api.close_position(symbol=ticker)
                
                api.submit_order(symbol=ticker,
                                 side='sell',
                                 qty=calculate_qty(df),
                                 type='market',
               				     time_in_force='gtc',
               				     )
                print(f'\nclosing long position, opening short position for {ticker} \
                      \n***************************************\n')
                logging.error(f'\nclosing long position, opening short position for {ticker} \
                              \n***************************************\n')
                
            elif signal == 'close-buy' and len(positions) <= max_trades:
                api.close_position(symbol=ticker)
                
                api.submit_order(symbol=ticker,
                                 side='buy',
                                 qty=calculate_qty(df),
                                 type='market',
               				     time_in_force='gtc',
               				     )
                print(f'\nclosing short position, opening long position for {ticker} \
                      \n***************************************\n')
                logging.error(f'\nclosing short position, opening long position for {ticker} \
                              \n***************************************\n')
                
        except Exception as e:
            print(f'error encountered... skipping {ticker}')
            print(e)
            logging.error(f'error encountered... skipping {ticker}')
            

if __name__ == '__main__':
    main()