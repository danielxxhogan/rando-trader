const router = require('express').Router();
const fetch = require('node-fetch');

router.get('/premarket-gainers', async (req, res) => {
  try {
    // res.json('hi');
    console.log('here');
    const response = await fetch('https://localhost:3002/premarket-gainers');
    console.log('here');
    console.log(response);
    res.json(response);

    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;