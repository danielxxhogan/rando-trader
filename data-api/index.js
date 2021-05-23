const express = require('express');
const pool = require('./db');
const cors = require('cors');

const app = express();
app.use(cors());

PORT = process.env.PORT || 3002;

// *****************************************************************************
app.get('/premarket-gainers', async (req, res) => {

  // this endpoint queries the database for all the contents of the premarket_gainers table

  try {
    const response = await pool.query('select * from premarket_gainers')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/premarket-losers', async (req, res) => {

  // this endpoint queries the database for all the contents of the premarket_losers table

  try {
    const response = await pool.query('select * from premarket_losers')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/most-active', async (req, res) => {

  // this endpoint queries the database for all the contents of the most_active table

  try {
    const response = await pool.query('select * from most_active')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/insider-trading', async (req, res) => {

  // this endpoint queries the database for all the contents of the insider_trading table

  try {
    const response = await pool.query('select * from insider_trading')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/short-interest', async (req, res) => {

  // this endpoint queries the database for all the contents of the short_interest table

  try {
    const response = await pool.query('select * from short_interest')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/contracts', async (req, res) => {

  // this endpoint queries the database for all the contents of the contracts table

  try {
    const response = await pool.query('select * from contracts')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/lobbying', async (req, res) => {

  // this endpoint queries the database for all the contents of the lobbying table

  try {
    const response = await pool.query('select * from lobbying')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/congress', async (req, res) => {

  // this endpoint queries the database for all the contents of the congress table

  try {
    const response = await pool.query('select * from congress')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/senate', async (req, res) => {

  // this endpoint queries the database for all the contents of the senate table

  try {
    const response = await pool.query('select * from senate')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})

app.get('/house', async (req, res) => {

  // this endpoint queries the database for all the contents of the house table

  try {
    const response = await pool.query('select * from house')
    res.json(response.rows);

  } catch (err) {
    console.log(err.message);
    res.status(500).json('data Server Error');
  }
})



app.get('*', (req, res) => {
  res.status(404).send('Thats not a recognized endpoint');
})


app.listen(PORT, () => {
  console.log('Server started on port', PORT);
});
