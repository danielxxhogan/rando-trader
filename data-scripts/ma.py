import requests
from bs4 import BeautifulSoup
import psycopg2

from config import *

conn = psycopg2.connect(user=PG_USER,
                 password=PG_PASSWORD,
                 host=PG_HOST,
                 port=PG_PORT,
                 dbname=PG_DATABASE,
                 )

cursor = conn.cursor()

r = requests.get(url='https://www.benzinga.com/m-a')

src = r.content
soup = BeautifulSoup(src, 'lxml')