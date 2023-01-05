from api.database.models import User
from api.schemas.user import CreateUser


async def add_user_db(user: CreateUser) -> User:
    u = User(**user.dict())
    return await u.save()


async def get_user_db(tg_id: int) -> User | None:
    return await User.objects.select_related(['records', 'files']).get_or_none(id=tg_id)


async def get_user_by_id_db(_id: int) -> User | None:
    return await User.objects.select_related(['records', 'files']).get_or_none(id=_id)


async def get_user_all_db(skip: int = 0, limit: int = 100) -> list[User]:
    return await User.objects.limit(limit).offset(skip).select_related(['records', 'files']).all()
