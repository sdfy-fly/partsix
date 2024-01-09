from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import DATABASE_URL, SHOW_SQL_QUERY

engine = create_async_engine(DATABASE_URL, echo=SHOW_SQL_QUERY)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()
