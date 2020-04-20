from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from project.base.models import BaseModel
from project.config import API_PREFIX, PROJECT_NAME
from project.db_connection import engine, Session
from project.route import root_api_router as api_router

# to create tables
BaseModel.metadata.create_all(bind=engine)

# creating FastAPI instance
app = FastAPI(title=PROJECT_NAME, version="0.0.1")

# CORS
origins = ['*']

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(api_router, prefix=API_PREFIX)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    middleware for database connections
    """
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    """
    customizing validation error response for better user experience
    :param request:
    :param exc: contains error in json format
    :return: error json
    """
    data = exc
    try:
        error_dict = {error['loc'][-1]: error['msg'] for error in exc.errors()}
        data = JSONResponse(status_code=400, content={'detail': error_dict})
    except Exception:
        pass
    return data
