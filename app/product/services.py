from collections import defaultdict

from app.db.database import async_session_maker
from app.product.exceptions import InsertProductException
from app.product.repository import ProductRepository
from app.product.serializers import ProductSerializer, CategorySerializer, ProductShortSerializer
from app.product.schemas import (
    ProductSchema,
    ProductSetSchema,
    ProductOrderSchema,
    Category,
    ProductCreate,
)


class ProductService:

    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def create(self, body: ProductCreate) -> bool:
        try:
            await self.repo.create(body)
        except Exception as e:
            raise InsertProductException(str(e))
        return True

    async def receive(self, pk: int) -> ProductSchema | None:

        product = await self.repo.receive_product(pk)
        if product:
            return ProductSerializer.serialize(product)

        return None

    async def all(self, **kwargs) -> list[ProductSchema]:
        result = await self.repo.get_products(**kwargs)
        return ProductSerializer.serialize(result)

    async def get_by_category(
            self, category_id: int,
            **kwargs
    ) -> list[ProductSchema]:

        result = await self.repo.get_products_by_category(category_id, **kwargs)
        return ProductSerializer.serialize(result)

    async def get_products_categories_tree(self, **kwargs):
        result = await self.repo.get_categories_tree(**kwargs)
        return CategorySerializer.serialize(result)

    async def get_product_sets(self) -> list[ProductSetSchema]:

        results = await self.repo.get_product_sets()
        data = defaultdict(list)

        for set_id, product in results:
            data[set_id].append(product)

        return [
            ProductSetSchema(
                set_id=set_id,
                count=len(products),
                products=ProductShortSerializer.serialize(products)
            )
            for set_id, products in data.items()
        ]

    @staticmethod
    async def receive_product_set(set_id: int) -> ProductSetSchema:
        session = async_session_maker()
        repo = ProductRepository(session)

        products = await repo.receive_product_set(set_id)
        serialized_data = ProductShortSerializer.serialize(products)

        return ProductSetSchema(
            set_id=set_id,
            count=len(products),
            products=serialized_data
        )

    @staticmethod
    async def get_best_products(limit: int = None, offset: int = None) -> list[ProductOrderSchema]:
        session = async_session_maker()
        repo = ProductRepository(session)

        products = await repo.bests(limit, offset)

        return [
            ProductOrderSchema(
                product=ProductShortSerializer.serialize(product),
                category=Category(id=category.id, name=category.name),
                orders=orders or 0
            )
            for product, category, orders in products
        ]
