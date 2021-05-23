import React, { useEffect, useState } from 'react';

const Home = () => {
  const [premarketGainers, setPremarketGainers] = useState();
  const [premarketLosers, setPremarketLosers] = useState();
  const [mostActive, setMostActive] = useState();
  const [insiderTrading, setInsiderTrading] = useState();
  const [shortInterest, setShortInterest] = useState();
  const [contracts, setContracts] = useState();
  const [lobbying, setLobbying] = useState();
  const [congress, setCongress] = useState();
  const [senate, setSenate] = useState();
  const [house, setHouse] = useState();

  const getPremarketGainers = async () => {
    const response = await fetch('/home/premarket-gainers');
    const parseRes = await response.json();
    setPremarketGainers(parseRes);
  }
  useEffect(() => { getPremarketGainers(); },[])

  const getPremarketLosers = async () => {
    const response = await fetch('/home/premarket-losers');
    const parseRes = await response.json();
    setPremarketLosers(parseRes);
  }
  useEffect(() => { getPremarketLosers(); },[])

  const getMostActive = async () => {
    const response = await fetch('/home/most-active');
    const parseRes = await response.json();
    setMostActive(parseRes);
  }
  useEffect(() => { getMostActive(); },[])

  const getInsiderTrading = async () => {
    const response = await fetch('/home/insider-trading');
    const parseRes = await response.json();
    setInsiderTrading(parseRes);
  }
  useEffect(() => { getInsiderTrading(); },[])

  const getShortInterest = async () => {
    const response = await fetch('/home/short-interest');
    const parseRes = await response.json();
    setShortInterest(parseRes);
  }
  useEffect(() => { getShortInterest(); },[])

  const getContracts = async () => {
    const response = await fetch('/home/contracts');
    const parseRes = await response.json();
    setContracts(parseRes);
  }
  useEffect(() => { getContracts(); },[])

  const getLobbying = async () => {
    const response = await fetch('/home/lobbying');
    const parseRes = await response.json();
    setLobbying(parseRes);
  }
  useEffect(() => { getLobbying(); },[])

  const getCongress = async () => {
    const response = await fetch('/home/congress');
    const parseRes = await response.json();
    setCongress(parseRes);
  }
  useEffect(() => { getCongress(); },[])

  const getSenate = async () => {
    const response = await fetch('/home/senate');
    const parseRes = await response.json();
    setSenate(parseRes);
  }
  useEffect(() => { getSenate(); },[])

  const getHouse = async () => {
    const response = await fetch('/home/house');
    const parseRes = await response.json();
    setHouse(parseRes);
  }
  useEffect(() => { getHouse(); },[])




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
    <h1 id='title'>Rando-Trader</h1>

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

    <hr />
    <h2>Government Contracts</h2>
    <table>
    {contracts && contracts.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Corporate Lobbying</h2>
    <table>
    {lobbying && lobbying.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Congress Trades</h2>
    <table>
    {congress && congress.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>Senate Trades</h2>
    <table>
    {senate && senate.map(row => { return makeTableRow(row) })}
    </table>

    <hr />
    <h2>House Trades</h2>
    <table>
    {house && house.map(row => { return makeTableRow(row) })}
    </table>

  </>

}

export default Home;