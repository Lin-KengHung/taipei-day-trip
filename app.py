from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from router import attraction
from pydantic import BaseModel
from router import Error

app = FastAPI(
	title="APIs for Taipei Day Trip",
    version="1.0.0",
    summary="台北一日遊網站 API 規格：網站後端程式必須支援這個 API 的規格，網站前端則根據 API 和後端互動。",
)

app.include_router(attraction.router)

@app.middleware("http")
async def ServerError(request: Request, call_next):
	try:
		response = await call_next(request)
		return response
	except:
		return JSONResponse(status_code=500,content=Error(message="伺服器內部錯誤"))



# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")
