const router = require('express').Router();
const request = require('request');

router.get('/premarket-gainers', async (req, res) => {
  try {
    // res.json('hi');
    console.log('here');
    // const response = await fetch('https://localhost:3002/premarket-gainers');
    request('http://54.157.199.149:3002/premarket-gainers', (err, reqres) => {
      if (err) return console.error(err.message);

      // const parseRes = reqres.json();
      // console.log(parseRes);
      // console.log(parseRes.body);
      // console.log(typeof parseRes);

      console.log(typeof reqres);
      console.log(reqres);
      console.log(reqres.body);
      console.log(typeof reqres.body);
      res.json(reqres.body)

    });

    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;