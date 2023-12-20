import uvicorn

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import APP_HOST, APP_PORT
# from app.product.routes import product_router

app = FastAPI()
main_router = APIRouter()

# main_router.include_router(product_router, prefix="/product", tags=["product"])
# app.include_router(main_router)


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "id": 123})


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
