from selenium import webdriver
from google.cloud import language_v1
import psycopg2
import requests
import datetime as dt
import os

from config import *


conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

client = language_v1.LanguageServiceClient()

browser = webdriver.Chrome()

# This script will execute toward the end of the trading day. It will get all
# companies reporting earnings after market from the db.
# It will query polygon api for news about the stock.
# It will look at the number of articles written that day,
# get a sentiment score for the day if possible,
# get the overall sentiment score
# Then it will query the stocktwits api and get the number of mentions that day,
# get sentiment score for the day if possible,
# get overall sentiment score
# Then it will scrape stocktwits to get the sentiment from stocktwits
# and the change in mentions
# it will store all this data for each stock reporting earnings after market each day.


# GET ALL STOCKS REPORTING AFTER MARKET
browser.get('https://www.benzinga.com/news/earnings')
earnings = browser.find_element_by_class_name('ag-center-cols-container').text.split('\n')
browser.quit()

for i in range(0, len(earnings), 11):
    if earnings[i+2] == 'PM':
        try:
            ticker = earnings[i+3]
            print(f'ticker: {ticker}\n\n')
    
            # GET NEWS FOR EACH STOCK, CALCULATE CURRENT ARTICLES, CURRENT SENTIMENT, AND OVERALL SENTIMENT
            # *********************************************************************************************
            
            # r = requests.get(f'https://api.polygon.io/v1/meta/symbols/{ticker}/news?apiKey={POLYGON_API_KEY}')
            # articles = r.json()
            
            r = requests.get(f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={ALPHA_VANTAGE_API_KEY}')
            company_name = r.json()['Name']
            
            r = requests.get(f'https://newsapi.org/v2/everything?q={company_name}&apiKey={NEWS_API_KEY}')
            articles = r.json()['articles']
            
            articles_today = 0
            
            total_magnitude = 0.0
            total_sentiment = 0.0
            magnitude_scores = []
            sentiment_scores = []
            
            today_total_magnitude = 0.0
            today_total_sentiment = 0.0
            today_magnitude_scores = []
            today_sentiment_scores = []
            
            for article in articles:
                try:
                    if ticker == 'DLPN':
                        print(article)
                        
                    article_string = article['title'] + ' ' + article['description'] + ' ' + article['content']
                    document = language_v1.Document(content=article_string, type_=language_v1.Document.Type.PLAIN_TEXT)
                    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
        
                    if article['publishedAt'][:10] == dt.datetime.today().strftime('%Y-%m-%d'):
                        articles_today += 1
                        
                        today_total_magnitude += sentiment.magnitude
                        today_magnitude_scores.append(sentiment.magnitude)
                        today_sentiment_scores.append(sentiment.score)
                    
                    else:
                        total_magnitude += sentiment.magnitude
                        magnitude_scores.append(sentiment.magnitude)
                        sentiment_scores.append(sentiment.score)
                        
                except:
                    pass
                    
            for i in range(len(today_sentiment_scores)):
                magnitude = today_magnitude_scores[i] / today_total_magnitude
                sentiment = today_sentiment_scores[i] * magnitude
                today_total_sentiment += sentiment
                
            total_magnitude += today_total_magnitude
            magnitude_scores += today_magnitude_scores
            sentiment_scores += today_sentiment_scores
            
            for i in range(len(sentiment_scores)):
                magnitude = magnitude_scores[i] / total_magnitude
                sentiment = sentiment_scores[i] * magnitude
                total_sentiment += sentiment
                
            print(f'articles today: {articles_today}\n \
                    todays sentiment: {today_total_sentiment}\n \
                    overall sentiment: {total_sentiment}\n\n')
                    
                    
            # GET STOCKTWITS DATA FOR EACH STOCK, CALCULATE CURRENT MESSAGES, CURRENT SENTIMENT, AND OVERALL SENTIMENT
            # ********************************************************************************************************
            
            r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json')
            messages = r.json()['messages']
            
            messages_today = 0
            
            total_magnitude = 0.0
            total_sentiment_st = 0.0
            magnitude_scores = []
            sentiment_scores = []
            
            today_total_magnitude = 0.0
            today_total_sentiment_st = 0.0
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
                        
                except:
                    pass
                    
            for i in range(len(today_sentiment_scores)):
                magnitude = today_magnitude_scores[i] / today_total_magnitude
                sentiment = today_sentiment_scores[i] * magnitude
                today_total_sentiment_st += sentiment
                
            total_magnitude += today_total_magnitude
            magnitude_scores += today_magnitude_scores
            sentiment_scores += today_sentiment_scores
            
            for i in range(len(sentiment_scores)):
                magnitude = magnitude_scores[i] / total_magnitude
                sentiment = sentiment_scores[i] * magnitude
                total_sentiment_st += sentiment
                
            print(f'messages today: {messages_today}\n \
                    todays sentiment: {today_total_sentiment_st}\n \
                    overall sentiment: {total_sentiment_st}\n\n')
                    
        except:
            pass
                
        
        

# GET STOCKTWITS DATA, CALCULATE CURRENT MENTIONS, CURRENT SENTIMENT, AND OVERALL SENTIMENT


# GET STOCKTWITS SENTIMENT AND CHANGE IN MENTIONS











