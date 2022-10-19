import datetime
from pydantic import BaseModel

from api.schemas.record import RecordItem


class UserBase(BaseModel):
    tg_id: int
    fullname: str
    phone_number: str

    class Config:
        orm_mode = True


class UserItem(UserBase):
    id: int
    create_at: datetime.datetime


class CreateUser(UserBase):
    pass


