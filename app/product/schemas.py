from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo


class AttributeSchema(BaseModel):
    id: int | None = None
    name: str
    text: str


class ReviewSchema(BaseModel):
    id: int | None = None
    text: str
    rating: int
    created_at: date


class ReviewCount(BaseModel):
    count: int
    avg: float


class ProductCreate(BaseModel):
    article: str
    name: str
    cost: float
    discount: int
    description: Optional[str] = None
    description_simple: Optional[str] = None
    published: bool
    category_id: int
    images: list[str] | None = None
    attributes: list[AttributeSchema] | None = None
    reviews: list[ReviewSchema] | None = None

    @field_validator("cost", "discount")
    def validate_balance(cls, value: int, info: ValidationInfo) -> Optional[int]:
        if value < 0:
            raise HTTPException(
                status_code=422, detail=f"{info.field_name} should be positive"
            )
        return value


class ProductSchema(ProductCreate):
    id: UUID


class ProductShort(BaseModel):
    id: UUID
    article: str
    name: str
    cost: float
    discount: int
    images: list[str] | None
    reviews: ReviewCount


class Category(BaseModel):
    id: str
    name: str


class CategoryTree(BaseModel):
    id: str
    name: str
    sub_categories: list[Category] | None


class ProductSetSchema(BaseModel):
    set_id: int
    count: int
    products: list[ProductShort] | None


class ProductOrderSchema(BaseModel):
    category: Category
    product: ProductShort
    orders: int
