from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from .database import Base

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
strname = Annotated[str, mapped_column(String(50), unique=True, index=True)]


class WomanName(Base):
    __tablename__ = 'names_woman'

    id: Mapped[intpk]
    name: Mapped[strname]

    def __repr__(self):
        return f'{self.name}'


class ManName(Base):
    __tablename__ = 'names_man'

    id: Mapped[intpk]
    name: Mapped[strname]

    def __repr__(self):
        return f'{self.name}'
