from sqlalchemy.orm import Session
from sqlalchemy import func
from model.attraction_model import Attraction, Image
from view.attraction_view import AttractionListOut, AttractionSingleOut, MrtsOut
from view.share import Error


class AttractionRepository:

    @staticmethod
    def get_attraction_data_list(db: Session, page: int, keyword: str = ""):
        query = (
            db.query(
                Attraction,
                func.array_agg(Image.url).label("images")  # 聚合圖片 URL
            )
            .outerjoin(Image, Attraction.id == Image.attraction_id)
            .filter(
                (Attraction.name.ilike(f"%{keyword}%")) |  # 使用 ILIKE 提升效能
                (Attraction.mrt.ilike(f"%{keyword}%"))
            )
            .group_by(Attraction.id)
            .offset(page * 12)
            .limit(13)
        )
        results = query.all()

        attractions_list = [
            {
                "id": attraction.id,
                "name": attraction.name,
                "category": attraction.category,
                "description": attraction.description,
                "address": attraction.address,
                "transport": attraction.transport,
                "mrt": attraction.mrt,
                "lat": attraction.lat,
                "lng": attraction.lng,
                "images": images or [],
            }
            for attraction, images in results
        ]

        next_page = page + 1 if len(attractions_list) == 13 else None
        if next_page:
            attractions_list.pop()

        return AttractionListOut(nextPage=next_page, data=attractions_list)
    
    @staticmethod
    def get_attraction_data_by_id(db: Session, attraction_id: int) -> AttractionSingleOut | Error:
        """
        根據 ID 查詢景點
        """
        query = (
            db.query(
                Attraction,
                func.array_agg(Image.url).label("images")  # 聚合圖片 URL
            )
            .outerjoin(Image, Attraction.id == Image.attraction_id)
            .filter(Attraction.id == attraction_id)
            .group_by(Attraction.id)
        )
        result = query.first()

        if not result:
            return Error(message="景點編號不正確")

        attraction, images = result
        return AttractionSingleOut(
            data={
                "id": attraction.id,
                "name": attraction.name,
                "category": attraction.category,
                "description": attraction.description,
                "address": attraction.address,
                "transport": attraction.transport,
                "mrt": attraction.mrt,
                "lat": attraction.lat,
                "lng": attraction.lng,
                "images": images or [],
            }
        )

    @staticmethod
    def get_mrts_list(db: Session) -> MrtsOut:
        """
        查詢 MRT 列表
        """
        mrt_query = (
            db.query(Attraction.mrt)
            .filter(Attraction.mrt.isnot(None))
            .group_by(Attraction.mrt)
            .order_by(func.count(Attraction.id).desc())
        )
        mrt_list = [mrt[0] for mrt in mrt_query.all()]
        return MrtsOut(data=mrt_list)
    