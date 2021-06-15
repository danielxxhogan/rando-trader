# file: sentiment.py
# author: Daniel Hogan

# This python script defines a class called Sentiment. When a Sentiment object
# is instantiated, the constructor function takes in a ticker. There are 6 methods
# that can be invoked on a Sentiment object, get_news, get_stocktwits, get_press_releases,
# get_insider_trading, get_analyst_ratings, and get_quiver_data.
# *****************************************************************************

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from google.cloud import language_v1
import datetime as dt

from config import *


class Sentiment:
    def __init__(self, ticker):
        self.ticker = ticker
        self.client = language_v1.LanguageServiceClient()
        
    def get_news(self):
        SIGNIFICANT_DATA = 'description'
        ticker = self.ticker
        client = self.client

        try:
            results = {'articles_today': 0,
                        'total_sentiment': 0.0,
                        'today_total_sentiment': 0.0}

            containers = {'total_magnitude': 0.0,
                          'magnitude_scores': [],
                          'sentiment_scores': [],
                          'today_total_magnitude': 0.0,
                          'today_magnitude_scores': [],
                          'today_sentiment_scores': []}
            
            start = (dt.datetime.today()-dt.timedelta(30)).strftime('%Y-%m-%d')
            end = dt.datetime.today().strftime('%Y-%m-%d')
            r = requests.get(url=f'https://newsapi.org/v2/everything?q={ticker}&from={start}&apiKey={NEWS_API_KEY}')
            r = r.json()
            articles = r['articles']
            
            for article in articles:
                if article['publishedAt'][:10] == end:
                    today = True
                else:
                    today = False
                    
                results, containers = self.__get_sentiment(client, article[SIGNIFICANT_DATA], today, results, containers)
                    
            results = self.__calculate_totals(results, containers)
            return results
                    

        except Exception as e:
            print('wtf', e)
            return e
        
        
    def get_stocktwits(self):
        ticker = self.ticker
        client = self.client
        
        try:
            results = {'articles_today': 0,
                       'total_sentiment': 0.0,
                       'today_total_sentiment': 0.0}

            containers = {'total_magnitude': 0.0,
                          'magnitude_scores': [],
                          'sentiment_scores': [],
                          'today_total_magnitude': 0.0,
                          'today_magnitude_scores': [],
                          'today_sentiment_scores': []}
            
            r = requests.get(f'https://api.stocktwits.com/api/2/streams/symbol/{ticker}.json')
            messages = r.json()['messages']
            
            for message in messages:
                if message['created_at'][:10] == dt.datetime.today().strftime('%Y-%m-%d'):
                    today = True
                else:
                    today = False
                    
                results, container = self.__get_sentiment(client, message['body'], today, results, containers)
                
            results = self.__calculate_totals(results, containers)
            return results
        
        except Exception as e:
            print(e)
            return e
        
        
    def __get_sentiment(self, client, significant_data, today, results, containers):
        
        # This is helper function called by the get_news function.
        # significat_data is the string of data passed in whose sentiment score
        # we are interested in. Today is a boolean value True if the publish date of
        # the article is today, else False. results is the dictionary of values
        # that will be returned by get_news. Containers is the dictionary of data
        # structures used to store intermediate calculations.
        
        try:
            document = language_v1.Document(content=significant_data, type_=language_v1.Document.Type.PLAIN_TEXT)
            sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
            
            if today == True:
                results['articles_today'] += 1
                containers['today_total_magnitude'] += sentiment.magnitude
                containers['today_magnitude_scores'].append(sentiment.magnitude)
                containers['today_sentiment_scores'].append(sentiment.score)
                
            elif today == False:
                containers['total_magnitude'] += sentiment.magnitude
                containers['magnitude_scores'].append(sentiment.magnitude)
                containers['sentiment_scores'].append(sentiment.score)
            
        except Exception as e:
            print(e)
            
        return results, containers
    
        
    def __calculate_totals(self, results, containers):
        
        # iterate throught all sentiment scores for todays articles, and divide each articles
        # magnitude by total magnitude to get its relative magnitude. Multiply the relative
        # magnitude by that articles sentiment score to get its relative sentiment score
        # and add the relative sentiment score to the total sentiment score for today.
        
        for i in range(len(containers['today_sentiment_scores'])):
            magnitude = containers['today_magnitude_scores'][i] / containers['today_total_magnitude']
            sentiment = containers['today_sentiment_scores'][i] * magnitude
            results['today_total_sentiment'] += sentiment
            
        # add all values for just today to total. Total values include every day including today.
            
        containers['total_magnitude'] += containers['today_total_magnitude']
        containers['magnitude_scores'] += containers['today_magnitude_scores']
        containers['sentiment_scores'] += containers['today_sentiment_scores']
        
        for i in range(len(containers['sentiment_scores'])):
            magnitude = containers['magnitude_scores'][i] / containers['total_magnitude']
            sentiment = containers['sentiment_scores'][i] * magnitude
            results['total_sentiment'] += sentiment
            
        return results
    
    
    def get_press_releases(self):
        ticker = self.ticker
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        press_releases_today = 0
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            browser = webdriver.Chrome(options=options)
            browser.get(f'https://www.benzinga.com/stock-articles/{ticker}/press-releases')
            press_releases = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="benzinga-content-area"]/div/div/div/div[1]/div[1]'))).text
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
        
        except Exception as e:
            print(e)
        
        return press_releases_today
        
        
    def get_insider_trading(self):
        ticker = self.ticker
        insider_trades = 0
    
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            browser = webdriver.Chrome(options=options)
            browser.get(f'https://finviz.com/quote.ashx?t={ticker}')
            insider_trading = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/table[3]/tbody/tr[12]/td/table/tbody'))).text.split('\n')
            browser.quit()
            
            for filing in insider_trading:
                if 'Buy' in filing:
                    insider_trades += 1
                    
        except Exception as e:
            print(e)
        
        return insider_trades
    
    
    def get_analyst_ratings(self):
        ticker = self.ticker
        upgrades = 0
        downgrades = 0
        response = {}
        
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            browser = webdriver.Chrome(options=options)
            browser.get(f'https://www.benzinga.com/stock/{ticker}')
            analyst_ratings = WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="benzinga-main"]/div[2]/div[2]/div[1]/div/div[5]/div/div/table[2]/tbody'))).text
            analyst_ratings = analyst_ratings.split('\n')
            browser.quit()
    
            for rating in analyst_ratings:
                rating = rating.split()
                if 'Upgrades' in rating:
                    upgrades += 1
                elif 'Downgrades' in rating:
                    downgrades += 1
            
        except Exception as e:
            print(e)
        
        response['upgrades'] = upgrades
        response['downgrades'] = downgrades
        
        return response
        
        
    def get_quiver_data(self):
        ticker = self.ticker
        response = {}
        month_ago = (dt.datetime.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
        
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
        except:
            pass
        
        response['house_buys'] = house_buys
        response['house_sales'] = house_sales
        
        return response

    
if __name__ == '__main__':
    
    s = Sentiment('AAPL')
    results = s.get_analyst_ratings()
    print('\n\n LAST LINE:', results)
    




