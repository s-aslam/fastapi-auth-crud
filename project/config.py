import os
from pathlib import Path

from dotenv import load_dotenv
from passlib.context import CryptContext

env_path = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/.env')
load_dotenv(dotenv_path=env_path)

API_PREFIX = '/api'

SECRET_KEY = os.getenv("SECRET_KEY")

DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# to run test cases
TEST_DB_NAME = 'test_{0}'.format(DB_NAME)
TEST_DATABASE_URI = (
    f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 10

PROJECT_NAME = 'Fast API '

PASSWORD_ENCRYPTION = CryptContext(schemes=["bcrypt"], deprecated="auto")

TOKEN_EXPIRE_TIMES = 24  # in hours
TOKEN_ALGORITHM = "HS512"
TOKEN_TYPE = 'Bearer'
