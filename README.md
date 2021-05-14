# rando-trader
Full stack trading platform, has a python automated backend for collecting data and trading bots, and a react/express frontend dashboard.

Rando-Trader is a full stack trading platform I built for myself. There are three main parts:

The first part is a series of python scripts that use a combination of web scraping and api requests to collect financial data and
store it to a postgres db hosted on RDS. The scripts are executed on an ec2 instance using cronjob and the db is updated periodically.

The second part is a series of trading algorithms that retrieve universes of stocks and other relevant data from the db and place trades
accordingly by connecting to the broker api. The broker I use is Alpaca.

The third part is the Rando-Trader dashboard which is a React/Express application hosted on Digital Ocean and accessible at rando-trader.com.
When the site is visited, data from the db is retrieved and displayed in the browser, and it also supports search functionality.
