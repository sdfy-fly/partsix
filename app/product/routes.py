from typing import Annotated

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse

from app.common.templates import templates
from app.product.dependencies import get_product_service
from app.product.exceptions import InsertProductException
from app.product.schemas import ProductCreate
from app.product.services import ProductService

product_router = APIRouter()


@product_router.get("/details", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("product/details/index.html", {"request": request})


@product_router.post('/')
async def create_product(
        body: ProductCreate,
        service: Annotated[ProductService, Depends(get_product_service)]
):
    """ Создать товар """
    try:
        await service.create(body)
    except InsertProductException as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {'success': True}
