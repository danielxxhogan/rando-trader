const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());

PORT = process.env.PORT || 3004;

app.use('/home', require('./routes/home'))
app.use('/search', require('./routes/search'));


// app.get('*', (req, res) => {
//   res.sendFile(path.join(__dirname, './client/build/index.html'));
// })

app.listen(PORT, () => {
  console.log('Server stared on port', PORT)
})