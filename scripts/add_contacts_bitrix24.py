import asyncio
import os
import aiofiles

from bitrix.bitrix_api import BitrixAPI

from dotenv import load_dotenv
from os import getenv

load_dotenv()
API_KEY = getenv('API_KEY')


async def read_file(path: str) -> list[str]:
    async with aiofiles.open(path, 'r', encoding='utf-8') as afile:
        names = []
        async for name in afile:
            name: str = name.strip()
            names.append(name)
    return names


async def process_files(file_name: str) -> list[str]:
    currdir = os.path.dirname(__file__)
    testdatadir = os.path.join(currdir, '..', 'testdata')
    path = os.path.join(testdatadir, file_name)
    task = asyncio.create_task(read_file(path))
    return await task


async def main(file_names: list[str]) -> None:
    tasks = [asyncio.create_task(process_files(file_name)) for file_name in file_names]
    result = await asyncio.gather(*tasks)

    async with BitrixAPI(API_KEY, 500) as conn:
        tasks = []
        for list_names in result:
            for name in list_names:
                task = asyncio.create_task(conn.add_contact(name))
                tasks.append(task)
        result = await asyncio.gather(*tasks)
        print(f'Всего добавлено {len(result)} контактов.')


if __name__ == '__main__':
    """Скрипт множественно добавляет контакты в систему Bitrix24, на вход функцию main принимает название файлов с 
    именами, находящиеся в директории testdata. Благодаря асинхронности можно добавлять большие объемы данных очень 
    быстро, класс BitrixAPI принимает на вход ограничение количества одновременных запросов, можно увеличить или 
    уменьшить в зависимости от ограничений API Bitrix24, по умолчанию 100"""

    file_names_with_data = ['names_woman.txt', 'names_men.txt']
    asyncio.run(main(file_names_with_data))
