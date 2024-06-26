from dbconfig import Database
from model.share import Error
from pydantic import BaseModel, Field
from typing import Optional
import json


# ---------- View ----------
class Attraction(BaseModel):
	id: int 
	name: str 
	category: str
	description: str
	address: str
	transport: str
	mrt: str | None = None
	lat: float
	lng: float
	images: list[str]
class AttractionListOut(BaseModel):
     nextPage: Optional[int] = Field(None, gt=0)
     data: list[Attraction]
class AttractionSingleOut(BaseModel):
    data: Attraction
class MrtsOut(BaseModel):
    data: list

# ---------- Core model  ----------
class AttractionModel:

     def get_attraction_data_list(page: int, keyword: str ="") -> AttractionListOut:
        
        ## 資料庫搜尋
        keyword = '%' + keyword + '%'
        sql = "SELECT a.*, JSON_ARRAYAGG(i.url) AS images FROM attraction a LEFT JOIN image i ON a.id = i.attraction_id WHERE name LIKE %s or mrt LIKE %s GROUP BY a.id LIMIT %s, %s;"
        val = (keyword, keyword, page * 12, 13)
        attractions_list = Database.read_all(sql, val)

        ## 資料格式處裡
        for attraction in attractions_list:
             attraction["images"] = json.loads(attraction["images"])
             attraction = Attraction(**attraction)
        
        ## 判斷有沒有下一頁
        if (len(attractions_list) == 13):
             nextPage = page + 1
             attractions_list.pop()
        else:
             nextPage = None

        return AttractionListOut(nextPage=nextPage, data=attractions_list)
    
     def get_attraction_data_by_id(id) -> AttractionSingleOut | Error:

        ## 資料搜尋
        sql = "SELECT a.*, JSON_ARRAYAGG(i.url) AS images FROM attraction a LEFT JOIN image i ON a.id = i.attraction_id WHERE a.id = %s GROUP BY a.id"
        val = (id,)
        attraction = Database.read_one(sql, val)

        ## 錯誤ID狀況
        if not attraction:
             return Error(message="景點編號不正確")
        
        ## 資料處裡
        attraction["images"] = json.loads(attraction["images"])

        return AttractionSingleOut(data=Attraction(**attraction))

     def get_mrts_list() -> MrtsOut:

          # 查詢資料庫
          sql = "SELECT mrt FROM attraction WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count(*) DESC"
          raw_mrt_list = Database.read_all(sql)

          # 資料格式處裡
          mrt_list = list(map(lambda x: x["mrt"], raw_mrt_list))

          return MrtsOut(data=mrt_list)
