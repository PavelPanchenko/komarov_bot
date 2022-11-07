import datetime

from pydantic import BaseModel


class RecordBase(BaseModel):
    location: str
    date_time: str
    user_id: int
    service: str
    confirmation: bool = False

    class Config:
        orm_mode = True


class RecordItem(RecordBase):
    id: int


class CreateRecord(RecordBase):
    pass

