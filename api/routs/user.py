from fastapi import APIRouter

from api.database.models import User
from api.database.user import get_user_all_db, get_user_db
from api.schemas.user import UserItem

users_rout = APIRouter(prefix='/users')


@users_rout.get('', response_model=list[UserItem], tags=['Пользователи'], name='Список Пользователей')
async def list_users(skip: int = 0, limit: int = 100):
    return await get_user_all_db(skip, limit)


@users_rout.get('/{tg_id}', response_model=UserItem | None, tags=['Пользователи'], name='Пользователь по ID telegram')
async def get_user(tg_id: int):
    return await get_user_db(tg_id=tg_id)
