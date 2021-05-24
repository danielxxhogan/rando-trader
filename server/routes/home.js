const router = require('express').Router();
const request = require('request');

const BASE_URL = 'http://54.157.199.149:3002';


// *****************************************************************************
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

// *****************************************************************************
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

// *****************************************************************************
router.get('/most-active', async (req, res) => {
  try {
    request('http://54.157.199.149:3002/most-active', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/insider-trading', async (req, res) => {
  try {
    request('http://54.157.199.149:3002/insider-trading', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/short-interest', async (req, res) => {
  try {
    request('http://54.157.199.149:3002/short-interest', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/contracts', async (req, res) => {
  try {
    request(BASE_URL + '/contracts', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/lobbying', async (req, res) => {
  try {
    request(BASE_URL + '/lobbying', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/congress', async (req, res) => {
  try {
    request(BASE_URL + '/congress', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/senate', async (req, res) => {
  try {
    request(BASE_URL + '/senate', (err, reqres) => {
      if (err) return console.error(err.message);

      const parseRes = JSON.parse(reqres.body);
      res.json(parseRes);
    });

  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

// *****************************************************************************
router.get('/house', async (req, res) => {
  try {
    request(BASE_URL + '/house', (err, reqres) => {
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