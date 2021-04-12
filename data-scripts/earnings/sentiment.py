import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from google.cloud import language_v1
import datetime as dt
import psycopg2

from config import *

def calculate_sentiment(ticker='FUV'):
    print(ticker)
    
    conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

    cursor = conn.cursor()
    
    client = language_v1.LanguageServiceClient()

    # GET ARTICLES FROM FINVIZ AND SPLIT BY ROW
    # *****************************************************************************
    articles_today = 0
    total_sentiment = 0.0
    today_total_sentiment = 0.0
    
    try:
        browser = webdriver.Chrome()
        browser.get(f'https://finviz.com/quote.ashx?t={ticker}')
        articles = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="news-table"]/tbody'))).text
        browser.quit()
        
        articles = articles.split('\n')
        
        total_magnitude = 0.0
        
        magnitude_scores = []
        sentiment_scores = []
        
        today_total_magnitude = 0.0
        
        today_magnitude_scores = []
        today_sentiment_scores = []
        
        day = 0
        
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
                    
            except:
                pass
            
        
        for i in range(len(today_sentiment_scores)):
            try:
                magnitude = today_magnitude_scores[i] / today_total_magnitude
                sentiment = today_sentiment_scores[i] * magnitude
                today_total_sentiment += sentiment
            except:
                pass
            
        total_magnitude += today_total_magnitude
        magnitude_scores += today_magnitude_scores
        sentiment_scores += today_sentiment_scores
        
        for i in range(len(sentiment_scores)):
            try:
                magnitude = magnitude_scores[i] / total_magnitude
                sentiment = sentiment_scores[i] * magnitude
                total_sentiment += sentiment
            except:
                pass
            
        print(f'articles today: {articles_today} \
                \ntodays sentiment: {today_total_sentiment} \
                \noverall sentiment: {total_sentiment}\n')
                
    except:
        pass
    
    
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
        
    print(f'messages today: {messages_today} \
            \ntodays sentiment: {today_total_sentiment_st} \
            \noverall sentiment: {total_sentiment_st}\n')
    
    
    # GET PRESS RELEASES FROM BENZINGA
    # *****************************************************************************
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    press_releases_today = 0
    
    try:
        browser = webdriver.Chrome()
        browser.get(f'https://www.benzinga.com/stock-articles/{ticker}/press-releases')
        press_releases = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="benzinga-content-area"]/div/div/div/div[1]/div[1]'))).text
        browser.quit()
        
        press_releases = press_releases.split('\n')
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
    
    
    # LOOP THROUGH PRESS_RELEASES AND GET ALL 
    # for i in range(100):
    #     try:
    #         browser = webdriver.Chrome()
    #         browser.get('https://www.benzinga.com/stock-articles/fb/press-releases')
    #         press_release = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="benzinga-content-area"]/div/div/div/div[1]/div[{i+1}]'))).text
    #         browser.quit()
            
    #         press_release = press_release.split('\n')
            
    #         for j in range(1, len(press_release), 2):
    #             print(press_release[j])
            
    #     except:
    #         break
    
    
    # GET QUIVER DATA FOR TICKER
    # *****************************************************************************
    month_ago = (dt.datetime.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
    
    QUIVER_URL = 'https://api.quiverquant.com/beta'
    
    headers = {'accept': 'application/json',
               'X-CSRFToken': 'TyTJwjuEC7VV7mOqZ622haRaaUr0x0Ng4nrwSRFKQs7vdoBcJlK9qjAS69ghzhFu',
               'Authorization': f'Token {QUIVER_API_KEY}'}
    
    # ----- contract -----
    r = requests.get(f'{QUIVER_URL}/historical/govcontractsall/{ticker}', headers=headers)
    contracts = r.json()
    
    num_contracts = 0
    for filing in contracts:
        if filing['Date'] > month_ago:        
            num_contracts += 1
            
    print(f'contracts: {num_contracts}')
    
    
    # ----- lobbying -----
    try:
        r = requests.get(f'{QUIVER_URL}/historical/lobbying/{ticker}', headers=headers)
        lobbying = r.json()
        
        num_lobbying = 0
        for filing in lobbying:
            if filing['Date'] > month_ago:        
                num_lobbying += 1
                
        print(f'lobbying: {num_lobbying}\n')
        
    except:
        pass
    
    
    # ----- congress -----
    r = requests.get(f'{QUIVER_URL}/historical/congresstrading/{ticker}', headers=headers)
    congress = r.json()
    
    congress_buys = 0
    congress_sales = 0
    
    for filing in congress:
        if filing['TransactionDate'] > month_ago and filing['Transaction'] == 'Purchase':
            congress_buys += 1
            
        elif filing['TransactionDate'] > month_ago and filing['Transaction'] == 'Sale':
            congress_sales += 1
            
    print(f'congress buys: {congress_buys}')
    print(f'congress sells: {congress_sales}')
            
            
    # ----- senate -----
    r = requests.get(f'{QUIVER_URL}/historical/senatetrading/{ticker}', headers=headers)
    senate = r.json()
    
    senate_buys = 0
    senate_sales = 0
    
    for filing in senate:
        if filing['Date'] > month_ago and filing['Transaction'] == 'Purchase':
            senate_buys += 1
            
        elif filing['Date'] > month_ago and filing['Transaction'] == 'Sale':
            senate_sales += 1
            
    print(f'senate buys: {senate_buys}')
    print(f'senate sells: {senate_sales}')
            
    
    # ----- house -----
    r = requests.get(f'{QUIVER_URL}/historical/housetrading/{ticker}', headers=headers)
    house = r.json()
    
    house_buys = 0
    house_sales = 0
    
    for filing in house:
        if filing['Date'] > month_ago and filing['Transaction'] == 'Purchase':
            house_buys += 1
            
        elif filing['Date'] > month_ago and filing['Transaction'] == 'Sale':
            house_sales += 1
            
    print(f'house buys: {house_buys}')
    print(f'house sells: {house_sales}\n')
    
    
    # GET INSIDER TRADING
    # *****************************************************************************
    month_ago = (dt.datetime.today() - dt.timedelta(days=30)).strftime('%Y-%m-%d')
    
    cursor.execute('select * from insider_trading')
    insider_trading = cursor.fetchall()
    
    num_insider_trades = 0
    for trade in insider_trading:
        if trade[1].strftime('%Y-%m-%d') > month_ago and trade[3] == ticker:
            num_insider_trades += 1
            
    print(f'insider trades: {num_insider_trades}\n')
            
    
    # GET ANALYST RATINGS FROM BENZINGA
    # *****************************************************************************
    upgrades = 0
    downgrades = 0
    
    try:
        browser = webdriver.Chrome()
        browser.get(f'https://www.benzinga.com/stock/{ticker}')
        analyst_ratings = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="benzinga-main"]/div[2]/div[2]/div[1]/div/div[5]/div/div/table[2]/tbody'))).text
        browser.quit()
        
        analyst_ratings = analyst_ratings.split('\n')
        
    
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
    
    
    conn.commit()

    cursor.close()
    conn.close()


if __name__ == '__main__':
    calculate_sentiment()