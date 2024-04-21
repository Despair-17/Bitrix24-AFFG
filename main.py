import sqlalchemy

from database.query import orm
from database.models import WomanName, ManName
import asyncio


async def main():
    try:
        await orm.AsyncORM.insert_names(WomanName, ['Аврора', 'Аза'])
    except sqlalchemy.exc.IntegrityError as err:
        print(err)
    # res = await orm.AsyncORM.get_name(WomanName, 'Белла')
    # print(res)
    ...


if __name__ == '__main__':
    asyncio.run(main())
