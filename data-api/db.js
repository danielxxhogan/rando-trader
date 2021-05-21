require('dotenv').config()
const Pool = require('pg').Pool;

console.log(process.env.PG_USER);

try {
  const pool = new Pool({
    user: process.env.PG_USER,
    password: process.env.PG_PASSWORD,
    host: process.env.PG_HOST,
    port: process.env.PG_PORT,
    database: process.env.PG_DATABASE
  });

  module.exports = pool;

} catch (err) {
  console.log(err.message);
}


