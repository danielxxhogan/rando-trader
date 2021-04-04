import pandas as pd
import alpaca_trade_api as tradeapi
import json
from math import isnan
import talib as ta
import psycopg2

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()
cursor.execute('delete from broad_universe')

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, PAPER_URL, api_version='v2')
tickers = api.list_assets(status=None, asset_class=None)

temp = []
for ticker in tickers:
    if ticker.tradable == True and ticker.status == 'active':
        temp.append(ticker)
    
tickers  = []
for ticker in temp:
    tickers.append(ticker.symbol)

# tickers = ['AMD', 'NVDA', 'XLK', 'SPRT', 'BA', 'WAFU', 'MVIS']


atrs = {}
seperated = {}
scores = {}

for i in range(0, len(tickers), 200):
    sequence = tickers[i:i+200]
    print(sequence)
    
    daily = api.get_barset(symbols=sequence, timeframe='day', limit=15)
    
    for j in range(len(daily)):
        try:
            ticker_data = daily[tickers[i+j]]
            print(tickers[i+j])
            
            ohlc_df = pd.DataFrame()
            open_list = []
            high_list = []
            low_list = []
            close_list = []
            volume_list = []
            
            for k in range(len(ticker_data)):
                open_list.append(ticker_data[k].o)
                high_list.append(ticker_data[k].h)
                low_list.append(ticker_data[k].l)
                close_list.append(ticker_data[k].c)
                volume_list.append(ticker_data[k].v)
                
            ohlc_df['open'] = open_list
            ohlc_df['high'] = high_list
            ohlc_df['low'] = low_list
            ohlc_df['close'] = close_list
            ohlc_df['volume'] = volume_list
            ohlc_df['avg_vol'] = ohlc_df['volume'].rolling(window=14).mean()
            ohlc_df['atr'] = ta.ATR(ohlc_df['high'], ohlc_df['low'], ohlc_df['close'], timeperiod=14)
            ohlc_df['atr_pct'] = ohlc_df['atr'] / ohlc_df['close']
            ohlc_df['CDL2CROWS'] = ta.CDL2CROWS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDL3BLACKCROWS'] = ta.CDL3BLACKCROWS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDL3INSIDE'] = ta.CDL3INSIDE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDL3LINESTRIKE'] = ta.CDL3LINESTRIKE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDL3OUTSIDE'] = ta.CDL3OUTSIDE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDL3STARSINSOUTH'] = ta.CDL3STARSINSOUTH(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDL3WHITESOLDIERS'] = ta.CDL3WHITESOLDIERS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLABANDONEDBABY'] = ta.CDLABANDONEDBABY(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLADVANCEBLOCK'] = ta.CDLADVANCEBLOCK(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLBELTHOLD'] = ta.CDLBELTHOLD(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLBREAKAWAY'] = ta.CDLBREAKAWAY(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLCLOSINGMARUBOZU'] = ta.CDLCLOSINGMARUBOZU(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLCONCEALBABYSWALL'] = ta.CDLCONCEALBABYSWALL(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLCOUNTERATTACK'] = ta.CDLCOUNTERATTACK(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLDARKCLOUDCOVER'] = ta.CDLDARKCLOUDCOVER(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLDOJI'] = ta.CDLDOJI(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLDOJISTAR'] = ta.CDLDOJISTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLDRAGONFLYDOJI'] = ta.CDLDRAGONFLYDOJI(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLENGULFING'] = ta.CDLENGULFING(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLEVENINGDOJISTAR'] = ta.CDLEVENINGDOJISTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLEVENINGSTAR'] = ta.CDLEVENINGSTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLGAPSIDESIDEWHITE'] = ta.CDLGAPSIDESIDEWHITE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLGRAVESTONEDOJI'] = ta.CDLGRAVESTONEDOJI(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHAMMER'] = ta.CDLHAMMER(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHANGINGMAN'] = ta.CDLHANGINGMAN(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHARAMI'] = ta.CDLHARAMI(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHARAMICROSS'] = ta.CDLHARAMICROSS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHIGHWAVE'] = ta.CDLHIGHWAVE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHIKKAKE'] = ta.CDLHIKKAKE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHIKKAKEMOD'] = ta.CDLHIKKAKEMOD(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLHOMINGPIGEON'] = ta.CDLHOMINGPIGEON(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLIDENTICAL3CROWS'] = ta.CDLIDENTICAL3CROWS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLINNECK'] = ta.CDLINNECK(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLINVERTEDHAMMER'] = ta.CDLINVERTEDHAMMER(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLKICKING'] = ta.CDLKICKING(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLKICKINGBYLENGTH'] = ta.CDLKICKINGBYLENGTH(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLLADDERBOTTOM'] = ta.CDLLADDERBOTTOM(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLLONGLEGGEDDOJI'] = ta.CDLLONGLEGGEDDOJI(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLLONGLINE'] = ta.CDLLONGLINE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLMARUBOZU'] = ta.CDLMARUBOZU(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLMATCHINGLOW'] = ta.CDLMATCHINGLOW(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLMATHOLD'] = ta.CDLMATHOLD(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLMORNINGDOJISTAR'] = ta.CDLMORNINGDOJISTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLMORNINGSTAR'] = ta.CDLMORNINGSTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLONNECK'] = ta.CDLONNECK(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLPIERCING'] = ta.CDLPIERCING(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLRICKSHAWMAN'] = ta.CDLRICKSHAWMAN(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLRISEFALL3METHODS'] = ta.CDLRISEFALL3METHODS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLSEPARATINGLINES'] = ta.CDLSEPARATINGLINES(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLSHOOTINGSTAR'] = ta.CDLSHOOTINGSTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLSHORTLINE'] = ta.CDLSHORTLINE(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLSPINNINGTOP'] = ta.CDLSPINNINGTOP(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLSTALLEDPATTERN'] = ta.CDLSTALLEDPATTERN(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLSTICKSANDWICH'] = ta.CDLSTICKSANDWICH(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLTAKURI'] = ta.CDLTAKURI(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLTASUKIGAP'] = ta.CDLTASUKIGAP(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLTHRUSTING'] = ta.CDLTHRUSTING(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLTRISTAR'] = ta.CDLTRISTAR(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLUNIQUE3RIVER'] = ta.CDLUNIQUE3RIVER(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLUPSIDEGAP2CROWS'] = ta.CDLUPSIDEGAP2CROWS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            ohlc_df['CDLXSIDEGAP3METHODS'] = ta.CDLXSIDEGAP3METHODS(ohlc_df['open'], ohlc_df['high'], ohlc_df['low'], ohlc_df['close'])
            
            if ohlc_df['atr_pct'].iloc[-1] < .05:
                pass
            
            elif ohlc_df['close'].iloc[-1] < 4.0:
                pass
            
            elif ohlc_df['volume'].iloc[-1] < 400000:
                pass
            
            else:
                todays_patterns = ohlc_df.values[-1][8:]
                current_ticker = tickers[i+j]
                current_atr = ohlc_df['atr'].iloc[-1]
                total = 0

                for pattern in todays_patterns:
                    # print(pattern)
                    total += pattern
                    
                print(f'total: {total}')
                    
                if total > 0 and not isnan(current_atr):
                    
                    atrs[current_ticker] = current_atr
                    seperated[current_ticker] = 'buy'
                    scores[current_ticker] = total
                    
                elif total < 0 and not isnan(current_atr):
                    
                    atrs[current_ticker] = current_atr
                    seperated[current_ticker] = 'sell'
                    scores[current_ticker] = total
                    
        except Exception as e:
            print(e)
        
    #     break
    # break
    

for key in atrs.keys():
    cursor.execute('insert into broad_universe (ticker, side, atr, score) \
                   values (%s, %s, %s, %s)', (key, seperated[key], atrs[key], scores[key]))
    
conn.commit()

cursor.close()
conn.close()