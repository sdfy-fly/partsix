from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.common.templates import templates

dashboard_router = APIRouter()


@dashboard_router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard/index.html", {"request": request})
