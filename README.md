# Rando-Trader

Rando-Trader is a full stack trading web app. There are three main parts:

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

pip3 install -r requirements.txt  

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

----- install talib -----

sudo apt update

sudo apt install build-essential

sudo apt-get install manpages-dev

gcc --version



unzip mrjbq7-ta-lib-TA_Lib-0.4.20-0-g95b4f80.zip

cd mrjbq7-ta-lib-95b4f80

sudo apt-get install python3-dev

sudo python3 setup.py install

<br />
<br />

----- setup cronjob -----

sudo service cron start

crontab -e  


\# GET LATEST INSIDER BUYS AND APPEND TO INSIDER_TRADING TABLE<br />
0 1 * * * cd ~/rando-trader/data-scripts && python3 insider_trading.py<br />


\# GET ALL CURRENT DATA FROM ALL QUIVER QUANT API ENDPOINTS AND UPDATE CORRESPONDING TABLES<br />
5 1 * * * cd ~/rando-trader/data-scripts && python3 get_quiver_data.py<br />


\# GET ALL STOCKS WITH THE HIGHEST SHORT INTEREST<br />
10 1 * * * cd ~rando-trader/data-scripts && python3 short_interest.py<br />


\# GET AM EARNINGS IN THE MORNING, GET PM EARNINGS IN THE AFTERNOON, GET EARNINGS SENTIMENT SHORTLY BEFORE MARKET CLOSE<br />
25 6 * * 1-5 cd ~/rando-trader/data-scripts/earnings && python3 morning_earnings_b.py<br />
0 17 * * 1-5 cd ~/rando-trader/data-scripts/earnings && python3 after_market_earnings_b.py<br />
55 12 * * 1-5 cd ~/rando-trader/data-scripts/earnings && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 earnings_sentiment.py<br />


\# GET ALL TICKERS WITH M&A ANNOUNCEMENTS, PASS EACH TO SENTIMENTY.PY AND STORE RESULTS TO MA_SENTIMENT TABLE<br />
0 8 * * * cd ~/rando-trader/data-scripts/ma && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 ma.py<br />


\# GET ALL TICKERS WITH ANALYST UPGRAGES OR DOWNGRADES FOR THE CURRENT DAY<br />
10 8 * * * cd ~/rando-trader/data-scripts/ratings && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 ratings.py<br />


\# GET PREMARKET GAINERS, LOSERS, AND MOST ACTIVE<br />
20 6 * * 1-5 cd ~/rando-trader/data-scripts/premarket-movers && python3 premarket_movers.py<br />
21 6 * * 1-5 cd ~/rando-trader/data-scripts/premarket-movers && python3 most_active.py<br />
22 6 * * 1-5 cd ~/rando-trader/data-scripts/premarket-movers && export GOOGLE_APPLICATION_CREDENTIALS=credentials.json && python3 premarket_sentiment.py<br />


\# STOCK UNIVERSES<br />
00 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 broad_universe.py<br />
10 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 heavily_traded.py.py<br />
20 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 high_rvol.py.py<br />
30 2 * * 1-5 cd ~/rando-trader/data-scripts/screeners && python3 high_score.py.py<br />

<br />
<br />
<br />
<br />

# Instructions on setting up ec2 instance for sentiment-api

<br />

----- commands to run a production flask server -----

export FLASK_APP=index.py

export FLASK_ENV=development

flask run

<br />
<br />

# Instructions on setting up ec2 instance for data-api

<br />

----- install node/npm, dependancies -----

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash

nvm install node

npm i





















