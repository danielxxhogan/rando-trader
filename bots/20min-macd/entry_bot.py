import alpaca_trade_api as tradeapi
import talib as ta
import pandas as pd
import json
import math
import logging

from config import *

logging.basicConfig(filename='entry.log', filemode='w', level=logging.ERROR)

tickers = pd.read_csv('tickers.csv')['0'].tolist()
buying_power = 150000
max_trades = len(tickers)

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')


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
def trade_signal(ticker, df):
    signal = ''
    if (df['macd'].iloc[-1] > df['signal'].iloc[-1]):
        print(f'\n{ticker} macd above signal\n')
        logging.error(f'\n{ticker} macd above signal\n')
        
        signal = 'buy'
    
    elif (df['macd'].iloc[-1] < df['signal'].iloc[-1]):
        print(f'\n{ticker} macd below signal\n')
        logging.error(f'\n{ticker} macd below signal\n')
    
        signal = 'sell'
    
    return signal


# ****************************************************************************************************************
def calculate_qty(df):
    print('here')
    close = df['close'].iloc[-1]
    amt_to_spend = buying_power / max_trades
    qty = math.floor(amt_to_spend / close)
    
    print(f'quantity: {qty}')
    logging.error(f'quantity: {qty}')
    
    return qty


# ****************************************************************************************************************
def main():
    for ticker in tickers:
        print(f'\n{ticker}')
        try:
            df = create_df(ticker)
            print(df.tail())
            logging.error(f'\n{df.tail()}')
                
            signal = trade_signal(ticker, df)
            print(f'signal: {signal}')
            logging.error(f'signal: {signal}')
            
            if signal == 'buy':
                print('here')
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
                print('here')
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
                
        except Exception as e:
            print(f'error encountered... skipping {ticker}')
            print(e)
            logging.error(f'error encountered... skipping {ticker}')
            

if __name__ == '__main__':
    main()
            
            
            
            
            
            
