import React, { useEffect, useState } from 'react';

const Home = () => {
  const [premarketGainers, setPremarketGainers] = useState();

  const getPremarketGainers = async () => {
    const response = await fetch('http://localhost:3004/home/premarket-gainers');
    console.log(response);
    console.log(typeof response);

    const parseRes = await response.json();
    console.log(parseRes);
    // console.log(parseRes.body);
    console.log(typeof parseRes);

    const parseRes2 = JSON.stringify(parseRes)
    console.log(parseRes2);
    console.log(parseRes2.body);
    console.log(typeof parseRes2);

    // console.log(typeof parseRes);
    // parseRes = JSON.stringify(parseRes)
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