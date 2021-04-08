const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());

PORT = process.env.PORT || 3002;


app.listen(PORT, () => {
  console.log('Server stared on port', PORT)
})