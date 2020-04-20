import asyncio
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

from project.base.message import messages
from project.base.models import BaseModel
from project.base.schema import ResponseSchema
from project.config import TEST_DATABASE_URI
from project.user.api import signup, login
from project.user.schema import SignUpSchema, LogInSchema, LogInResponseSchema


@pytest.fixture(scope="session", autouse=True)
def db(request):
    engine = create_engine(TEST_DATABASE_URI)
    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)

    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    BaseModel.metadata.create_all(bind=engine)
    db_session = session()

    def end():
        drop_database(engine.url)
        db_session.close()

    request.addfinalizer(end)
    return db_session


@pytest.fixture(scope="session")
def run(request):
    loop = asyncio.get_event_loop()

    def end():
        loop.close()

    request.addfinalizer(end)
    return loop.run_until_complete


@pytest.fixture(scope="session", autouse=True)
def user(run, db):
    data = SignUpSchema(email='test@example.com', username='test', first_name='Test', last_name='Test',
                        password='123123')
    response = run(signup(data, db))
    assert ResponseSchema(**response).message == messages['signup_success']
    login_data = LogInSchema(username='test', password='123123')
    login_response = run(login(login_data, db))
    assert LogInResponseSchema(**login_response).user.username == login_data.username
    return LogInResponseSchema(**login_response).user
