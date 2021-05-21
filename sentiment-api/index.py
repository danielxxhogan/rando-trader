from flask import Flask
import psycopg2

from config import *


app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test():
    conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

    cursor = conn.cursor()
    
    conn.commit()

    cursor.close()
    conn.close()
    
    return 'test'


if __name__ == '__main__':
    app.run()