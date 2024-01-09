from typing import Annotated

from fastapi import Depends

from app.db.database import async_session_maker
from app.product.repository import ProductRepository
from app.product.services import ProductService


async def get_product_repo() -> ProductRepository:
    session = async_session_maker()
    return ProductRepository(session)


async def get_product_service(
        repo: Annotated[ProductRepository, Depends(get_product_repo)]
) -> ProductService:
    return ProductService(repo)
