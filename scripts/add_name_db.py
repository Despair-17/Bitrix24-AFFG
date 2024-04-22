import asyncio
import aiofiles
import os
from typing import Type
import sqlalchemy

from database.query.orm import AsyncORM
from database.models import WomanName, ManName


async def read_file_add_db(path: str, model: Type[WomanName | ManName]) -> None:
    async with aiofiles.open(path, 'r', encoding='utf-8') as afile:
        names = []
        async for name in afile:
            name: str = name.strip()
            names.append(name)

    try:
        await AsyncORM.insert_names(model, names)
    except sqlalchemy.exc.IntegrityError as err:
        print(err)


async def main(file_names: list[tuple[str, Type[WomanName | ManName]]]):
    tasks = []
    currdir = os.path.dirname(__file__)
    testdatadir = os.path.join(currdir, '..', 'testdata')
    for name_file, model in file_names:
        path = os.path.join(testdatadir, name_file)
        task = asyncio.create_task(read_file_add_db(path, model))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    """Скрипт добавляет в БД имена из файлов в папке testdata, функция main на вход принимает список с кортежами, где
    первый элемент название файла, второй это обращение (гендер) представляющие из себя классы модели ORM: WomanName - 
    женское имя, ManName - мужские имена. Благодаря асинхронности можно добавлять огромные объемы данных очень быстро"""

    file_names_with_data = [('names_woman.txt', WomanName), ('names_men.txt', ManName)]
    asyncio.run(main(file_names_with_data))
