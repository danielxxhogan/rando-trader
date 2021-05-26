from flask import Flask
# import psycopg2

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from google.cloud import language_v1
import datetime as dt

from config import *

app = Flask(__name__)
client = language_v1.LanguageServiceClient()


@app.route('/test', methods=['GET'])
def test():
    # conn = psycopg2.connect(user=PG_USER,
    #              password=PG_PASSWORD,
    #              host=PG_HOST,
    #              port=PG_PORT,
    #              dbname=PG_DATABASE,
    #              )

    # cursor = conn.cursor()
    
    # conn.commit()

    # cursor.close()
    # conn.close()
    
    return 'test'


# GET ANALYST RATINGS FROM BENZINGA
# *****************************************************************************
@app.route('/analyst-ratings/<ticker>', methods=['GET'])
def get_analyst_ratings(ticker):
  try:
    response = {}

    upgrades = 0
    downgrades = 0
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(f'https://www.benzinga.com/stock/{ticker}')
        analyst_ratings = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="benzinga-main"]/div[2]/div[2]/div[1]/div/div[5]/div/div/table[2]/tbody'))).text
        analyst_ratings = analyst_ratings.split('\n')
        browser.quit()

        for rating in analyst_ratings:
            rating = rating.split()
            if 'Upgrades' in rating:
                upgrades += 1
            elif 'Downgrades' in rating:
                downgrades += 1
                
        print(f'upgrades: {upgrades}')
        print(f'downgrades: {downgrades}')
        
    except:
        pass
    
    response['upgrades'] = upgrades
    response['downgrades'] = downgrades
    
    return response

  except Exception as e:
    print(e)
    return 'Server Error', 500


# GET INSIDER TRADING
# *****************************************************************************
@app.route('/insider-trading/<ticker>', methods=['GET'])
def get_insider_trading(ticker):
  try:
    response = {}
    insider_trades = 0
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(f'https://finviz.com/quote.ashx?t={ticker}')
        insider_trading = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div/table[3]/tbody/tr[12]/td/table/tbody'))).text.split('\n')
        browser.quit()

        for filing in insider_trading:
            if 'Buy' in filing:
                insider_trades += 1
                
        print(f'insider trades: {insider_trades}')
                
    except:
        pass
    
    response['insider_trades'] = insider_trades
    return response

  except Exception as e:
    return 'Server Error', 500


# GET QUIVER DATA FOR TICKER
# *****************************************************************************
@app.route('/quiver-quant/<ticker>', methods=['GET'])
def get_quiver_data(ticker):
  try:
    response = {}

    month_ago = (dt.datetime.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
    print(month_ago)
    QUIVER_URL = 'https://api.quiverquant.com/beta'
    headers = {'accept': 'application/json',
               'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
               'Authorization': f'Token {QUIVER_API_KEY}'}
    
    # ----- contract -----
    num_contracts = 0
    
    try:
        r = requests.get(f'{QUIVER_URL}/historical/govcontractsall/{ticker}', headers=headers)
        contracts = r.json()
        
        for filing in contracts:
            if filing['Date'] > month_ago:        
                num_contracts += 1
                
        print(f'contracts: {num_contracts}')
        
    except:
        pass
    
    response['contracts'] = num_contracts
    
    
    # ----- lobbying -----
    num_lobbying = 0
    
    try:
        r = requests.get(f'{QUIVER_URL}/historical/lobbying/{ticker}', headers=headers)
        lobbying = r.json()
        
        for filing in lobbying:
            if filing['Date'] > month_ago:        
                num_lobbying += 1
                
        print(f'lobbying: {num_lobbying}\n')
        
    except:
        pass
    
    response['lobbying'] = num_lobbying
    
    
    # ----- congress -----
    congress_buys = 0
    congress_sales = 0
    
    try:
        r = requests.get(f'{QUIVER_URL}/historical/congresstrading/{ticker}', headers=headers)
        congress = r.json()
        
        
        for filing in congress:
            if filing['TransactionDate'] > month_ago and filing['Transaction'] == 'Purchase':
                congress_buys += 1
                
            elif filing['TransactionDate'] > month_ago and filing['Transaction'] == 'Sale':
                congress_sales += 1
                
        print(f'congress buys: {congress_buys}')
        print(f'congress sells: {congress_sales}')
        
    except:
        pass
    
    response['congress_buys'] = congress_buys
    response['congress_sales'] = congress_sales
            
    # ----- senate -----
    senate_buys = 0
    senate_sales = 0
    
    try:
        r = requests.get(f'{QUIVER_URL}/historical/senatetrading/{ticker}', headers=headers)
        senate = r.json()
        
        
        for filing in senate:
            if filing['Date'] > month_ago and filing['Transaction'] == 'Purchase':
                senate_buys += 1
                
            elif filing['Date'] > month_ago and filing['Transaction'] == 'Sale':
                senate_sales += 1
                
        print(f'senate buys: {senate_buys}')
        print(f'senate sells: {senate_sales}')
        
    except:
        pass
    
    response['senate_buys'] = senate_buys
    response['senate_sales'] = senate_sales        
    
    # ----- house -----
    house_buys = 0
    house_sales = 0
    
    try:
        r = requests.get(f'{QUIVER_URL}/historical/housetrading/{ticker}', headers=headers)
        house = r.json()
        
        
        for filing in house:
            if filing['Date'] > month_ago and filing['Transaction'] == 'Purchase':
                house_buys += 1
                
            elif filing['Date'] > month_ago and filing['Transaction'] == 'Sale':
                house_sales += 1
                
        print(f'house buys: {house_buys}')
        print(f'house sells: {house_sales}\n')
        
    except:
        pass
    
    response['house_buys'] = house_buys
    response['house_sales'] = house_sales

    return response


    
  except Exception as e:
    print(e)
    return 'Server Error', 500


# GET PRESS RELEASES FROM BENZINGA
# *****************************************************************************
@app.route('/press-releases/<ticker>', methods=['GET'])
def get_press_releases(ticker):
    response = {}

    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    press_releases_today = 0
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(f'https://www.benzinga.com/stock-articles/{ticker}/press-releases')
        try:
          press_releases = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="benzinga-content-area"]/div/div/div/div[1]/div[1]'))).text
        except Exception as e:
          print(e)
        press_releases = press_releases.split('\n')
        browser.quit()
        
        date = press_releases[0].split()
        month = date[1]
        day = date[2][:-1]
        year = date[3]
        
        month = months.index(month) + 1
        if month < 10:
            month = f'0{str(month)}'
        else:
            month = str(month)
            
        date = f'{year}-{month}-{day}'
        today = dt.datetime.today().strftime('%Y-%m-%d')
        
        if date == today:
            for j in range(1, len(press_releases), 2):
                press_releases_today += 1
            
        print(f'press releases today: {press_releases_today}\n')
        
    except:
        pass
    
    response['press_releases'] = press_releases_today
    return response


# GET STOCKTWITS DATA FOR TICKER, CALCULATE CURRENT MESSAGES, CURRENT SENTIMENT, AND OVERALL SENTIMENT
# ********************************************************************************************************
@app.route('/stocktwits/<ticker>', methods=['GET'])
def get_stocktwits_data(ticker):
  try:

    response = {}

    messages_today = 0
    total_sentiment_st = 0.0
    today_total_sentiment_st = 0.0
    
    try:
        r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json')
        messages = r.json()['messages']
        
        total_magnitude = 0.0
        magnitude_scores = []
        sentiment_scores = []
        today_total_magnitude = 0.0
        today_magnitude_scores = []
        today_sentiment_scores = []
        
        for message in messages:
            try:
                message_string = message['body']
                document = language_v1.Document(content=message_string, type_=language_v1.Document.Type.PLAIN_TEXT)
                sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        
                if message['created_at'][:10] == dt.datetime.today().strftime('%Y-%m-%d'):
                    messages_today += 1
                    
                    today_total_magnitude += sentiment.magnitude
                    today_magnitude_scores.append(sentiment.magnitude)
                    today_sentiment_scores.append(sentiment.score)
                
                else:
                    total_magnitude += sentiment.magnitude
                    magnitude_scores.append(sentiment.magnitude)
                    sentiment_scores.append(sentiment.score)
                    
            except Exception as e:
                print('1', e)
                pass
                
        for i in range(len(today_sentiment_scores)):
            try:
                magnitude = today_magnitude_scores[i] / today_total_magnitude
                sentiment = today_sentiment_scores[i] * magnitude
                today_total_sentiment_st += sentiment
            except:
                print('2')
                pass
            
        total_magnitude += today_total_magnitude
        magnitude_scores += today_magnitude_scores
        sentiment_scores += today_sentiment_scores
        
        for i in range(len(sentiment_scores)):
            try:
                magnitude = magnitude_scores[i] / total_magnitude
                sentiment = sentiment_scores[i] * magnitude
                total_sentiment_st += sentiment
            except:
                print('3')
                pass
            
        print(f'messages today: {messages_today} \
                \ntodays sentiment: {today_total_sentiment_st} \
                \noverall sentiment: {total_sentiment_st}\n')
                
    except:
        print('4')
        pass
            
    response['messages'] = messages_today
    response['today_sentiment_st'] = today_total_sentiment_st
    response['sentiment_st'] = total_sentiment_st

    return response

  except Exception as e:
    print(e)
    return 'Server Error', 500


# GET ARTICLES FROM FINVIZ AND SPLIT BY ROW
# *****************************************************************************
@app.route('/articles/<ticker>', methods=['GET'])
def get_articles_data(ticker):

    response = {}

    articles_today = 0
    total_sentiment = 0.0
    today_total_sentiment = 0.0
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        browser = webdriver.Chrome(options=options)
        browser.get(f'https://finviz.com/quote.ashx?t={ticker}')
        try:
          articles = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="news-table"]/tbody'))).text
          browser.quit()

          articles = articles.split('\n')
          
          total_magnitude = 0.0
          magnitude_scores = []
          sentiment_scores = []
          today_total_magnitude = 0.0
          today_magnitude_scores = []
          today_sentiment_scores = []
          
          for i in range(0, len(articles), 3):
              time = articles[i+0]
              time = time.split(' ')
              time = [x for x in time if x != '']
              
              if len(time) == 2:
                  date = time[0]
                  month = date[:3]
                  
                  if month == 'May':
                      month = '05'
                      
                  day = date[4:6]
                  year = date[7:9]
                  date = f'{year}-{month}-{day}'
                  
                  if date == dt.datetime.today().strftime('%y-%m-%d'):
                      today = True
                  else:
                      today = False
              
              try:
                  article_string = articles[i+1]
                  document = language_v1.Document(content=article_string, type_=language_v1.Document.Type.PLAIN_TEXT)
                  sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
                  
                  if today == True:
                      articles_today += 1
                      
                      today_total_magnitude += sentiment.magnitude
                      today_magnitude_scores.append(sentiment.magnitude)
                      today_sentiment_scores.append(sentiment.score)
                      
                  elif today == False:
                      total_magnitude += sentiment.magnitude
                      magnitude_scores.append(sentiment.magnitude)
                      sentiment_scores.append(sentiment.score)
                      
              except Exception as e:
                  print('1', e)
              
          
          for i in range(len(today_sentiment_scores)):
              try:
                  magnitude = today_magnitude_scores[i] / today_total_magnitude
                  sentiment = today_sentiment_scores[i] * magnitude
                  today_total_sentiment += sentiment
              except Exception as e:
                  print('2', e)
              
          total_magnitude += today_total_magnitude
          magnitude_scores += today_magnitude_scores
          sentiment_scores += today_sentiment_scores
          
          for i in range(len(sentiment_scores)):
              try:
                  magnitude = magnitude_scores[i] / total_magnitude
                  sentiment = sentiment_scores[i] * magnitude
                  total_sentiment += sentiment
              except Exception as e:
                  print('3', e)
              
          print(f'articles today: {articles_today} \
                  \ntodays sentiment: {today_total_sentiment} \
                  \noverall sentiment: {total_sentiment}\n')

        except Exception as e:
          print(e)
                
        response['articles'] = articles_today
        response['sentiment'] = total_sentiment
        response['today_sentiment'] = today_total_sentiment

        return response

    except Exception as e:
        print('4', e)
        return 'Server Error', 500


if __name__ == '__main__':
    app.run()