const express = require('express');

const app = express();

PORT = process.env.PORT || 3002;

app.get('*', (req, res) => {
  res.status(404).send('Thats not a recognized endpoint');
})


app.listen(PORT, () => {
  console.log('Server started on port', PORT);
});