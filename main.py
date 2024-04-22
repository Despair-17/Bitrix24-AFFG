import sqlalchemy

from database.query.orm import AsyncORM
from database.models import WomanName, ManName
import asyncio
from os import getenv
from dotenv import load_dotenv

load_dotenv()

from bitrix.bitrix_api import BitrixAPI

api_key = getenv('API_KEY')


async def main():
    # try:
    #     await orm.AsyncORM.insert_names(WomanName, ['Аврора', 'Аза'])
    # except sqlalchemy.exc.IntegrityError as err:
    #     print(err)
    # res = await AsyncORM.get_name(WomanName, 'Аврора')
    # print(res)
    # await AsyncORM.delete_all_data(WomanName)
    # await AsyncORM.delete_all_data(ManName)
    async with BitrixAPI(api_key) as conn:
        #     s1 = await conn.get_contact_data()
        #     print(s1)
        #
        #     s2 = await conn.update_contact_gender('1', 'men')
        #     print(s2)
        # s3 = await conn.add_contact('Борис')
        # print(s3)
        s4 = await conn.get_all_contacts()
        print(s4)
        s4 = await conn.delete_contact('11')
        print(s4)
    ...


if __name__ == '__main__':
    asyncio.run(main())
