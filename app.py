from fastapi import *
from fastapi.responses import FileResponse
from router import attraction

app = FastAPI(
	title="APIs for Taipei Day Trip",
    version="1.0.0",
    summary="台北一日遊網站 API 規格：網站後端程式必須支援這個 API 的規格，網站前端則根據 API 和後端互動。",
)

app.include_router(attraction.router)


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