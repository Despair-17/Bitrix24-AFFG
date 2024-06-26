import asyncio

from bitrix.bitrix_api import BitrixAPI

from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_KEY = getenv('API_KEY')


async def main():
    async with BitrixAPI(API_KEY, 100) as conn:
        contacts = await conn.get_contact_data(without_gender=False)
        print(len(contacts))
        tasks = []
        for contact in contacts:
            pk = contact['ID']
            task = asyncio.create_task(conn.delete_contact(pk))
            tasks.append(task)

        result = await asyncio.gather(*tasks)
        print(f'Всего удалено {sum(result)} из {len(contacts)} контактов.')


if __name__ == '__main__':
    """Скрипт удаляет все контакты из системы Bitrix24. Благодаря асинхронности можно удалять большие объемы данных 
    очень быстро, класс BitrixAPI принимает на вход ограничение количества одновременных запросов, можно увеличить или 
    уменьшить в зависимости от ограничений API Bitrix24, по умолчанию 100."""
    asyncio.run(main())
