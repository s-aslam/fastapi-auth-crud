from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from starlette.requests import Request

from project.config import DATABASE_URI

engine = create_engine(DATABASE_URI, pool_pre_ping=True)

# creating db if not exists
if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class CustomBase(object):
    # Generate table name automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


Base = declarative_base(cls=CustomBase)


def get_db(request: Request):
    return request.state.db
