import React, { useEffect, useState } from 'react';

const Home = () => {
  const [premarketGainers, setPremarketGainers] = useState();
  const [premarketLosers, setPremarketLosers] = useState();
  const [mostActive, setMostActive] = useState();
  const [insiderTrading, setInsiderTrading] = useState();
  const [shortInterest, setShortInterest] = useState();

  const getPremarketGainers = async () => {
    const response = await fetch('http://localhost:3004/home/premarket-gainers');
    const parseRes = await response.json();
    setPremarketGainers(parseRes);
  }
  useEffect(() => { getPremarketGainers(); },[])

  const getPremarketLosers = async () => {
    const response = await fetch('http://localhost:3004/home/premarket-losers');
    const parseRes = await response.json();
    setPremarketLosers(parseRes);
  }
  useEffect(() => { getPremarketLosers(); },[])

  const getMostActive = async () => {
    const response = await fetch('http://localhost:3004/home/most-active');
    const parseRes = await response.json();
    setMostActive(parseRes);
  }
  useEffect(() => { getMostActive(); },[])

  const getInsiderTrading = async () => {
    const response = await fetch('http://localhost:3004/home/insider-trading');
    const parseRes = await response.json();
    setInsiderTrading(parseRes);
  }
  useEffect(() => { getInsiderTrading(); },[])

  const getShortInterest = async () => {
    const response = await fetch('http://localhost:3004/home/short-interest');
    const parseRes = await response.json();
    setShortInterest(parseRes);
  }
  useEffect(() => { getShortInterest(); },[])




  const makeTableRow = (row) => {
    return <>
      <tr>
        <td>{row.ticker}</td>
        <td>{row.company}</td>
        <td>{row.price}</td>
        <td>{row.change}</td>
        <td>{row.volume}</td>
      </tr>
    </>
  }


  return <>
    <h1>Home</h1>

    <h2>Premarket Gainers</h2>
    <table>
      {premarketGainers && premarketGainers.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Premarket Losers</h2>
    <table>
    {premarketLosers && premarketLosers.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Most Active</h2>
    <table>
    {mostActive && mostActive.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Insider Trading</h2>
    <table>
    {insiderTrading && insiderTrading.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Short Interest</h2>
    <table>
    {shortInterest && shortInterest.map(row => { return makeTableRow(row) })}
    </table>
  </>

}

export default Home;