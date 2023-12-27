from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.utils.templates import templates

product_router = APIRouter()


@product_router.get("/details", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("product/details/index.html", {"request": request})
