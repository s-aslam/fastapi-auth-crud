import pytest
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from project.base.message import messages
from project.items.api import create_item, get_item, update_item, list_item, delete_item
from project.items.schema import CreateItemSchema, ItemSchema


def test_create_item(run, db, user):
    """
    Test create status with valid arguments
    """
    data = CreateItemSchema(title="Item1", description="Lorem Ipsum")
    response = run(create_item(data, db, user))
    assert ItemSchema(**response.__dict__).title == data.title


def test_create_item_title_exists(run, db, user):
    """
    Test create status with valid arguments
    """
    data = CreateItemSchema(title="Item1", description="Lorem Ipsum")
    with pytest.raises(HTTPException) as error:
        run(create_item(data, db, user))
    assert error.value.status_code == HTTP_400_BAD_REQUEST


def test_create_new_item(run, db, user):
    """
    Test create status with valid arguments
    """
    data = CreateItemSchema(title="Item2", description="Lorem Ipsum")
    response = run(create_item(data, db, user))
    assert ItemSchema(**response.__dict__).title == data.title


def test_get_item(run, db, user):
    item_id = 1
    response = run(get_item(item_id, db, user))
    assert ItemSchema(**response.__dict__).id == item_id


def test_get_item_with_invalid_id(run, db, user):
    """
    Test get item with invalid value
    """
    with pytest.raises(HTTPException) as error:
        run(get_item(10000, db, user))
    assert error.value.status_code == HTTP_404_NOT_FOUND


def test_update_item_with_invalid_id(run, db, user):
    data = CreateItemSchema(title="NewItem", description="Description")
    item_id = 100
    with pytest.raises(HTTPException) as error:
        run(update_item(item_id, data, db, user))
    assert error.value.status_code == HTTP_404_NOT_FOUND


def test_update_item(run, db, user):
    data = CreateItemSchema(title="NewItem", description="Description")
    item_id = 1
    response = run(update_item(item_id, data, db, user))
    assert ItemSchema(**response.__dict__).title == data.title
    assert ItemSchema(**response.__dict__).description == data.description


def test_update_item_with_title_exists(run, db, user):
    data = CreateItemSchema(title="Item2", description="Description")
    item_id = 1
    with pytest.raises(HTTPException) as error:
        run(update_item(item_id, data, db, user))
    assert error.value.status_code == HTTP_400_BAD_REQUEST


def test_list_item(run, db, user):
    """
    Test list item
    """
    response = run(list_item(db, current_user=user))
    assert 'count' in response
    assert 'data' in response


def test_list_status_with_limit(run, db, user):
    """
    Test list item with limit
    """
    limit = 2
    response = run(list_item(db, limit=limit, current_user=user))
    assert 'count' in response
    assert len(response.get('data')) <= limit


def test_list_item_with_search_text(run, db, user):
    """
    Test list item with search
    """
    search_text = 'Item'
    response = run(list_item(db, search=search_text, current_user=user))
    data = response.get('data')[0]
    schema = ItemSchema(**data.__dict__)
    assert search_text in schema.title


def test_delete_item(run, db, user):
    """
    Test delete item with valid value
    """
    item_id = 1
    response = run(delete_item(item_id, db, current_user=user))
    assert response.get('detail', {}).get('message') == messages['delete_success']


def test_delete_item_with_invalid_id(run, db, user):
    """
    Test delete item with invalid value
    """
    with pytest.raises(HTTPException) as error:
        run(delete_item(10000, db, user))
    assert error.value.status_code == HTTP_404_NOT_FOUND
