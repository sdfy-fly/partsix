import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles

from config import APP_HOST, APP_PORT
from app.dashboard.routes import dashboard_router
from app.product.routes import product_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="./static/partsix"), name="static")

main_router = APIRouter()
main_router.include_router(dashboard_router, prefix="", tags=["DashBoard"])
main_router.include_router(product_router, prefix="/product", tags=["Product"])

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)
