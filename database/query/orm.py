from typing import Type

from sqlalchemy import select

from ..database import Base, engine_async, session_async_factory
from ..models import WomanName, ManName


class AsyncORM:
    @staticmethod
    async def create_table() -> None:
        async with engine_async.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            # await connection.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_names(model: Type[WomanName | ManName], names: list[str]) -> None:
        async with session_async_factory() as session:
            name_objs = []
            for name in names:
                name_objs.append(model(name=name))
            session.add_all(name_objs)
            await session.commit()

    @staticmethod
    async def get_name(model: Type[WomanName | ManName], name: str) -> list[WomanName | ManName]:
        async with session_async_factory() as session:
            query = select(model).filter(model.name == name)
            result = await session.execute(query)
            return result.scalars().all()
