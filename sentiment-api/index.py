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








@app.route('/articles/<ticker>', methods=['GET'])
def get_num_articles(ticker):

    # GET ARTICLES FROM FINVIZ AND SPLIT BY ROW
    # *****************************************************************************
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
          articles = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="news-table"]/tbody'))).text
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
                  
                  if month == 'Apr':
                      month = '04'
                      
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