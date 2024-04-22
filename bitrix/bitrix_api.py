import asyncio
import aiohttp

from typing import Any


class BitrixAPI:

    def __init__(self, api_key: str, max_connect: int = 1000):
        """api_key - вебхук bitrix24, max_connect - ограничение на количество одновременных запросов к bitrix24 на
        изменения обращения (гендера)"""
        self._semaphore = asyncio.Semaphore(max_connect)
        self._get_contacts_url = f'{api_key}crm.contact.list.json'
        self._post_contact_url = f'{api_key}crm.contact.update.json'

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def get_contact_data(self) -> list[dict[str, Any]] | None:
        """Метод отправляет GET запрос к Bitrix24 получает JSON ответ, в котором содержатся все контакты без обращений
        (гендера) и возвращает список из словарей, содержащие эти контакты, либо None если статус ответа не 200"""
        params = {
            'filter[HONORIFIC]': '',
            'select[]': ['ID', 'NAME'],
        }

        async with self._session.get(self._get_contacts_url, params=params) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response.get('result')
            return None

    async def update_contact_gender(self, pk: str, gender: str) -> bool | None:
        """Метод отправляет POST запрос к Bitrix24 на изменение обращения (гендера) контакта. pk - это id контакта на
        Bitrix24, gender - это обращение (women - г-жа), (men - г-н), возвращает при статусе ответа 200 True/False
        при ином статусе None"""
        gender = 'HNR_RU_2' if gender == 'woman' else 'HNR_RU_1'
        data = {
            'ID': pk,
            'fields':
                {
                    'HONORIFIC': gender
                }
        }

        async with self._semaphore:
            async with self._session.post(self._post_contact_url, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    return json_response.get('result')
                return None
