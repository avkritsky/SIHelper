from fastapi import APIRouter, Response

from src.domain import models


router = APIRouter(
    prefix='/',
    tags=['/'],
    responses={404: {'description': 'Not found'}}
)


@router.post('/user')
async def add_user(user: models.User) -> Response:
    """Create new user in DB"""
    ...
