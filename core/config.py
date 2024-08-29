import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_HASHING_ALGORITHM = os.environ.get('JWT_HASHING_ALGORITHM')
    JWT_ACCESS_TOKEN_TTL_MINUTES = int(os.environ.get('JWT_ACCESS_TOKEN_TTL_MINUTES'))
