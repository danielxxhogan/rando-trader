const router = require('express').Router();
const request = require('request');

router.get('/premarket-gainers', async (req, res) => {
  try {
    request('http://54.157.199.149:3002/premarket-gainers', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

router.get('/premarket-losers', async (req, res) => {
  try {
    request('http://54.157.199.149:3002/premarket-losers', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;