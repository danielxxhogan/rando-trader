const router = require('express').Router();
const request = require('request');

router.get('/premarket-gainers', async (req, res) => {
  try {
    // res.json('hi');
    console.log('here');
    // const response = await fetch('https://localhost:3002/premarket-gainers');
    const response = request('http://54.157.199.149:3002/premarket-gainers', (err, reqres) => {
      if (err) return console.error(err.message);

      console.log(reqres.body);
      res.json(reqres.body)

    });

    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;