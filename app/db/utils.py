from sqlalchemy import Select


def is_positive(value: int):
    return value and value > 0


class BaseRepository:

    async def limit(self, query: Select, limit: int):
        if is_positive(limit):
            return query.limit(limit)
        return query

    async def offset(self, query: Select, offset: int):
        if is_positive(offset):
            return query.offset(offset)
        return query
