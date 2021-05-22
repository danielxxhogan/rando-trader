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
    console.log(response.rows);
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
    console.log(response.rows);
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
