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


# *****************************************************************************


# # ----- CONGRESS -----
cursor.execute('delete from congress')

r = requests.get(QUIVER_URL + '/live/congresstrading', headers=headers)
congress_trading = r.json()

for filing in congress_trading:
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