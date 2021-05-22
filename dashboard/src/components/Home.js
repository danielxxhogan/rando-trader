import React, { useEffect, useState } from 'react';

const Home = () => {
  const [premarketGainers, setPremarketGainers] = useState();

  const getPremarketGainers = async () => {
    const response = await fetch('http://localhost:3004/home/premarket-gainers');
    const parseRes = await response.json();
    console.log(parseRes);
    console.log(typeof parseRes);
    setPremarketGainers(parseRes);
  }
  useEffect(() => { getPremarketGainers(); })

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
    <h1>Hi</h1>

    <table>
      {premarketGainers && premarketGainers.map(row => { return makeTableRow(row) })}
    </table>
  </>

}

export default Home;