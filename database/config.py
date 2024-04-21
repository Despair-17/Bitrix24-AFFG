from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def get_url_database(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings(
    getenv('DB_HOST'),
    getenv('DB_PORT'),
    getenv('DB_USER'),
    getenv('DB_PASS'),
    getenv('DB_NAME'),
)
