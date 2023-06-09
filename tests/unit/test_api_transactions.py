import json

import pytest

from src.domain.models import User


@pytest.mark.asyncio
async def test_get_transaction(client_test, create_db):
    client, session = client_test

    await create_db(session)

    user = User(tg_id='0001', chat_id='0001', fullname='avkritksy')

    session.add(user)

    transaction = dict(
        tg_id='0001',
        target_currency='BTC',
        target_value='0.001',
        from_currency='USDT',
        from_value='30',
    )

    data = client.post('/transaction', data=json.dumps(transaction))

    assert data.status_code == 200

    data = client.get('/transaction/?tg_id=0001')

    from_db = data.json().get('data')

    for item in from_db:
        for key in transaction:
            if key in item:
                assert transaction[key] == item[key]

    data = client.delete('/transaction/?trans_id=1')

    assert data.status_code == 200
    assert data.json().get('data') == 'Delete transaction #1'

    await session.close()


@pytest.mark.asyncio
async def test_get_all_transactions(client_test, create_db):
    client, session = client_test

    transactions_count = 3
    await create_db(session)

    user = User(tg_id='0001', chat_id='0001', fullname='avkritksy')
    session.add(user)

    user = User(tg_id='0002', chat_id='0001', fullname='avkritksy')
    session.add(user)

    for _ in range(transactions_count):
        transaction = dict(
            tg_id='0001',
            target_currency='BTC',
            target_value='0.001',
            from_currency='USDT',
            from_value='30',
        )
        data = client.post('/transaction', data=json.dumps(transaction))

        assert data.status_code == 200

    # add transaction for another user
    transaction = dict(
        tg_id='0002',
        target_currency='BTC',
        target_value='0.001',
        from_currency='USDT',
        from_value='30',
    )
    client.post('/transaction', data=json.dumps(transaction))

    data = client.get('/transaction/?tg_id=0001')

    from_db = data.json().get('data')

    assert isinstance(from_db, list)
    assert len(from_db) == transactions_count

    await session.close()