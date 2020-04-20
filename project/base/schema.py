from datetime import datetime
from typing import List, Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class BaseSchema(BaseModel):
    id: int
    is_active: bool = False
    created_at: datetime
    updated_at: datetime = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


T = TypeVar('T', bound=BaseSchema)


class BaseListSchema(GenericModel, Generic[T]):
    data: List[T]
    count: int = 0

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class ResponseSchema(BaseModel):
    message: str
