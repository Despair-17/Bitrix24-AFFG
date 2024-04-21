from database.query import orm
from database.models import WomanName, ManName
import asyncio


async def main():
    # await orm.AsyncORM.insert_names(WomanName, ['Аня', 'Белла', 'Настя'])
    # res = await orm.AsyncORM.get_name(WomanName, 'Белла')
    # print(res)
    ...


if __name__ == '__main__':
    asyncio.run(main())
