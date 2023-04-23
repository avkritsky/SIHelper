import json

import pytest
from sqlalchemy import select

from src.domain.models import User


@pytest.mark.asyncio
async def test_get_user(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(user_id='0001', chat_id='0001', fullname='avkritksy')

    session.add(user)

    data = client.get('/user?user_id=0001')

    assert data.status_code == 200
    assert data.json().get('data') == user.output

    await session.close()


@pytest.mark.asyncio
async def test_post_user(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(user_id='0001', chat_id='0001', fullname='avkritksy')

    client.post('/user', data=json.dumps(user.output))

    user.id = 1

    data = await session.execute(
        select(User).where(
            User.user_id == user.user_id
        )
    )

    assert data.fetchone()[0] == user

    await session.close()


@pytest.mark.asyncio
async def test_del_user(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(user_id='0001', chat_id='0001', fullname='avkritksy')

    session.add(user)

    data = client.delete('/user?user_id=0001')

    assert data.status_code == 200

    data = await session.execute(
        select(User).where(
            User.user_id == user.user_id
        )
    )

    assert data.fetchone() is None

    await session.close()


@pytest.mark.asyncio
async def test_get_all_users(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(user_id='0001', chat_id='0001', fullname='avkritksy')

    session.add(user)

    data = client.get('/users')

    assert data.status_code == 200
    assert data.json().get('data') == [user.output]

    await session.close()
