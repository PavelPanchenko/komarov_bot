import datetime
from pydantic import BaseModel

from api.database.models import Record, UserFile
from api.schemas.record import RecordItem


class UserBase(BaseModel):
    id: int
    full_name: str
    phone_number: str

    class Config:
        orm_mode = True


class UserItem(UserBase):
    created_at: datetime.datetime
    records: list[Record] = []
    files: list[UserFile] = []


class CreateUser(UserBase):
    pass
