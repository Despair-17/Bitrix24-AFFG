import asyncio
import aiohttp

from os import getenv
from dotenv import load_dotenv

from bitrix.bitrix_api import BitrixAPI
from database.query.orm import AsyncORM
from database.models import WomanName, ManName

load_dotenv()
API_KEY = getenv('API_KEY')


async def check_name_in_database(contact: dict[str, str]) -> dict[str, str]:
    name = contact['NAME']
    woman_name = await AsyncORM.get_name(WomanName, name)
    if woman_name:
        contact['gender'] = 'woman'
        return contact

    men_name = await AsyncORM.get_name(ManName, name)
    if men_name:
        contact['gender'] = 'men'
        return contact

    contact['gender'] = ''
    return contact


async def main():
    print(f'Запуск приложения...')
    async with BitrixAPI(API_KEY, 100) as conn:
        contacts_without_gender = await conn.get_contact_data()
        print(f'Контакты получены с Bitrix24...')
        tasks = []
        for contact in contacts_without_gender:
            task = asyncio.create_task(check_name_in_database(contact))
            tasks.append(task)

        count_contacts_without_gender = len(contacts_without_gender)
        del contacts_without_gender

        contacts_with_gender = await asyncio.gather(*tasks)
        print(f'Контакты обработаны в приложении...')

        tasks = []
        for contact in contacts_with_gender:
            pk, gender = contact['ID'], contact['gender']
            task = asyncio.create_task(conn.update_contact_gender(pk, gender))
            tasks.append(task)

        try:
            result = await asyncio.gather(*tasks)
            print(f'Добавлено обращений {sum(result)} из {count_contacts_without_gender} контактам.')
        except aiohttp.ClientResponseError as err:
            print(err)


if __name__ == '__main__':
    asyncio.run(main())
