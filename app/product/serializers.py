from typing import Union, Iterable, List

from app.product.models import Product, ProductCategories, ProductAttributes, ProductReview
from app.product.utils import get_review_count
from app.product.schemas import (
    ProductSchema,
    Category,
    CategoryTree,
    ProductShort,
    AttributeSchema,
    ReviewSchema,
)


class ProductSerializer:
    @classmethod
    def serialize(cls, product: Product | Iterable[Product]) -> ProductSchema | list[ProductSchema]:
        if isinstance(product, Iterable):
            return [cls._serialize_single(item) for item in product]
        else:
            return cls._serialize_single(product)

    @classmethod
    def _serialize_single(cls, product: Product) -> ProductSchema:

        images = [img.url for img in product.images]
        attrs = AttributeSerializer.serialize(product.attributes)
        reviews = ReviewSerializer.serialize(product.reviews)

        return ProductSchema(
            id=product.id,
            article=attrs,
            name=product.name,
            cost=product.cost,
            discount=product.discount,
            description=product.description,
            description_simple=product.description_simple,
            published=product.published,
            images=images,
            attributes=attrs,
            reviews=reviews,
        )


class ProductShortSerializer:
    @classmethod
    async def serialize(cls, product: Union[Product, Iterable[Product]]) -> Union[ProductShort, List[ProductShort]]:
        if isinstance(product, Iterable):
            return [await cls._serialize_single(item) for item in product]
        else:
            return await cls._serialize_single(product)

    @classmethod
    async def _serialize_single(cls, product: Product) -> ProductShort:
        images = [img.url for img in product.images]
        reviews = await get_review_count(product.id)

        return ProductShort(
            id=product.id,
            article=product.article,
            name=product.name,
            cost=product.cost,
            discount=product.discount,
            images=images,
            reviews=reviews,
        )


class CategorySerializer:
    @classmethod
    def serialize(cls, categories: Iterable[ProductCategories]) -> List[CategoryTree]:
        data = []
        for c in categories:
            category = CategoryTree(
                id=c.id,
                name=c.name,
                sub_categories=None
            )
            subs = [sub for sub in categories if sub.parent_id == c.id]
            if subs:
                sub_categories = [Category(id=s.id, name=s.name) for s in subs]
                category.sub_categories = sub_categories
            data.append(category)

        return data


class AttributeSerializer:
    @classmethod
    def serialize(cls, attrs: Iterable[ProductAttributes]) -> list[AttributeSchema]:
        return [
            AttributeSchema(
                id=attr.id,
                name=attr.name,
                text=attr.text,
            )
            for attr in attrs
        ]


class ReviewSerializer:
    @classmethod
    def serialize(cls, reviews: Iterable[ProductReview]) -> list[ReviewSchema]:
        return [
            ReviewSchema(
                id=review.id,
                text=review.text,
                rating=review.rating,
                created_at=review.created_at,
            )
            for review in reviews
        ]
