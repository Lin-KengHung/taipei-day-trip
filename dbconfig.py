import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_HOST = os.getenv('DATABASE_HOST')
# DATABASE_HOST = "localhost"
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

print(f"Host: {DATABASE_HOST}, User: {DATABASE_USER}")

class Database:
    mydb = {
        "host": DATABASE_HOST,
        "user": DATABASE_USER,
        "password": DATABASE_PASSWORD,
        "database": DATABASE_NAME
    }
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="my_pool", pool_size=15, **mydb)
    
    def read_all(sql, val=None):
        connect = Database.connection_pool.get_connection()
        mycursor = connect.cursor(dictionary=True)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        mycursor.close()
        connect.close()
        return result
    
    def read_one(sql, val=None):
        connect = Database.connection_pool.get_connection()
        mycursor = connect.cursor(dictionary=True)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        mycursor.close()
        connect.close()
        return result

    def create(sql, val=None):
        connect = Database.connection_pool.get_connection()
        mycursor = connect.cursor(dictionary=True)
        mycursor.execute(sql, val)
        connect.commit()
        affected_rows = mycursor.rowcount
        mycursor.close()
        connect.close()
        return affected_rows
    
    def update(sql, val=None):
        connect = Database.connection_pool.get_connection()
        mycursor = connect.cursor(dictionary=True)
        mycursor.execute(sql, val)
        connect.commit()
        affected_rows = mycursor.rowcount
        mycursor.close()
        connect.close()
        return affected_rows
    
    def delete(sql, val=None):
        connect = Database.connection_pool.get_connection()
        mycursor = connect.cursor(dictionary=True)
        mycursor.execute(sql, val)
        connect.commit()
        affected_rows = mycursor.rowcount
        mycursor.close()
        connect.close()
        return affected_rows
