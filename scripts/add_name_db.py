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


async def main():
    file_names = [('names_woman.txt', WomanName), ('names_men.txt', ManName)]
    tasks = []
    currdir = os.path.dirname(__file__)
    testdatadir = os.path.join(currdir, '..', 'testdata')
    for name_file, model in file_names:
        path = os.path.join(testdatadir, name_file)
        task = asyncio.create_task(read_file_add_db(path, model))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
