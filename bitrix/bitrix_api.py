import asyncio
import aiohttp

from typing import Any


class BitrixAPI:

    def __init__(self, api_key: str, max_connect: int = 100):
        """api_key - вебхук bitrix24, max_connect - ограничение на количество одновременных запросов к Bitrix24"""
        self._semaphore = asyncio.Semaphore(max_connect)
        self._get_contacts_url = f'{api_key}crm.contact.list.json'
        self._update_contact_url = f'{api_key}crm.contact.update.json'
        self._add_contact_url = f'{api_key}crm.contact.add.json'
        self._delete_contact_url = f'{api_key}crm.contact.delete.json'

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    async def get_contact_data(self, without_gender: bool = True) -> list[dict[str, Any]]:
        """Метод отправляет GET запрос к Bitrix24 получает JSON ответ, в котором содержатся все контакты без обращений
        (гендера) и возвращает список из словарей, содержащие эти контакты. Флаг without_gender - если True, то
        возвращает все, иначе только без обращения"""
        all_contacts = []
        start = 0
        limit = 50
        total = float('inf')

        params = {
            'start': start,
            'select[]': ['ID', 'NAME'],
        }
        if without_gender:
            params['filter[HONORIFIC]'] = ''

        while len(all_contacts) < total:
            async with self._session.get(self._get_contacts_url, params=params) as response:
                if response.status == 200:
                    json_response = await response.json()
                    total = json_response.get('total')
                    all_contacts.extend(json_response.get('result'))
                    params['start'] += limit
                else:
                    raise aiohttp.ClientResponseError(response.request_info, history=tuple(), status=response.status)

        return all_contacts

    async def update_contact_gender(self, pk: str, gender: str) -> bool:
        """Метод отправляет POST запрос к Bitrix24 на изменение обращения (гендера) контакта. pk - это id контакта на
        Bitrix24, gender - это обращение (women - г-жа), (men - г-н), возвращает при статусе ответа 200 True/False
        """
        gender = 'HNR_RU_2' if gender == 'woman' else 'HNR_RU_1'
        data = {
            'ID': pk,
            'fields':
                {
                    'HONORIFIC': gender,
                }
        }

        async with self._semaphore:
            async with self._session.post(self._update_contact_url, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    return json_response.get('result')
                raise aiohttp.ClientResponseError(response.request_info, history=tuple(), status=response.status)

    async def add_contact(self, name: str) -> int:
        """Метод отправляет POST запрос к Bitrix24 на добавление контакта, возвращает при статусе ответа 200 id
        контакта. (В тех. задании не требуется, но нужен для текстов)."""
        data = {
            "fields":
                {
                    "NAME": name,
                }
        }

        async with self._semaphore:
            async with self._session.post(self._add_contact_url, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    pk = json_response.get('result')
                    return pk
                raise aiohttp.ClientResponseError(response.request_info, history=tuple(), status=response.status)

    async def delete_contact(self, pk: str) -> bool:
        """Метод удаляет контакт с Bitrix24 по id. (В тех. задании не требуется, но нужен для текстов)"""
        data = {
            "ID": pk,
        }

        async with self._semaphore:
            async with self._session.post(self._delete_contact_url, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    return json_response.get('result')
                raise aiohttp.ClientResponseError(response.request_info, history=tuple(), status=response.status)
