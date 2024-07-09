from fastapi import *
from fastapi.responses import FileResponse, JSONResponse
from router import attraction, user, booking, order
from view.share import Error
from view.user_view import CustomizeRaise
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError


app = FastAPI(
	title="APIs for Taipei Day Trip",
    version="1.0.0",
    summary="台北一日遊網站 API 規格：網站後端程式必須支援這個 API 的規格，網站前端則根據 API 和後端互動。",
)

app.include_router(attraction.router)
app.include_router(user.router)
app.include_router(booking.router)
app.include_router(booking.router)
app.include_router(order.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


## 500 error raise
@app.middleware("http")
async def ServerError(request: Request, call_next):
	try:
		response = await call_next(request)
		return response
	except Exception as e:
		print(e)
		return JSONResponse(status_code=500,content=Error(message="伺服器內部錯誤").model_dump())

## 403 customize error raise 
@app.exception_handler(CustomizeRaise)
async def error_raise(requset: Request, exc: CustomizeRaise):
	return JSONResponse(status_code=exc.status_code, content=Error(message=exc.message).model_dump())

## validation error 
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	error = exc.errors()[0]
	message = f'錯誤欄位:{error["loc"]}, 錯誤訊息: {error["msg"]}, 錯誤類型: {error["type"]}'
	return JSONResponse(status_code=400,content=Error(message=message).model_dump())

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



