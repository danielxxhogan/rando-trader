const router = require('express').Router();
const fetch = require('node-fetch');
const NewsAPI = require('newsapi');
require('dotenv').config()

const SENTIMENT_API_URL = 'http://localhost:5000';
const DATA_API_URL = 'http://54.157.199.149:3002';

const newsapi = new NewsAPI(process.env.NEWS_API_KEY);

// *****************************************************************************
router.get('/company/:ticker', async (req, res) => {
  try {
    const ticker = req.params.ticker.toUpperCase();

    const response = await fetch('https://www.alphavantage.co/query?' +
                                 `function=OVERVIEW&symbol=${ticker}&` +
                                 `apikey=${process.env.ALPHA_VANTAGE_API_KEY}`)

    const parseRes = await response.json()
    const company = parseRes.Name;
    res.json(company);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/news/:ticker', async (req, res) => {
  try {
    const ticker = req.params.ticker.toUpperCase();
    const response = await fetch(SENTIMENT_API_URL + `/news/${ticker}`);
    const parseRes = await response.json();

    res.json(parseRes);
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/articles/:ticker', async (req, res) => {
  try {
    const response = {};

    const ticker = req.params.ticker.toUpperCase();
    const companyResponse = await fetch('https://www.alphavantage.co/query?' +
                                        `function=OVERVIEW&symbol=${ticker}&` +
                                        `apikey=${process.env.ALPHA_VANTAGE_API_KEY}`);

    const parseCompany = await companyResponse.json();
    const company = parseCompany.Name;
    response['company'] = company;

    const today = new Date();
    const currentYear = today.getFullYear()
    var currentMonth = today.getMonth()   // gets month index value
    currentMonth = currentMonth + 1;
    const currentDay = today.getDate()

    var startMonth = null;
    var startYear = null;
    var startDay = null;

    if (currentMonth == 1) {
      startMonth = 12
      startYear = currentYear - 1;
    }
    else {
      startMonth = currentMonth - 1;
      startYear = currentYear;
    }

    if (currentDay >= 28) {
       startDay = 28;
    }
    else {
      startDay = currentDay;
    }

    const fromString = `${startYear}-${startMonth}-${startDay}`;
    const toString = `${currentYear}-${currentMonth}-${currentDay}`;

    const newsResponse = await newsapi.v2.everything({
      q: company,
      from: fromString,
      to: toString,
      language: 'en',
      sortBy: 'relevancy',
      page: 2
      })

    const articles = newsResponse.articles;
    response['articles'] = articles;
    res.json(response);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/stocktwits/:ticker', async (req, res) => {
  try {
    const ticker = req.params.ticker.toUpperCase();
    const response = await fetch(SENTIMENT_API_URL + `/stocktwits/${ticker}`);
    const parseRes = await response.json();

    res.json(parseRes);
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/press-releases/:ticker', async (req, res) => {
  try {
    const ticker = req.params.ticker.toUpperCase();
    const response = await fetch(SENTIMENT_API_URL + `/press-releases/${ticker}`);
    const parseRes = await response.json();

    res.json(parseRes);
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/insider-trading/:ticker', async (req, res) => {

  // this endpoint takes requests from the client for insider trading data on a
  // specific ticker. It then sends a request to the data-api on ec2 which queries
  // the db on rds.

  try {
    const ticker = req.params.ticker.toUpperCase();
    const response = await fetch(DATA_API_URL + `/insider-trading-ticker/${ticker}`);
    const parseRes = await response.json();

    res.json(parseRes);
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/analyst-ratings/:ticker', async (req, res) => {
  try {
    const ticker = req.params.ticker.toUpperCase();
    const response = await fetch(SENTIMENT_API_URL + `/analyst-ratings/${ticker}`);
    const parseRes = await response.json();

    res.json(parseRes);
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/quiver-quant/:ticker', async (req, res) => {
  try {
    const ticker = req.params.ticker.toUpperCase();
    const response = await fetch(SENTIMENT_API_URL + `/quiver-quant/${ticker}`);
    const parseRes = await response.json();

    res.json(parseRes);
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;