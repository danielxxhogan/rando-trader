const router = require('express').Router();

router.get('/:ticker', (req, res) => {
  try {
    
  } catch (err) {
    console.log(err.message);
    res.status(500).json('Server Error');
  }
})

module.exports = router;