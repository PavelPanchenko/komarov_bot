import datetime
from typing import Optional

import databases
import ormar
import sqlalchemy

from settings.config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = "users"
        orm_mode = True

    id: int = ormar.Integer(primary_key=True, autoincrement=False)
    full_name: str = ormar.String(max_length=100)
    phone_number: str = ormar.String(max_length=15)
    created_at: datetime = ormar.DateTime(default=datetime.datetime.utcnow())


class Record(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = "records"
        orm_mode = True

    id: int = ormar.Integer(primary_key=True)
    location: str = ormar.String(max_length=100)
    date_time: datetime = ormar.DateTime()
    service: str = ormar.String(max_length=100)
    confirmation: bool = ormar.Boolean(default=False)
    user_id: User = ormar.ForeignKey(User, related_name='records')


class UserFile(ormar.Model):
    class Meta(BaseMeta):
        tablename: str = "files"
        orm_mode = True

    id: int = ormar.Integer(primary_key=True)

    file_name: str = ormar.String(max_length=150)
    file_path: str = ormar.String(max_length=100)
    file_size: str = ormar.String(max_length=30)
    user_id: Optional[User] = ormar.ForeignKey(User, related_name='files')
