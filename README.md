# rando-trader
Full stack trading platform, has a python automated backend for collecting data and trading bots, and a react/express frontend dashboard.

Rando-Trader is a full stack trading platform I built for myself. There are three main parts:

The first part is a series of python scripts that use a combination of web scraping and api requests to collect financial data and
store it to a postgres db hosted on RDS. The scripts are executed on an ec2 instance using cronjob and the db is updated periodically.

The second part is a series of trading algorithms that retrieve universes of stocks and other relevant data from the db and place trades
accordingly by connecting to the broker api. The broker I use is Alpaca.

The third part is the Rando-Trader dashboard which is a React/Express application hosted on Digital Ocean and accessible at rando-trader.com.
When the site is visited, data from the db is retrieved and displayed in the browser, and it also supports search functionality.  


<br />
<br />

# Instructions on setting up ec2 instance for data-scripts and bots.

Create new instance and ssh into it.  

<br />

----- install git, get rando-trader, set date -----  


Install git:  sudo apt-get install git

git clone https://github.com/rando-mane/rando-trader.git && cd rando-trader

sudo timedatectl set-timezone America/Los_Angeles

copy over all config, credentials, and env files  

<br />
<br />

----- Get distutils and pip and install all requirements -----  

sudo apt-get install python3-distutils

python3 get-pip.py

export PATH="$PATH:/home/ubuntu/.local/bin"

source ~/.profile

sudo pip3 install -r requirements.txt  

<br />
<br />

----- install chrome, chromedriver -----  

wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

sudo apt install ./google-chrome-stable_current_amd64.deb


sudo wget https://chromedriver.storage.googleapis.com/90.0.4430.24/chromedriver_linux64.zip

sudo apt install unzip

sudo unzip chromedriver_linux64.zip

sudo mv chromedriver /usr/bin/chromedriver  

<br />
<br />

----- setup cronjob -----  

sudo service cron start

crontab -e  


\# GET LATEST INSIDER BUYS AND APPEND TO INSIDER_TRADING TABLE<br />
0 1 * * * cd ~/rando-trader/data-scripts && python3 insider_trading.py  


\# GET ALL CURRENT DATA FROM ALL QUIVER QUANT API ENDPOINTS AND UPDATE CORRESPONDING TABLES<br />
5 1 * * * cd ~/rando-trader/data-scripts && python3 get_quiver_data.py  


\# GET ALL STOCKS WITH THE HIGHEST SHORT INTEREST<br />
10 1 * * * cd ~rando-trader/data-scripts && python3 short_interest.py  


\# GET AM EARNINGS IN THE MORNING, GET PM EARNINGS IN THE AFTERNOON, GET EARNINGS SENTIMENT SHORTLY BEFORE MARKET CLOSE<br />
25 6 * * 1-5 cd ~/rando-trader/data-scripts/earnings && python3 morning_earnings_b.py
0 17 * * 1-5 cd ~/rando-trader/data-scripts/earnings && python3 after_market_earnings_b.py
55 12 * * 1-5 cd ~/rando-trader/data-scripts/earnings && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 earnings_sentiment.py  


\# GET ALL TICKERS WITH M&A ANNOUNCEMENTS, PASS EACH TO SENTIMENTY.PY AND STORE RESULTS TO MA_SENTIMENT TABLE<br />
0 8 * * * cd ~/rando-trader/data-scripts/ma && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 ma.py  


\# GET ALL TICKERS WITH ANALYST UPGRAGES OR DOWNGRADES FOR THE CURRENT DAY<br />
10 8 * * * cd ~/rando-trader/data-scripts/ratings && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 ratings.py  


\# GET PREMARKET GAINERS, LOSERS, AND MOST ACTIVE<br />
20 6 * * 1-5 cd ~/rando-trader/data-scripts/premarket-movers && python3 premarket_movers.py
21 6 * * 1-5 cd ~/rando-trader/data-scripts/premarket-movers && python3 most_active.py
22 6 * * 1-5 cd ~/rando-trader/data-scripts/premarket-movers && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 premarket_sentiment.py  


\# STOCK UNIVERSES<br />
00 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 broad_universe.py
10 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 heavily_traded.py.py
20 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 high_rvol.py.py
30 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 high_score.py.py

