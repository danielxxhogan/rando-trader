const Pool = require('pg').Pool;
require('dotenv').config()

const pool = new Pool({
  user: PG_USER,
  password: PG_PASSWORD,
  host: PG_HOST,
  port: PG_PORT,
  database: PG_DATABASE
});

// const testing_db = async () => {
//   try {
//     const results = await pool.query(
//       'select products.name, description, price, images.name as image, categories.name as category \
//        from products \
//        join images \
//        on products.product_id = images.product_id \
//        join categories \
//        on products.category_id = categories.category_id'
//       );
  
//       console.log(results);
//   } catch (err) {
//     console.log(err);
//   };
// };

// testing_db();

module.exports = pool;