import React, {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
const TradingView = window.TradingView;

const Search = () => {
  const [ticker, setTicker] = useState('');
  const [articles, setArticles] = useState({});
  const [news, setNews] = useState({});
  const [stocktwits, setStocktwits] = useState({});
  const [pressReleases, setPressRelease] = useState({});
  const [insiderTrades, setInsiderTrades] = useState();
  const [analystRatings, setAnalystRatings] = useState({});
  const [quiverData, setQuiverData] = useState({});
  const [error, setError] = useState(false);


  // This code creates a TradingViews object which is a class imported with a script tag
  // from the internet. The script tag is in the root index.html file and is imported into
  // this react component at the top.

  const tradingViewSetup = () => {
    new TradingView.widget(
      {
      "width": 1000,
      "height": 600,
      "symbol": `${ticker}`,
      "interval": "D",
      "timezone": "Etc/UTC",
      "theme": "dark",
      "style": "1",
      "locale": "en",
      "toolbar_bg": "#f1f3f6",
      "enable_publishing": false,
      "allow_symbol_change": true,
      "container_id": "tradingview_ae533"
      }
    )
  }
  useEffect(() => {
    tradingViewSetup();
  },[]);

  // when a user types letteres into the input, they are automatically converted
  // to uppercase b/c all tickers are always uppercase.

  const onChange = (e) => {
    setTicker(e.target.value.toUpperCase());
  }

  // const getCompany = async () => {
  //   const response = await fetch(`/search/company/${ticker}`);
  //   const parseRes = await response.json();
  //   setCompany(parseRes);
  //   console.log('company', company);
  // }

  const getNews = async () => {
    const response = await fetch(`/search/news/${ticker}`);
    const parseRes = await response.json();
    // console.log(parseRes);
    setNews(parseRes);
    console.log('news', parseRes);
  }

  const getArticles = async () => {

    const response = await fetch(`/search/articles/${ticker}`);
    const parseRes = await response.json();
    setArticles(parseRes);
    console.log(parseRes);
  }

  const getStocktwits = async () => {
    const response = await fetch(`/search/stocktwits/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
    setStocktwits(parseRes);
  }

  const getPressRelease = async () => {
    const response = await fetch(`/search/press-releases/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
    setPressRelease(parseRes);
  }

  const getInsiderTrading = async () => {
    const response = await fetch(`/search/insider-trading/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
    setInsiderTrades(parseRes);
  }

  const getAnalystRatings = async () => {
    const response = await fetch(`/search/analyst-ratings/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
    setAnalystRatings(parseRes);
  }

  const getQuiverQuant = async () => {
    const response = await fetch(`/search/quiver-quant/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
    setQuiverData(parseRes);
    
  }

  const onSubmit = async (e) => {
    e.preventDefault()

    getNews()
    getArticles()
    getStocktwits()
    getPressRelease()
    getInsiderTrading()
    getAnalystRatings()
    getQuiverQuant()
  }

  const makeArticle = (article) => {
    return <>
      <h2>{article.title}</h2>
      <h3>{article.description}</h3>
      <p>{article.content}</p>
      <a href={article.url} target='_blank'>continue reading</a>
      <hr />
    </>
  }

  return <>
  <h1 id='title'>Rando-Trader</h1>

    <nav>
      <ul>
        <li><Link to='/'><h1>Home</h1></Link></li>
        <li><Link to='/search'><h1>Search</h1></Link></li>
      </ul>
    </nav>

  {/* form for the user to enter a ticker */}

  <form onSubmit={onSubmit}>
    <input value={ticker} onChange={onChange} ></input>
    <button type='submit'>Submit</button>
  </form>

  <h1>{articles['company'] ? articles['company'] : ''}</h1>

  <table>
    <tbody>
      <tr>
        <td>Articles Today</td>
        <td>Today's Sentiment</td>
        <td>Total Sentiment</td>
      </tr>
      <tr>
        <td>{news['articles_today'] ? news['articles_today'] : 0}</td>
        <td>{news['today_total_sentiment'] ? news['today_total_sentiment'] : 0}</td>
        <td>{news['total_sentiment'] ? news['total_sentiment'] : 0}</td>
      </tr>
      <tr>
        <td>Stocktwits Messages Today</td>
        <td>Today's Sentiment</td>
        <td>Total Sentiment</td>
      </tr>
      <tr>
        <td>{stocktwits['articles_today'] ? stocktwits['articles_today'] : 0}</td>
        <td>{stocktwits['today_total_sentiment'] ? stocktwits['today_total_sentiment'] : 0}</td>
        <td>{stocktwits['total_sentiment'] ? stocktwits['total_sentiment'] : 0}</td>
      </tr>
    </tbody>
  </table>

    {/* divs for the trading view widget */}

    <div class="tradingview-widget-container">
      <div id="tradingview_ae533"></div>
    </div>

    <table>
    <tbody>
      <tr>
        <td>Insider Trading</td>
        <td>Press Releases</td>
        <td>Analyst Upgrades</td>
        <td>Analyst Downgrades</td>
      </tr>
      <tr>
        <td>{insiderTrades ? insiderTrades.length : 0}</td>
        <td>{pressReleases['press_releases'] ? pressReleases['press_releases'] : 0}</td>
        <td>{analystRatings['upgrades'] ? analystRatings['upgrades'] : 0}</td>
        <td>{analystRatings['downgrades'] ? analystRatings['downgrades'] : 0}</td>
      </tr>
      <tr>
        <td>Government Contracts</td>
        <td>Corporate Lobbying</td>
        <td>Congress Buys</td>
        <td>Congress Sells</td>
      </tr>
      <tr>
        <td>{quiverData['contracts'] ? quiverData['contracts'] : 0}</td>
        <td>{quiverData['lobbying'] ? quiverData['lobbying'] : 0}</td>
        <td>{quiverData['congress_buys'] ? quiverData['congress_buys'] : 0}</td>
        <td>{quiverData['congress_sales'] ? quiverData['congress_sales'] : 0}</td>
      </tr>
      <tr>
        <td>House Buys</td>
        <td>House Sells</td>
        <td>Senate Buys</td>
        <td>Senate Sells</td>
      </tr>
      <tr>
        <td>{quiverData['house_buys'] ? quiverData['house_buys'] : 0}</td>
        <td>{quiverData['house_sales'] ? quiverData['house_sales'] : 0}</td>
        <td>{quiverData['senate_buys'] ? quiverData['senate_buys'] : 0}</td>
        <td>{quiverData['senate_sales'] ? quiverData['senate_sales'] : 0}</td>
      </tr>
    </tbody>
  </table>

  <div>
    <h1>News</h1>
    {articles['articles'] && articles['articles'].map(makeArticle)}
  </div>
  </>


}

export default Search;