import psycopg2

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

# ----- QUIVER QUANT DATA -----
# *****************************************************************************
cursor.execute('create table if not exists congress (congress_id serial primary key, \
                                                     amount decimal, \
                                                     house varchar, \
                                                     report_date date, \
                                                     representative varchar, \
                                                     ticker varchar, \
                                                     transaction varchar, \
                                                     transaction_date date);')
    
cursor.execute('create table if not exists senate (senate_id serial primary key, \
                                                   amount decimal, \
                                                   date date, \
                                                   party varchar, \
                                                   senator varchar, \
                                                   ticker varchar, \
                                                   transaction varchar);')
    
cursor.execute('create table if not exists house (house_id serial primary key, \
                                                  amount decimal, \
                                                  date date, \
                                                  representative varchar, \
                                                  ticker varchar, \
                                                  transaction varchar);')
    
cursor.execute('create table if not exists contracts (contracts_id serial primary key, \
                                                      agency varchar, \
                                                      amount decimal, \
                                                      date date, \
                                                      description varchar, \
                                                      ticker varchar);')
    
cursor.execute('create table if not exists lobbying (lobbying_id serial primary key, \
                                                     amount decimal, \
                                                     client varchar, \
                                                     date date, \
                                                     issue varchar, \
                                                     specific_issue varchar, \
                                                     ticker varchar);')

# ----- SCREENERS -----
# *****************************************************************************
cursor.execute('create table if not exists high_score (ticker varchar, \
                                                          side varchar, \
                                                          atr decimal, \
                                                          score decimal);')
    
cursor.execute('create table if not exists rvol_seperated (ticker varchar, \
                                                           side varchar, \
                                                           atr decimal, \
                                                           rvol decimal, \
                                                           score decimal);')
    
cursor.execute('create table if not exists broad_universe (ticker varchar, \
                                                           side varchar, \
                                                           atr decimal, \
                                                           score decimal);')
    
cursor.execute('create table if not exists heavily_traded (ticker varchar, \
                                                           side varchar, \
                                                           atr decimal, \
                                                           score decimal);')

# ----- PORTFOLIOS -----
# *****************************************************************************
# cursor.execute('create table if not exists twenty_min_macd_portfolio (ticker varchar, \
#                                                                       side varchar)')

# ----- EARNINGS -----
# *****************************************************************************

# ----- MARKETWATCH EARNINGS -----
cursor.execute('create table if not exists morning_earnings (company varchar, \
                                                             symbol varchar, \
                                                             quarter varchar, \
                                                             estimate decimal, \
                                                             actual decimal, \
                                                             actual_surprise decimal, \
                                                             surprise_pct decimal)')
    
cursor.execute('create table if not exists after_market_earnings (company varchar, \
                                                                  symbol varchar, \
                                                                  quarter varchar, \
                                                                  estimate decimal, \
                                                                  actual decimal, \
                                                                  actual_surprise decimal, \
                                                                  surprise_pct decimal)')
    
# ----- BENZINGA EARNINGS -----



# ----- EARNINGS SENTIMENT -----


    
# ----- INSIDER TRADING -----
# *****************************************************************************
cursor.execute('create table if not exists insider_trading (it_id serial primary key, \
                                                            filing_date date, \
                                                            trade_date date, \
                                                            ticker varchar, \
                                                            company varchar, \
                                                            insider varchar, \
                                                            title varchar, \
                                                            price decimal, \
                                                            qty decimal, \
                                                            owned decimal, \
                                                            change varchar, \
                                                            value decimal)')
    

# ----- PREMARKET MOVERS -----
# *****************************************************************************
cursor.execute('create table if not exists premarket_gainers (ticker varchar, \
                                                              company varchar, \
                                                              price varchar, \
                                                              change varchar, \
                                                              volume varchar)')
                                                              
cursor.execute('create table if not exists premarket_losers (ticker varchar, \
                                                             company varchar, \
                                                             price varchar, \
                                                             change varchar, \
                                                             volume varchar)')

cursor.execute('create table if not exists most_active (ticker varchar, \
                                                        company varchar, \
                                                        price varchar, \
                                                        change varchar, \
                                                        volume varchar)')






conn.commit()

cursor.close()
conn.close()