import React, {useState, useEffect} from 'react';
import {Link} from 'react-router-dom';
const TradingView = window.TradingView;

const Search = () => {
  const [ticker, setTicker] = useState('GME');
  const [news, setNews] = useState({});
  const [stocktwits, setStocktwits] = useState({});
  const [pressReleases, setPressRelease] = useState();
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

  const getNews = async () => {
    const response = await fetch(`/search/news/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
  }

  const getStocktwits = async () => {
    const response = await fetch(`/search/stocktwits/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
  }

  const getPressRelease = async () => {
    const response = await fetch(`/search/press-releases/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
  }

  const getInsiderTrading = async () => {
    const response = await fetch(`/search/insider-trading/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
  }

  const getAnalystRatings = async () => {
    const response = await fetch(`/search/analyst-ratings/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
  }

  const getQuiverQuant = async () => {
    const response = await fetch(`/search/quiver-quant/${ticker}`);
    const parseRes = await response.json();
    console.log(parseRes);
  }

  const onSubmit = async (e) => {
    e.preventDefault()

    getNews()
    getStocktwits()
    getPressRelease()
    getInsiderTrading()
    getAnalystRatings()
    getQuiverQuant()
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

    {/* divs for the trading view widget */}

    <div class="tradingview-widget-container">
      <div id="tradingview_ae533"></div>
    </div>
  </>


}

export default Search;