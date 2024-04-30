# Bitrix24-AFFG

Приложение заполняет поле обращение (пол) асинхронно, всем контактам в системе Bitrix24 у которых это поле пустое,
определение обращения осуществляется с помощью базы данных с именами, если в БД (базе данных) имени нет, то обращение добавлено
не будет. 

## Установка и запуск
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Despair-17/Bitrix24-AFFG.git
   ```
2. Создайте виртуальное окружение:
   ```bash
   python3 -m venv venv
   venv\Scripts\activate.bat на Windows
   source venv/bin/activate на Linux
   ```
3. Установите зависимости
   ```bash
   pip install -r requirements.txt
   ```
4. Создайте файл .env в корне и добавте в него:
   ```bash
   DB_HOST - хост БД
   DB_PORT - порт БД
   DB_USER - логин пользователя БД
   DB_PASS - пароль пользователя БД
   DB_NAME - название БД (создайте БД если её нет)
   API_KEY - Вебхук Bitrix24
   ```
5. Сделайте миграции для создания таблиц:
   ```bash
   alembic revision --autogenerate
   alembic upgrade head
   ```
6. Запуск приложения из корневой папки:
   ```bash
   python main.py
   ```
### Дополнительно
В scripts содержатся python скрипты для добавления, удаления тестовых данных в систему Bitrix24 и в БД приложения: add_contacts_bitrix24.py, add_name_db.py, delete_contacts_bitrix24.py.
   ```bash
   python ./scripts/add_contacts_bitrix24.py
   python ./scripts/add_name_db.py
   python ./scripts/delete_contacts_bitrix24.py
   ```
**Использовать add_contacts_bitrix24 и delete_contacts_bitrix24 только на пустом аккаунте, для теста работы приложения, иначе можно добавить лишнего или удалить с аккаунта важные данные, add_name_db безопасен, он лишь добавляет имена в БД приложения.**
