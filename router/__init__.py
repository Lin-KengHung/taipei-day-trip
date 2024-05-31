import mysql.connector
from pydantic import BaseModel
import os
from dotenv import load_dotenv

## .env
load_dotenv()
password = os.getenv("PASSWORD")


## connect to MySQL
mydb = {
    "host" : "localhost",
    "user" : "root",
    "password" : password,
    "database" : "taipei_day_trip"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=10, **mydb)

## universal model

class Error(BaseModel):
    error : bool = True
    message : str