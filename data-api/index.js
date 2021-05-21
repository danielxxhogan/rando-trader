const express = require('express');
const pool = require('db');

const app = express();

PORT = process.env.PORT || 3002;

// *****************************************************************************
app.get('/premarket-gainers', async (res, req) => {

  // this endpoint queries the database for all the contents of the premarket_gainers table

  try {
    const response = await pool.query('select * from premarket_gainers')
    console.log(response);
    res.json(response);

  } catch (err) {
    console.log(err.message);
  }
})

app.get('*', (req, res) => {
  res.status(404).send('Thats not a recognized endpoint');
})


app.listen(PORT, () => {
  console.log('Server started on port', PORT);
});