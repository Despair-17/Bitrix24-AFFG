import asyncio
from os import getenv
from dotenv import load_dotenv

from bitrix.bitrix_api import BitrixAPI

load_dotenv()

API_KEY = getenv('API_KEY')


async def main():
    count = 0
    async with BitrixAPI(API_KEY) as conn:
        contacts_without_gender = await conn.get_contact_data()

        print(len(contacts_without_gender))
        print(contacts_without_gender)


if __name__ == '__main__':
    asyncio.run(main())
