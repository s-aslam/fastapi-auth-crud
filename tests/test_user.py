import pytest
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from project.base.message import messages
from project.base.schema import ResponseSchema
from project.user.api import signup, login, profile
from project.user.schema import SignUpSchema, LogInSchema, LogInResponseSchema


def test_signup(run, db):
    data = SignUpSchema(email='test1@example.com', username='test1', first_name='Test', last_name='Test',
                        password='123123')
    response = run(signup(data, db))
    assert ResponseSchema(**response).message == messages['signup_success']


def test_signup_username_exists(run, db):
    data = SignUpSchema(email='test2@example.com', username='test1', first_name='Test', last_name='Test',
                        password='123123')
    with pytest.raises(HTTPException) as error:
        run(signup(data, db))
    assert error.value.detail.get('username') == messages['username_exists']
    assert error.value.status_code == HTTP_400_BAD_REQUEST


def test_signup_email_exists(run, db):
    data = SignUpSchema(email='test1@example.com', username='test12', first_name='Test', last_name='Test',
                        password='123123')
    with pytest.raises(HTTPException) as error:
        run(signup(data, db))
    assert error.value.detail.get('email') == messages['email_exists']
    assert error.value.status_code == HTTP_400_BAD_REQUEST


def test_login_with_invalid_username(run, db):
    data = LogInSchema(username='test12', password='123123')
    with pytest.raises(HTTPException) as error:
        run(login(data, db))
    assert error.value.status_code == HTTP_404_NOT_FOUND


def test_login_with_invalid_email(run, db):
    data = LogInSchema(username='test12@test.com', password='123899')
    with pytest.raises(HTTPException) as error:
        run(login(data, db))
    assert error.value.status_code == HTTP_404_NOT_FOUND


def test_login_with_invalid_password(run, db):
    data = LogInSchema(username='test', password='123899')
    with pytest.raises(HTTPException) as error:
        run(login(data, db))
    assert error.value.status_code == HTTP_401_UNAUTHORIZED


def test_login(run, db):
    data = LogInSchema(username='test', password='123123')
    response = run(login(data, db))
    assert 'token' in LogInResponseSchema(**response).token.dict().keys()
    assert LogInResponseSchema(**response).user.username == data.username


def test_profile(run, user):
    response = run(profile(user))
    assert 'username' in dict(response).keys()
