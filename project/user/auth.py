from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN, HTTP_401_UNAUTHORIZED

from project.base.message import messages
from project.config import SECRET_KEY, TOKEN_EXPIRE_TIMES, TOKEN_ALGORITHM, TOKEN_TYPE
from project.db_connection import get_db
from project.user.models import User


def generate_token(data: dict):
    expire_time = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_TIMES)
    to_encode = data.copy()
    to_encode.update({'time': float(expire_time.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=TOKEN_ALGORITHM)


def get_current_user(request: Request, db: Session = Depends(get_db)):
    auth_token = request.headers.get('Authorization', None)
    if not auth_token:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail={'message': messages['invalid_user']}
        )

    try:
        token_type, token = auth_token.split(' ')
        if token_type != TOKEN_TYPE:
            raise Exception
        payload = jwt.decode(token, SECRET_KEY, algorithm=TOKEN_ALGORITHM)
        username = payload.get('username')
        expire_time = payload.get('time')
        current_time = datetime.utcnow().timestamp()
        if expire_time < current_time:
            raise Exception
        return db.query(User).filter(User.username == username).one()
    except Exception:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail={'message': messages['invalid_token']})
