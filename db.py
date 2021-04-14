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
    

# ----- EARNINGS -----
# *****************************************************************************
cursor.execute('create table if not exists morning_earnings (date date, \
                                                             ticker varchar, \
                                                             estimate decimal, \
                                                             actual decimal, \
                                                             surprise decimal)')
    
cursor.execute('create table if not exists after_market_earnings (date date, \
                                                             ticker varchar, \
                                                             estimate decimal, \
                                                             actual decimal, \
                                                             surprise decimal)')
    

# ----- EARNINGS SENTIMENT -----
cursor.execute('create table if not exists earnings_sentiment (date date, \
                                                               ticker varchar, \
                                                               articles integer, \
                                                               sentiment_today decimal, \
                                                               overall_sentiment decimal, \
                                                               messages integer, \
                                                               st_sentiment_today decimal, \
                                                               st_overall_sentiment decimal)')
    

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
    

# MERGERS AND ACQUISITIONS AND SENTIMENT
# *****************************************************************************
cursor.execute('create table if not exists ma_sentiment (ticker varchar, \
                                                         articles integer, \
                                                         sentiment decimal, \
                                                         today_sentiment decimal, \
                                                         messages integer, \
                                                         today_sentiment_st decimal, \
                                                         sentiment_st decimal, \
                                                         press_releases integer, \
                                                         contracts integer, \
                                                         lobbying integer, \
                                                         congress_buys integer, \
                                                         congress_sells integer, \
                                                         senate_buys integer, \
                                                         senate_sells integer, \
                                                         house_buys integer, \
                                                         house_sells integer, \
                                                         insider_trades integer, \
                                                         upgrades integer, \
                                                         downgrades integer)')
    
    
# ANALYST UPGRADES AND SENTIMENT
# *****************************************************************************
cursor.execute('create table if not exists upgrades_sentiment (ticker varchar, \
                                                         articles integer, \
                                                         sentiment decimal, \
                                                         today_sentiment decimal, \
                                                         messages integer, \
                                                         today_sentiment_st decimal, \
                                                         sentiment_st decimal, \
                                                         press_releases integer, \
                                                         contracts integer, \
                                                         lobbying integer, \
                                                         congress_buys integer, \
                                                         congress_sells integer, \
                                                         senate_buys integer, \
                                                         senate_sells integer, \
                                                         house_buys integer, \
                                                         house_sells integer, \
                                                         insider_trades integer, \
                                                         upgrades integer, \
                                                         downgrades integer)')
    
    
# ANALYST UPGRADES AND SENTIMENT
# *****************************************************************************
cursor.execute('create table if not exists downgrades_sentiment (ticker varchar, \
                                                         articles integer, \
                                                         sentiment decimal, \
                                                         today_sentiment decimal, \
                                                         messages integer, \
                                                         today_sentiment_st decimal, \
                                                         sentiment_st decimal, \
                                                         press_releases integer, \
                                                         contracts integer, \
                                                         lobbying integer, \
                                                         congress_buys integer, \
                                                         congress_sells integer, \
                                                         senate_buys integer, \
                                                         senate_sells integer, \
                                                         house_buys integer, \
                                                         house_sells integer, \
                                                         insider_trades integer, \
                                                         upgrades integer, \
                                                         downgrades integer)')
    
    
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


conn.commit()

cursor.close()
conn.close()