from sqlalchemy import select, cast, Integer, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.db.utils import BaseRepository
from app.product.models import Product, ProductImages, ProductAttributes, ProductCategories, ProductSet, ProductReview
from app.product.schemas import ProductCreate


class ProductRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, body: ProductCreate) -> Product:
        async with self.session.begin():

            product = Product(
                article=body.article,
                name=body.name,
                cost=body.cost,
                discount=body.discount,
                description=body.description,
                description_simple=body.description_simple,
                published=body.published,
                category_id=body.category_id,
            )

            if body.images:
                for url in body.images:
                    ProductImages(url=url, product=product)

            if body.attributes:
                for attr in body.attributes:
                    ProductAttributes(product=product, name=attr.name, text=attr.text)

            if body.reviews:
                for r in body.reviews:
                    ProductReview(text=r.text, created_at=r.created_at, rating=r.rating, product=product)

            self.session.add(product)
            await self.session.commit()

        return product

    async def receive_product(self, pk: int):
        async with self.session.begin():
            query = select(Product).where(
                cast(Product.id, Integer) == pk
            ).options(selectinload(Product.images), selectinload(Product.attributes))
            product = await self.session.scalars(query)
            await self.session.flush()
        return product.first()

    async def get_products(self, **kwargs):
        async with self.session.begin():
            query = select(Product).options(selectinload(Product.images), selectinload(Product.attributes))

            if kwargs['name']:
                query = query.filter(Product.name.ilike(f"%{kwargs['name']}%"))
            if kwargs['article']:
                query = query.filter_by(article=kwargs['article'])

            query = await self.offset(query, kwargs['offset'])
            query = await self.limit(query, kwargs['limit'])

            products = await self.session.scalars(query)
        return products.unique().all()

    async def get_products_by_category(self, **kwargs):
        async with self.session.begin():
            query = select(Product).options(
                joinedload(Product.images), joinedload(Product.attributes)
            ).where(
                and_(
                    Product.category_id == kwargs['category_id']
                )
            )
            query = await self.offset(query, kwargs['offset'])
            query = await self.limit(query, kwargs['limit'])

            products = await self.session.scalars(query)
        return products.unique().all()

    async def get_categories_tree(self, **kwargs):
        async with self.session.begin():
            query = select(ProductCategories).order_by('id')
            query = await self.limit(query, kwargs['limit'])

            categories = await self.session.execute(query)
            return categories.scalars().all()

    async def get_product_sets(self):
        async with self.session.begin():
            query = (
                select(ProductSet.set_id, Product)
                .join(ProductSet, cast(ProductSet.product_id, Integer) == Product.id)
                .options(
                    joinedload(Product.images),
                )
                .order_by(ProductSet.set_id)
            )
            results = await self.session.execute(query)
        return results.unique()

    async def receive_product_set(self, set_id: int):
        async with self.session.begin():
            query = (
                select(Product)
                .join(ProductSet, cast(ProductSet.product_id, Integer) == Product.id)
                .options(
                    joinedload(Product.images),
                    joinedload(Product.attributes)
                )
                .filter(cast(ProductSet.set_id, Integer) == set_id)
            )
            result = await self.session.execute(query)
        return result.unique().scalars().all()

    # async def bests(self, limit: int = None, offset: int = None):
    #     async with self.session.begin():
    #         subquery = (
    #             select(
    #                 Order.product_id,
    #                 func.count().label('orders')
    #             )
    #             .group_by(Order.product_id)
    #             .alias('anon_1')
    #         )
    #
    #         query = (
    #             select(
    #                 Product,
    #                 ProductCategories,
    #                 subquery.c.orders
    #             )
    #             .join(subquery, Product.id == subquery.c.product_id, isouter=True)
    #             .join(ProductCategories, cast(Product.category_id, String) == ProductCategories.id)
    #             .options(
    #                 joinedload(Product.images)
    #             )
    #             .order_by(subquery.c.orders.desc().nullslast())
    #         )
    #
    #         query = await self.limit(query, limit)
    #         query = await self.offset(query, offset)
    #         products = await self.session.execute(query)
    #
    #     return products.unique()
