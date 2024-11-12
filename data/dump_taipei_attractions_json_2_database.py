import json
import re
import psycopg2
from dotenv import load_dotenv, find_dotenv
import os




# 加載環境變數
env_path = find_dotenv("..\\.env")  
load_dotenv(env_path)

password = os.getenv("DATABASE_PASSWORD")

# 連接到 PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password=password,
    database="taipei_day_trip",
    options="-c client_encoding=UTF8"
)
cur = conn.cursor()

# 讀取 JSON 檔案
with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)

# 清理數據的函數
def clean_data(data):
    try:
        return data.encode('utf-8', errors='ignore').decode('utf-8')
    except Exception as e:
        print(f"Encoding error: {e}")
        return ""

# 處理圖片 URL
def split_urls_to_url_list(urls: str) -> list:
    raw_list = urls.split("https")
    process_list = []
    pattern = ".+[JPG|jpg|PNG|png]$"
    for url in raw_list:
        if re.match(pattern, url):
            process_list.append("https" + url)
    return process_list

# 清空原本的資料
cur.execute("TRUNCATE TABLE image RESTART IDENTITY CASCADE;")
cur.execute("TRUNCATE TABLE attraction RESTART IDENTITY CASCADE;")
conn.commit()

# 插入資料
for attraction in data["result"]["results"]:
    # 清理資料
    description = clean_data(attraction["description"])
    img_list = split_urls_to_url_list(attraction["file"])

    # 插入 attraction 資料
    sql_attraction = """
    INSERT INTO attraction (id, name, category, description, address, transport, mrt, lat, lng)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    """
    val_attraction = (
        attraction["_id"],
        clean_data(attraction["name"]),
        clean_data(attraction["CAT"]),
        description,
        clean_data(attraction["address"]),
        clean_data(attraction["direction"]),
        clean_data(attraction["MRT"]) if attraction["MRT"] else None,
        attraction["latitude"],
        attraction["longitude"]
    )
    cur.execute(sql_attraction, val_attraction)

    # 插入 image 資料
    for url in img_list:
        sql_image = """
        INSERT INTO image (url, attraction_id)
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING
        """
        val_image = (clean_data(url), attraction["_id"])
        cur.execute(sql_image, val_image)

    # 提交交易
    conn.commit()

# 關閉資料庫連接
cur.close()
conn.close()


# CREATE TABLE attraction (
#     id BIGINT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     category VARCHAR(255) NOT NULL,
#     description TEXT NOT NULL,
#     address TEXT NOT NULL,
#     transport TEXT NOT NULL,
#     mrt VARCHAR(255),
#     lat DOUBLE PRECISION NOT NULL DEFAULT 0,
#     lng DOUBLE PRECISION NOT NULL DEFAULT 0
# );

# CREATE TABLE image (
#     id SERIAL PRIMARY KEY,
#     url TEXT NOT NULL,
#     attraction_id BIGINT NOT NULL,
#     FOREIGN KEY (attraction_id) REFERENCES attraction(id)
# );
