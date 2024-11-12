from fastapi import *
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.dbconfig import get_db
from view.share import Error
from view.attraction_view import AttractionListOut, AttractionSingleOut, MrtsOut
from repository.attraction_repository import AttractionRepository

router = APIRouter(
     prefix="/api", 
)



@router.get("/attractions" , summary="取得景點資料列表", response_model=AttractionListOut, description="取得不同分頁的旅遊景點列表資料，也可以根據標題關鍵字、或捷運站名稱篩選", tags=["Attraction"])
async def get_attraction_data_list(
    page: int = Query(..., ge=0, description="要取得的分頁，每頁 12 筆資料"), 
    keyword: str  =  Query(default="", description="用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做篩選"),
    db: Session = Depends(get_db),
    ):
    return AttractionRepository.get_attraction_data_list(db, page, keyword)

@router.get("/attraction/{attractionId}", summary="根據景點編號取得景點資料", tags=["Attraction"], response_model=AttractionSingleOut, responses={400:{"model":Error}})
async def get_attraction_data_by_id(attractionId: int, db: Session = Depends(get_db)) :
    result = AttractionRepository.get_attraction_data_by_id(db, attractionId)

    if isinstance(result, Error):
       return JSONResponse(status_code=400, content=result.model_dump())

    return result

@router.get("/mrts", summary="取得捷運站名稱列表", description="取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序", tags=["MRT Station"], response_model=MrtsOut)
async def get_mrts_list(db: Session = Depends(get_db)):
    result = AttractionRepository.get_mrts_list(db)
    return result

