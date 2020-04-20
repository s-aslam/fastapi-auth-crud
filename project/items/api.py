from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from starlette.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from project.base.message import messages
from project.base.schema import BaseListSchema
from project.db_connection import get_db
from project.items.models import Item
from project.items.schema import CreateItemSchema, ItemSchema
from project.user.auth import get_current_user
from project.user.models import User

router = APIRouter()


@router.get('', response_model=BaseListSchema[ItemSchema])
async def list_item(db: Session = Depends(get_db), limit: int = 10, offset: int = 0, search: str = None,
                    current_user: User = Depends(get_current_user)):
    """
    Retrieve All Item.
    """

    return_data = dict()
    if search:
        searchable_fields = ['title', ]
        query_condition = tuple(Item.__dict__.get(field).ilike('%{0}%'.format(search))
                                for field in searchable_fields)
        return_data['data'] = db.query(Item).filter(Item.user_id == current_user.id, Item.is_active,
                                                    or_(*query_condition)).limit(limit).offset(offset).all()
        return_data['count'] = db.query(Item).filter(Item.user_id == current_user.id, Item.is_active,
                                                     or_(*query_condition)).count()
        return return_data
    return_data['data'] = db.query(Item).filter(Item.user_id == current_user.id,
                                                Item.is_active).limit(limit).offset(offset).all()
    return_data['count'] = db.query(Item).filter(Item.user_id == current_user.id, Item.is_active).count()
    return return_data


@router.post('', response_model=ItemSchema)
async def create_item(data: CreateItemSchema, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Create new Item.
    """
    item_obj = db.query(Item).filter(Item.title.ilike(f'{data.title}')).first()

    if item_obj:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail={'title': messages['item_exists']})

    obj = Item(**data.__dict__, user_id=current_user.id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.put('/{id}', response_model=ItemSchema)
async def update_item(id: int, data: CreateItemSchema, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    """
    Update an existing Item.
    """
    try:
        obj = db.query(Item).filter(Item.id == id, Item.user_id == current_user.id, Item.is_active).one()

        title_obj = db.query(Item).filter(Item.id != id, Item.title == data.title).first()
        if title_obj:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail={'message': messages['item_exists']})

        data = data.dict(skip_defaults=True)
        for field in jsonable_encoder(obj):
            if field in data:
                setattr(obj, field, data[field])
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
    except NoResultFound:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': messages['no_records']})


@router.patch('/{id}', description='To make active/inactive item')
async def change_item(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get status by ID.
    """
    try:
        obj = db.query(Item).filter(Item.id == id, Item.user_id == current_user.id).one()
        obj.is_active = False if obj.is_active else True
        db.commit()
        db.refresh(obj)
        return {'detail': {'message': messages['success']}}
    except NoResultFound:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': messages['no_records']})


@router.get('/{id}', response_model=ItemSchema)
async def get_item(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Get status by ID.
    """
    try:
        return db.query(Item).filter(Item.id == id, Item.user_id == current_user.id, Item.is_active).one()
    except NoResultFound:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': messages['no_records']})


@router.delete('/{id}')
async def delete_item(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Delete Item.
    """
    try:
        obj = db.query(Item).filter(Item.id == id, Item.user_id == current_user.id).one()
        db.delete(obj)
        db.commit()
        return {'detail': {'message': messages['delete_success']}}
    except NoResultFound:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': messages['no_records']})
