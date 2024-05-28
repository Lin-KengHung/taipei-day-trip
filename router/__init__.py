import mysql.connector

mydb = {
    "host" : "localhost",
    "user" : "root",
    "password" : "123456",
    "database" : "taipei_day_trip"
}
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=10, **mydb)