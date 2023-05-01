import json

import pytest

from src.domain.models import User


@pytest.mark.asyncio
async def test_get_user(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(tg_id='0001', chat_id='0001', fullname='avkritksy')

    session.add(user)

    data = client.get('/user?tg_id=0001')

    assert data.status_code == 200
    assert data.json().get('data') == user.output

    await session.close()


@pytest.mark.asyncio
async def test_post_user(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(tg_id='0001', chat_id='0001', fullname='avkritksy')
    user.id = 1

    client.post('/user', data=json.dumps(user.output))

    data = client.get('/user?tg_id=0001')

    data = data.json().get('data')

    assert data == user.output

    await session.close()


@pytest.mark.asyncio
async def test_del_user(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(tg_id='0001', chat_id='0001', fullname='avkritksy')

    client.post('/user', data=json.dumps(user.output))

    data = client.delete(f'/user?tg_id={user.tg_id}')

    assert data.status_code == 200

    data = client.get(f'/user?tg_id={user.tg_id}')

    data = data.json().get('data')

    assert data is None

    await session.close()


@pytest.mark.asyncio
async def test_get_all_users(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(tg_id='0001', chat_id='0001', fullname='avkritksy')

    session.add(user)

    data = client.get('/user/all')

    assert data.status_code == 200
    assert data.json().get('data') == [user.output]

    await session.close()
