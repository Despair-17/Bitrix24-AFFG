import sqlalchemy

from database.query.orm import AsyncORM
from database.models import WomanName, ManName
import asyncio


async def main():
    # try:
    #     await orm.AsyncORM.insert_names(WomanName, ['Аврора', 'Аза'])
    # except sqlalchemy.exc.IntegrityError as err:
    #     print(err)
    # res = await orm.AsyncORM.get_name(WomanName, 'Белла')
    # print(res)
    # await AsyncORM.delete_all_data(WomanName)
    # await AsyncORM.delete_all_data(ManName)
    ...


if __name__ == '__main__':
    asyncio.run(main())
