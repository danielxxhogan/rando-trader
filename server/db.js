const Pool = require('pg').Pool;

const pool = new Pool({
  user: 'postgres',
  password: 'COLExBURNED#363',
  host: 'database-2.c7stlrulp8px.us-east-1.rds.amazonaws.com',
  port: 5432,
  database: 'sk'
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