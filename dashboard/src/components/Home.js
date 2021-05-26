import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

const useStyles = makeStyles({
  table: {
    backgroundColor: '#275606',
    color: 'white',
  },
  tr: {
    color: 'white'
  },
  td: {
    color: 'white',
    padding: '1rem',
  }
});


const Home = () => {
  const classes = useStyles();
  
  // state variables for holding database data
  // *****************************************************************************
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


  // get data from all tables in the database
  // *****************************************************************************
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


  // functions for creating table rows for each table
  // *****************************************************************************
  const makePremarket = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.company}</TableCell>
          <TableCell className={classes.td} align="right">{row.price}</TableCell>
          <TableCell className={classes.td} align="right">{row.change}</TableCell>
          <TableCell className={classes.td} align="right">{row.volume}</TableCell>
        </TableRow>
      </tr>
    </>
  }

  const makeInsider = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.filing_date}</TableCell>
          <TableCell className={classes.td} align="right">{row.trade_date}</TableCell>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.company}</TableCell>
          <TableCell className={classes.td} align="right">{row.insider}</TableCell>
          <TableCell className={classes.td} align="right">{row.title}</TableCell>
          <TableCell className={classes.td} align="right">{row.price}</TableCell>
          <TableCell className={classes.td} align="right">{row.qty}</TableCell>
          <TableCell className={classes.td} align="right">{row.owned}</TableCell>
          <TableCell className={classes.td} align="right">{row.change}</TableCell>
          <TableCell className={classes.td} align="right">{row.value}</TableCell>
        </TableRow>
      </tr>
    </>
  }

  const makeShortInterest = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.company}</TableCell>
          <TableCell className={classes.td} align="right">{row.price}</TableCell>
          <TableCell className={classes.td} align="right">{row.short_interest}</TableCell>
          <TableCell className={classes.td} align="right">{row.float}</TableCell>
          <TableCell className={classes.td} align="right">{row.float_shorted}</TableCell>
        </TableRow>
      </tr>
    </>
  }

  const makeContracts = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.date}</TableCell>
          <TableCell className={classes.td} align="right">{row.agency}</TableCell>
          <TableCell className={classes.td} align="right">{row.amount}</TableCell>
          <TableCell className={classes.td} align="right">{row.description}</TableCell>
      </TableRow>
      </tr>
    </>
  }

  const makeLobbying = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.date}</TableCell>
          <TableCell className={classes.td} align="right">{row.amount}</TableCell>
          <TableCell className={classes.td} align="right">{row.client}</TableCell>
          <TableCell className={classes.td} align="right">{row.issue}</TableCell>
        </TableRow>
      </tr>
    </>
  }

  const makeCongress = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.report_date}</TableCell>
          <TableCell className={classes.td} align="right">{row.transaction_date}</TableCell>
          <TableCell className={classes.td} align="right">{row.amount}</TableCell>
          <TableCell className={classes.td} align="right">{row.transaction}</TableCell>
          <TableCell className={classes.td} align="right">{row.representative}</TableCell>
          <TableCell className={classes.td} align="right">{row.house}</TableCell>
        </TableRow>
      </tr>
    </>
  }

  const makeSenate = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.date}</TableCell>
          <TableCell className={classes.td} align="right">{row.amount}</TableCell>
          <TableCell className={classes.td} align="right">{row.transaction}</TableCell>
          <TableCell className={classes.td} align="right">{row.senator}</TableCell>
        </TableRow>
      </tr>
    </>
  }

  const makeHouse = (row) => {
    return <>
      <tr>
        <TableRow className={classes.tr}>
          <TableCell className={classes.td} align="right">{row.ticker}</TableCell>
          <TableCell className={classes.td} align="right">{row.date}</TableCell>
          <TableCell className={classes.td} align="right">{row.amount}</TableCell>
          <TableCell className={classes.td} align="right">{row.transaction}</TableCell>
          <TableCell className={classes.td} align="right">{row.representative}</TableCell>
        </TableRow>
      </tr>
    </>
  }


  return <>
    <h1 id='title'>Rando-Trader</h1>

    <h1>Home</h1>

    <h2>Premarket Gainers</h2>
    <div class='table'>
    <TableContainer component={Paper}>
      <Table className={classes.table} aria-label="simple table">
        <TableHead>
          <tr>
            <TableRow>
              <TableCell className={classes.td}>Ticker</TableCell>
              <TableCell className={classes.td}>Company</TableCell>
              <TableCell className={classes.td}>Price</TableCell>
              <TableCell className={classes.td}>Change</TableCell>
              <TableCell className={classes.td}>Volume</TableCell>
            </TableRow>
          </tr>
        </TableHead>
        <TableBody>
          {premarketGainers && premarketGainers.map(row => { return makePremarket(row) })}
        </TableBody>
      </Table>
    </TableContainer>
    </div>


    <hr />
    <h2>Premarket Losers</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {premarketLosers && premarketLosers.map(row => { return makePremarket(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Most Active</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {mostActive && mostActive.map(row => { return makePremarket(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Insider Trading</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {insiderTrading && insiderTrading.map(row => { return makeInsider(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Short Interest</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {shortInterest && shortInterest.map(row => { return makeShortInterest(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Government Contracts</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {contracts && contracts.map(row => { return makeContracts(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Corporate Lobbying</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {lobbying && lobbying.map(row => { return makeLobbying(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Congress Trades</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {congress && congress.map(row => { return makeCongress(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>Senate Trades</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {senate && senate.map(row => { return makeSenate(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


    <hr />
    <h2>House Trades</h2>
    <div class='table'>
      <TableContainer component={Paper}>
        <Table className={classes.table} aria-label="simple table">
          <TableBody>
            {house && house.map(row => { return makeHouse(row) })}
          </TableBody>
        </Table>
      </TableContainer>
    </div>


  </>
}

export default Home;