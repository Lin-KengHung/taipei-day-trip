import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv("PASSWORD")

mydb = {
    "host" : "localhost",
    "user" : "root",
    "password" : password,
    "database" : "taipei_day_trip"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=10, **mydb)