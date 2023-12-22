from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.utils.templates import templates

home_router = APIRouter()


@home_router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})
