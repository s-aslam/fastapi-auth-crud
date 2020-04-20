from copy import deepcopy
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from project.base.message import messages
from project.base.schema import ResponseSchema
from project.db_connection import get_db
from project.user.auth import generate_token, get_current_user
from project.user.models import User
from project.user.schema import SignUpSchema, LogInSchema, LogInResponseSchema, UserSchema

router = APIRouter()


@router.post('/signup', response_model=ResponseSchema)
async def signup(data: SignUpSchema, db: Session = Depends(get_db)):
    error_dict = dict()
    # checking email
    user_email_objects = db.query(User).filter(User.email == data.email).first()
    if user_email_objects:
        error_dict['email'] = messages['email_exists']

    # checking username
    username_objects = db.query(User).filter(User.username == data.username).first()
    if username_objects:
        error_dict['username'] = messages['username_exists']

    if error_dict:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_dict)

    obj = User(**data.__dict__)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {'message': messages['signup_success']}


@router.post('/login', response_model=LogInResponseSchema)
async def login(data: LogInSchema, db: Session = Depends(get_db)):
    try:
        user_object = db.query(User).filter(or_(User.email == data.username,
                                                User.username == data.username)).one()
    except Exception:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=messages['invalid_username'])

    if not user_object.verify_password(data.password):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=messages['invalid_password'])

    if not user_object.is_active:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=messages['inactive_user'])

    token = generate_token({'username': user_object.username})
    user_object_last_login = deepcopy(user_object)
    user_object.last_login = datetime.now()
    db.commit()

    return {
        'token': {'token': token},
        'user': user_object_last_login
    }


@router.get('/profile', response_model=UserSchema)
async def profile(user: User = Depends(get_current_user)):
    return user
