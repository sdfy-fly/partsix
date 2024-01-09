import asyncio
from uuid import UUID

from sqlalchemy import text, select

# from app.common.products import get_products
from app.db.database import async_session_maker
from app.product.schemas import ProductSchema, ReviewCount
from app.product.models import Product, ProductSet
from app.product.repository import ProductRepository


# async def import_products():
#     products = await get_products(0, 200)
#     await __import_products(products['data'])


async def __import_products(products):
    session = async_session_maker()
    repo = ProductRepository(session)

    for p in products:
        dto = ProductSchema(**p)
        await repo.create(dto)


async def upload_product_sets():
    session = async_session_maker()
    async with session.begin():

        parents = await session.execute(
            select(Product.hierarchicalParent).distinct()
        )

        for index, parent_id in enumerate(parents.scalars(), 1):
            products = await session.execute(
                select(Product).filter(Product.hierarchicalParent == parent_id)
            )

            for product in products.scalars():
                product_set = ProductSet(set_id=index, product_id=product.id)
                session.add(product_set)

        await session.commit()


async def upload_categories():
    query = """
    INSERT INTO category (id, parent_id, name) VALUES
    ('01000000', null, 'Токарный инструмент'),
    ('01010000', '01000000','Токарные монолитные резцы (таблица)'),
    ('01010100', '01010000', 'Токарные монолитные резцы для наружной обработки'),
    ('01010200', '01010000', 'Токарные монолитные резцы для внутренней обработки'),
    ('01010300', '01010000', 'Токарные монолитные отрезные и канавочные резцы'),
    ('01020000', '01000000', 'Токарные сборные резцы '),
    ('01020100', '01020000', 'Токарные сборные резцы для наружной обработки (таблица)'),
    ('01020200', '01020000', 'Токарные сборные резцы для внутренней обработки (таблица)'),
    ('01020300', '01020000', 'Токарные сборные отрезные и канавочные резцы (таблица)'),
    ('01020400', '01020000', 'Токарные сменные пластины (таблица)'),
    ('01020500', '01020000', 'Запасные части и комплектующие для токарных сборных резцов (таблица)'),
    ('02000000', null, 'Фрезерный инструмент'),
    ('02010000', '02000000', 'Фрезерный монолитный инструмент (таблица)'),
    ('02010100', '02010000', 'Фрезерный монолитный твердосплавный инструмент'),
    ('02010101', '02010100', 'Фрезы монолитные твердосплавные концевые'),
    ('02010102', '02010100', 'Фрезы монолитные твердосплавные фасочные'),
    ('02010103', '02010100', 'Фрезы монолитные твердосплавные радиусные'),
    ('02010104', '02010100', 'Фрезы монолитные твердосплавные сферические'),
    ('02010105', '02010100', 'Фрезы монолитные твердосплавные высокоподачные'),
    ('02010106', '02010100', 'Фрезы монолитные твердосплавные грибковые'),
    ('02010107', '02010100', 'Фрезы монолитные твердосплавные для радиусной фаски'),
    ('02010108', '02010100', 'Фрезы монолитные твердосплавные конические'),
    ('02010109', '02010100', 'Фрезы монолитные твердосплавные черновые'),
    ('02010110', '02010100', 'Фрезы монолитные твердосплавные дисковая'),
    ('02010200', '02010000', 'Фрезерный монолитный быстрорежущий инструмент'),
    ('02010201', '02010200', 'Фрезы монолитные быстрорежущие концевые'),
    ('02010202', '02010200', 'Фрезы монолитные быстрорежущие фасочные'),
    ('02010203', '02010200', 'Фрезы монолитные быстрорежущие радиусные'),
    ('02010204', '02010200', 'Фрезы монолитные быстрорежущие сферические'),
    ('02010205', '02010200', 'Фрезы монолитные быстрорежущие высокоподачные'),
    ('02010206', '02010200', 'Фрезы монолитные быстрорежущие грибковые'),
    ('02010207', '02010200', 'Фрезы монолитные быстрорежущие для радиусной фаски'),
    ('02010208', '02010200', 'Фрезы монолитные быстрорежущие конические'),
    ('02010209', '02010200', 'Фрезы монолитные быстрорежущие черновые'),
    ('02010300', '02010000', 'Фрезерный монолитный CBN PCD инструмент'),
    ('02020000', '02000000', 'Фрезерный сборный инструмент (таблица)'),
    ('02020100', '02020000', 'Фрезы сборные насадные'),
    ('02020101', '02020100', 'Фрезы сборные насадные для обработки уступов 90 градусов'),
    ('02020102', '02020100', 'Фрезы сборные насадные для обработки плоскостей'),
    ('02020103', '02020100', 'Фрезы сборные насадные для высокоподачной обработки'),
    ('02020104', '02020100', 'Фрезы сборные насадные фасочные'),
    ('02020105', '02020100', 'Фрезы сборные насадные дисковые'),
    ('02020200', '02020000', 'Фрезы сборные концевые'),
    ('02020201', '02020200', 'Фрезы сборные концевые для обработки уступов 90 градусов'),
    ('02020202', '02020200', 'Фрезы сборные концевые для обработки плоскостей'),
    ('02020203', '02020200', 'Фрезы сборные концевые для высокоподачной обработки'),
    ('02020204', '02020200', 'Фрезы сборные концевые фасочные'),
    ('02020205', '02020200', 'Фрезы сборные концевые дисковые'),
    ('02020300', '02020000', 'Фрезерные сменные пластины'),
    ('02020400', '02020000', 'Запчасти и комплектующие для фрезерного сборного инструмента'),
    ('03000000', null, 'Сверлильный инструмент'),
    ('03010000', '03000000', 'Сверла монолитные (таблица)'),
    ('03010100', '03010000', 'Сверла монолитные твердосплавные'),
    ('03010200', '03010000', 'Сверла монолитные быстрорежущие'),
    ('03010300', '03010000', 'Центровки монолитные'),
    ('03010400', '03010000', 'Зенковки монолитные'),
    ('03010500', '03010000', 'Цековки монолитные'),
    ('03010600', '03010000', 'Развертки монолитные'),
    ('03010700', '03010000', 'Сверло монолитное корончатое'),
    ('03010800', '03010000', 'Сверло монолитное ступенчатое'),
    ('03020000', '03000000', 'Сверла сборные (таблица)'),
    ('03020100', '03020000', 'Сверла сборные со сменными пластинами'),
    ('03020200', '03020000', 'Сверла сборные со сменными головками'),
    ('03020300', '03020000', 'Сверла сборные корончатые'),
    ('03020400', '03020000', 'Сверлильные сменные пластины и головки');
"""
    session = async_session_maker()
    async with session.begin():
        await session.execute(text(query))


async def get_review_count(product_id: UUID) -> ReviewCount:
    ...
