require('dotenv').config()
const Pool = require('pg').Pool;

try {
  const pool = new Pool({
    user=PG_USER,
    password=PG_PASSWORD,
    host=PG_HOST,
    port=PG_PORT,
    database: PG_DATABASE
  });

  module.exports = pool;

} catch (err) {
  console.log(err.message);
}


