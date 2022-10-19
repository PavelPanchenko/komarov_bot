from api.database.base import SessionLocal
from api.database.models import User
from api.schemas.user import CreateUser


def add_user_db(item: CreateUser):
    with SessionLocal() as session:
        user = User(**item.dict())
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_db(tg_id: int):
    with SessionLocal() as session:
        return session.query(User).filter(User.tg_id == tg_id).one_or_none()


def get_user_by_id_db(_id: int):
    with SessionLocal() as session:
        return session.query(User).filter(User.id == _id).one_or_none()


def get_user_all_db(skip: int = 0, limit: int = 100):
    with SessionLocal() as session:
        return session.query(User).limit(limit).offset(skip).all()


async def update_user_db(tg_id: int, is_recorded_by: bool):
    with SessionLocal() as session:
        user = session.query(User).filter(User.tg_id == tg_id).update({User.is_recorded_by: is_recorded_by})
        session.commit()
        session.refresh(user)
        return user
