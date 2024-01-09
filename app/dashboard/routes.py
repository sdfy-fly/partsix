from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.common.templates import templates

dashboard_router = APIRouter()


@dashboard_router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("home/index.html", {"request": request})
