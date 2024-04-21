from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import setting

engine_async = create_async_engine(
    url=setting.get_url_database,
    echo=True,
)

session_async_factory = async_sessionmaker(
    bind=engine_async,
)


class Base(DeclarativeBase):
    ...
