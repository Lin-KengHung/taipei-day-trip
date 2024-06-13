from fastapi import *
from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
from . import connection_pool, Error
from fastapi.responses import JSONResponse




router = APIRouter(
     prefix="/api", 
)

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
	images: List[str]
class AttractionOut(BaseModel):
     nextPage: Optional[int] = Field(None, gt=0)
     data: List[Attraction]

class DataOut(BaseModel):
    data: Union[list, dict] 

    


@router.get("/attractions", response_model=AttractionOut , summary="取得景點資料列表", description="取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選", tags=["Attraction"])
async def get_attraction_data_list(page: int = Query(..., ge=0, description="要取得的分頁，每頁 12 筆資料"), keyword: str  =  Query(default="", description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選")):
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)
 
    keyword = '%' + keyword + '%'
    # get query total row
    mycursor.execute("SELECT COUNT(*) FROM attraction WHERE name LIKE %s or mrt LIKE %s", (keyword, keyword))
    tot_raw = mycursor.fetchone()["COUNT(*)"]
    # get attraction data
    mycursor.execute("SELECT * FROM attraction WHERE name LIKE %s or mrt LIKE %s LIMIT %s, %s", (keyword, keyword, page * 12, 12))
    attractions_list = mycursor.fetchall()
    # get image url of needed attractions
    mycursor.execute("SELECT a.id, i.url FROM (SELECT id FROM attraction WHERE name LIKE %s or mrt LIKE %s LIMIT %s, %s) AS a JOIN image AS i ON a.id = i.attraction_id", (keyword, keyword, page * 12, 12))
    images_list = mycursor.fetchall()

    data_list = make_Attraction_schema(attractions_list, images_list)
    nextPage = page + 1 if page * 12 + 12 < tot_raw else None
    response = AttractionOut(nextPage=nextPage, data=data_list)
    mycursor.close()
    connect.close()
    return response


@router.get("/attraction/{attractionId}", summary="根據景點編號取得景點資料", tags=["Attraction"], response_model=DataOut, responses={400:{"model":Error}})
async def get_attraction_data_by_id(attractionId: int) :
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)

    # get attraction data
    mycursor.execute("SELECT * FROM attraction WHERE id = %s", (attractionId,))
    attractions_list = mycursor.fetchall()
    if not attractions_list:
        return JSONResponse(status_code=400, content=Error(message="景點編號不正確").model_dump())

    # get image url of needed attractions
    mycursor.execute("SELECT a.id, i.url FROM (SELECT id FROM attraction WHERE id = %s) AS a JOIN image AS i ON a.id = i.attraction_id", (attractionId,))
    images_list = mycursor.fetchall()
    attraction_dict = dict(make_Attraction_schema(attractions_list, images_list)[0])
    response = DataOut(data=attraction_dict)

    mycursor.close()
    connect.close()
    return response

@router.get("/mrts", summary="取得捷運站名稱列表", description="取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序", tags=["MRT Station"], response_model=DataOut)
async def get_mrts_list():
    connect = connection_pool.get_connection()
    mycursor = connect.cursor(dictionary=True)

    # get all mrts 
    mycursor.execute("SELECT mrt FROM attraction WHERE mrt IS NOT NULL GROUP BY mrt ORDER BY count(*) DESC")
    raw_mrt_list = mycursor.fetchall()

    mrt_list = list(map(lambda x: x["mrt"], raw_mrt_list))
    response = DataOut(data=mrt_list)
    mycursor.close()
    connect.close()
    return response

def make_Attraction_schema(attraction_list, image_list) -> List[Attraction]:
     # image list vertical integrate
    id2image_list = {}
    for image in image_list:
        id = image["id"]
        if id not in id2image_list:
            id2image_list[id] = []
        id2image_list[id].append(image["url"])
    # make data list with Attraction schema
    data_list = []
    for attraction in attraction_list:
        attraction["images"] = id2image_list[attraction["id"]]
        data_list.append(Attraction(**attraction))
    return data_list
