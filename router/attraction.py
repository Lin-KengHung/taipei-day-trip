from fastapi import APIRouter


router = APIRouter(
     prefix="/api", 
     tags=["Attraction"]
)

@router.get("/attractions")
async def test():
    return {"ok": True}