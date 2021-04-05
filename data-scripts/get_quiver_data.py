import requests
import pandas as pd
import datetime as dt
import psycopg2

from config import *

QUIVER_URL = 'https://api.quiverquant.com/beta'

headers = {'accept': 'application/json',
           'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
           'Authorization': f'Token {QUIVER_API_KEY}'}

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

# one_month_ago = (dt.datetime.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')


# EMPY AND RESET
# *****************************************************************************
# when the code above runs, all new data is appended to the tables. If too much
# unused data accumulate delete all tables and repopulate with just most recent

# # ----- CONGRESS -----
cursor.execute('delete from congress')

r = requests.get(QUIVER_URL + '/live/congresstrading', headers=headers)
congress_trading = r.json()

for filing in congress_trading:
    # if filing['ReportDate'] > one_month_ago:
    cursor.execute('insert into congress (amount, house, report_date, representative, ticker, transaction, transaction_date) \
                    values(%s, %s, %s, %s, %s, %s, %s)',
                    (filing['Amount'],
                    filing['House'],
                    filing['ReportDate'],
                    filing['Representative'],
                    filing['Ticker'],
                    filing['Transaction'],
                    filing['TransactionDate']))

conn.commit()

# # ----- SENATE -----
cursor.execute('delete from senate')

r = requests.get(QUIVER_URL + '/live/senatetrading', headers=headers)
senate_trading = r.json()

for filing in senate_trading:
    # if filing['Date'] > one_month_ago:
    cursor.execute('insert into senate (amount, date, party, senator, ticker, transaction) \
                    values(%s, %s, %s, %s, %s, %s)',
                    (filing['Amount'],
                    filing['Date'],
                    filing['Party'],
                    filing['Senator'],
                    filing['Ticker'],
                    filing['Transaction']))

conn.commit()

# # ----- HOUSE -----
cursor.execute('delete from house')

r = requests.get(QUIVER_URL + '/live/housetrading', headers=headers)
house_trading = r.json()

for filing in house_trading:
    # if filing['Date'] > one_month_ago:
    cursor.execute('insert into house (amount, date, representative, ticker, transaction) \
                    values(%s, %s, %s, %s, %s)',
                    (filing['Amount'],
                    filing['Date'],
                    filing['Representative'],
                    filing['Ticker'],
                    filing['Transaction']))

conn.commit()

# # ----- CONTRACTS -----
cursor.execute('delete from contracts')

r = requests.get(QUIVER_URL + '/live/govcontractsall', headers=headers)
government_contracts = r.json()

for filing in government_contracts:
    # if filing['Date'] > one_month_ago:
    cursor.execute('insert into contracts (agency, amount, date, description, ticker) \
                    values(%s, %s, %s, %s, %s)',
                    (filing['Agency'],
                    filing['Amount'],
                    filing['Date'][:10],
                    filing['Description'],
                    filing['Ticker']))

conn.commit()

# # ----- LOBBYING -----
cursor.execute('delete from lobbying')

r = requests.get(QUIVER_URL + '/live/lobbying', headers=headers)
corporate_lobbying = r.json()

for filing in corporate_lobbying:
    # if filing['Date'] > one_month_ago:
    cursor.execute('insert into lobbying (amount, client, date, issue, specific_issue, ticker) \
                    values(%s, %s, %s, %s, %s, %s)',
                    (filing['Amount'],
                    filing['Client'],
                    filing['Date'],
                    filing['Issue'],
                    filing['Specific_Issue'],
                    filing['Ticker']))

conn.commit()


cursor.close()
conn.close()







# QUIVER QUANT API
# *****************************************************************************

# ----- CONGRESS -----
# r = requests.get(QUIVER_URL + '/live/congresstrading', headers=headers)
# congress_trading = r.json()

# cursor.execute('select * from congress \
#                 order by report_date desc')
                
# congress_results = cursor.fetchall()

# loops through the values in congress_trading which are the most recent filings
# returned by the api. if at any point the value in congress_trading matches the
# most recent value in congress_results from table in db, loop breaks, otherwise
# values from api are added to db starting with most recent.

# for i in range(len(congress_trading)):
#     if (congress_trading[i]['Amount'] == float(congress_results[0][1]) and
#         congress_trading[i]['House'] == congress_results[0][2] and
#         congress_trading[i]['ReportDate'] == congress_results[0][3].strftime('%Y-%m-%d') and
#         congress_trading[i]['Representative'] == congress_results[0][4] and
#         congress_trading[i]['Ticker'] == congress_results[0][5] and
#         congress_trading[i]['Transaction'] == congress_results[0][6] and
#         congress_trading[i]['TransactionDate'] == congress_results[0][7].strftime('%Y-%m-%d')):
#         print(True)
#         break
    



# ----- SENATE -----
# r = requests.get(QUIVER_URL + '/live/senatetrading', headers=headers)
# senate_trading = r.json()

# cursor.execute('select * from senate \
#                                 order by date desc')

# senate_results = cursor.fetchall()



# loops through the values in congress_trading which are the most recent filings
# returned by the api. if at any point the value in congress_trading matches the
# most recent value in congress_results from table in db, loop breaks, otherwise
# values from api are added to db starting with most recent.

# for i in range(len(congress_trading)):
#     if (congress_trading[i]['Amount'] == float(congress_results[0][1]) and
#         congress_trading[i]['House'] == congress_results[0][2] and
#         congress_trading[i]['ReportDate'] == congress_results[0][3].strftime('%Y-%m-%d') and
#         congress_trading[i]['Representative'] == congress_results[0][4] and
#         congress_trading[i]['Ticker'] == congress_results[0][5] and
#         congress_trading[i]['Transaction'] == congress_results[0][6] and
#         congress_trading[i]['TransactionDate'] == congress_results[0][7].strftime('%Y-%m-%d')):
#         print(True)
#         break
    
    
    
    



# ----- HOUSE -----
# r = requests.get(QUIVER_URL + '/live/housetrading', headers=headers)
# house_trading = r.json()

# cursor.execute('select * from house \
#                                order by date desc')
                               
# house_results = cursor.fetchall()




# loops through the values in congress_trading which are the most recent filings
# returned by the api. if at any point the value in congress_trading matches the
# most recent value in congress_results from table in db, loop breaks, otherwise
# values from api are added to db starting with most recent.

# for i in range(len(congress_trading)):
#     if (congress_trading[i]['Amount'] == float(congress_results[0][1]) and
#         congress_trading[i]['House'] == congress_results[0][2] and
#         congress_trading[i]['ReportDate'] == congress_results[0][3].strftime('%Y-%m-%d') and
#         congress_trading[i]['Representative'] == congress_results[0][4] and
#         congress_trading[i]['Ticker'] == congress_results[0][5] and
#         congress_trading[i]['Transaction'] == congress_results[0][6] and
#         congress_trading[i]['TransactionDate'] == congress_results[0][7].strftime('%Y-%m-%d')):
#         print(True)
#         break
    
    
    
    




# ----- CONTRACTS -----
# r = requests.get(QUIVER_URL + '/live/govcontractsall', headers=headers)
# government_contracts = r.json()

# cursor.execute('select * from contracts \
#                                    order by date desc')
                                   
# contracts_results = cursor.fetchall()



                                   
                                   
                                   
# loops through the values in congress_trading which are the most recent filings
# returned by the api. if at any point the value in congress_trading matches the
# most recent value in congress_results from table in db, loop breaks, otherwise
# values from api are added to db starting with most recent.

# for i in range(len(congress_trading)):
#     if (congress_trading[i]['Amount'] == float(congress_results[0][1]) and
#         congress_trading[i]['House'] == congress_results[0][2] and
#         congress_trading[i]['ReportDate'] == congress_results[0][3].strftime('%Y-%m-%d') and
#         congress_trading[i]['Representative'] == congress_results[0][4] and
#         congress_trading[i]['Ticker'] == congress_results[0][5] and
#         congress_trading[i]['Transaction'] == congress_results[0][6] and
#         congress_trading[i]['TransactionDate'] == congress_results[0][7].strftime('%Y-%m-%d')):
#         print(True)
#         break







# ----- LOBBYING -----
# r = requests.get(QUIVER_URL + '/live/lobbying', headers=headers)
# corporate_lobbying = r.json()

# cursor.execute('select * from lobbying \
#                                   order by date desc')

# lobbying_results = cursor.fetchall()




# loops through the values in congress_trading which are the most recent filings
# returned by the api. if at any point the value in congress_trading matches the
# most recent value in congress_results from table in db, loop breaks, otherwise
# values from api are added to db starting with most recent.

# for i in range(len(congress_trading)):
#     if (congress_trading[i]['Amount'] == float(congress_results[0][1]) and
#         congress_trading[i]['House'] == congress_results[0][2] and
#         congress_trading[i]['ReportDate'] == congress_results[0][3].strftime('%Y-%m-%d') and
#         congress_trading[i]['Representative'] == congress_results[0][4] and
#         congress_trading[i]['Ticker'] == congress_results[0][5] and
#         congress_trading[i]['Transaction'] == congress_results[0][6] and
#         congress_trading[i]['TransactionDate'] == congress_results[0][7].strftime('%Y-%m-%d')):
#         print(True)
#         break


# cursor.close()
# conn.close()









