import json
import re
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="taipei_day_trip"
)
mycursor = mydb.cursor()

with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)

def split_urls_to_url_list(urls : str) -> list:
    raw_list = urls.split("https")
    process_list = []
    pattern = ".+[JPG|jpg|PNG|png]$"
    for url in raw_list:
        if re.match(pattern,url):
            process_list.append("https" + url)
    return process_list

for attraction in data["result"]["results"]:
    img_list = split_urls_to_url_list(attraction["file"])
    # print(attraction["_id"])
    ## insert into attraction table
    sql = "INSERT INTO attraction (id, name, category, description, address, transport, mrt, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (attraction["_id"], attraction["name"], attraction["CAT"], attraction["description"], attraction["address"], attraction["direction"], attraction["MRT"], attraction["latitude"], attraction["longitude"])
    mycursor.execute(sql, val)
    mydb.commit()
    ## insert into image table
    for url in img_list:
        sql = "INSERT INTO image (url, attraction_id) VALUES (%s, %s)"
        val = (url, attraction["_id"])
        mycursor.execute(sql, val)
        mydb.commit()
    
mycursor.close()
mydb.close()


'''
 -------------------------------Create table via SQL----------------------------------------------------

CREATE TABLE attraction (
  id BIGINT PRIMARY KEY COMMENT "Unique ID",
  name VARCHAR(255) NOT NULL COMMENT "name",
  category VARCHAR(255) NOT NULL COMMENT "category CAT",
  description VARCHAR(2000) NOT NULL COMMENT "description",
  address VARCHAR(255) NOT NULL COMMENT "address",
  transport VARCHAR(500) NOT NULL COMMENT "direction",
  mrt VARCHAR(255) COMMENT "mrt",
  lat FLOAT UNSIGNED NOT NULL DEFAULT 0 COMMENT "latitude",
  lng FLOAT UNSIGNED NOT NULL DEFAULT 0 COMMENT "longitude"
);

CREATE TABLE image (
  id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT "Unique ID", 
  url TEXT NOT NULL COMMENT "image url",
  attraction_id BIGINT NOT NULL COMMENT "attraction id for image belonging",
  FOREIGN KEY (attraction_id) REFERENCES attraction(id)
);
'''