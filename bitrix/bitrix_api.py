import asyncio
import aiohttp

from typing import Any


class BitrixAPI:

    def __init__(self, api_key: str, max_connect: int = 1000):
        """api_key - вебхук bitrix24, max_connect - ограничение на количество одновременных запросов к bitrix24 на
        изменения обращения (гендера)"""
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

    async def get_contact_data(self) -> list[dict[str, Any]] | tuple[None, int]:
        """Метод отправляет GET запрос к Bitrix24 получает JSON ответ, в котором содержатся все контакты без обращений
        (гендера) и возвращает список из словарей, содержащие эти контакты, либо кортеж из None и кода ответа."""
        params = {
            'filter[HONORIFIC]': '',
            'select[]': ['ID', 'NAME'],
        }

        async with self._session.get(self._get_contacts_url, params=params) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response.get('result')
            return None, response.status

    async def update_contact_gender(self, pk: str, gender: str) -> bool | tuple[None, int]:
        """Метод отправляет POST запрос к Bitrix24 на изменение обращения (гендера) контакта. pk - это id контакта на
        Bitrix24, gender - это обращение (women - г-жа), (men - г-н), возвращает при статусе ответа 200 True/False
        при ином кортеж из None и кода ответа."""
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
                return None, response.status

    async def add_contact(self, name: str) -> int | tuple[None, int]:
        """Метод отправляет POST запрос к Bitrix24 на добавление контакта, возвращает при статусе ответа 200 id -
        контакта при ином кортеж из None и кода ответа. (В тех. задании не требуется, но нужен для текстов)."""
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
                return None, response.status

    async def get_all_contacts(self) -> bool | tuple[None, int]:
        """Метод возвращает все контакты с Bitrix24 их id и name. (В тех. задании не требуется, но нужен для текстов)"""
        params = {
            'select[]': ['ID', "name"],
        }
        async with self._session.get(self._get_contacts_url, params=params) as response:
            if response.status == 200:
                json_response = await response.json()
                return json_response.get('result')
            return None, response.status

    async def delete_contact(self, pk: str) -> bool | tuple[None, int]:
        """Метод удаляет контакт с Bitrix24 по id. (В тех. задании не требуется, но нужен для текстов)"""
        data = {
            "ID": pk,
        }
        async with self._semaphore:
            async with self._session.post(self._delete_contact_url, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    return json_response.get('result')
                return None, response.status
