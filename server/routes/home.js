const router = require('express').Router();
const fetch = require('node-fetch');
const request = require('request');

router.get('/premarket-gainers', async (req, res) => {
  try {
    // res.json('hi');
    console.log('here');
    // const response = await fetch('https://localhost:3002/premarket-gainers');
    const response = request('http://localhost:3002/premarket-gainers', (err, reqres) => {
      if (err) return console.error(err.message);

      console.log(reqres.body);
      res.json(reqres.body)

    });



    // console.log('here');
    // console.log(response);
    // res.json(response);

    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;