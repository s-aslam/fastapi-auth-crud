from pydantic import BaseModel

from project.base.schema import BaseSchema


class CreateItemSchema(BaseModel):
    title: str = None
    description: str = None


class ItemSchema(CreateItemSchema, BaseSchema):
    pass
