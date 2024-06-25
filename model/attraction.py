from dbconfig import Database
from pydantic import BaseModel
from typing import List

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
     
class AttractionModel:

    def get_attraction_data_list(page: int, keyword: str =""):

        keyword = '%' + keyword + '%'
        
        # get query total row
        result = Database.read("SELECT COUNT(*) FROM attraction WHERE name LIKE %s or mrt LIKE %s", (keyword, keyword))[0]
        tot_raw = result["COUNT(*)"]
        
        # get attraction data
        attractions_list = Database.read("SELECT * FROM attraction WHERE name LIKE %s or mrt LIKE %s LIMIT %s, %s", (keyword, keyword, page * 12, 12))
        # get image url of needed attractions
        images_list = Database.read("SELECT a.id, i.url FROM (SELECT id FROM attraction WHERE name LIKE %s or mrt LIKE %s LIMIT %s, %s) AS a JOIN image AS i ON a.id = i.attraction_id", (keyword, keyword, page * 12, 12))

        data_list = AttractionModel.make_Attraction_schema(attractions_list, images_list)
        nextPage = page + 1 if page * 12 + 12 < tot_raw else None

        return [nextPage, data_list]
    
    def make_Attraction_schema(attraction_list, image_list):
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
