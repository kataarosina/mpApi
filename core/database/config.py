import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL

from core.utils import classproperty

load_dotenv()


class DBConfig:

    DB_DRIVER = os.environ.get('DB_DRIVER')
    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')

    @classproperty
    def database_url(cls) -> URL:
        return URL.create(
            drivername=cls.DB_DRIVER,
            username=cls.DB_USER,
            password=cls.DB_PASS,
            host=cls.DB_HOST,
            port=cls.DB_PORT,
            database=cls.DB_NAME,
        )
