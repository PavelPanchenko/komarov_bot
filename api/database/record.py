from api.database.base import SessionLocal
from api.database.models import Record
from api.database.user import get_user_db
from pydantic import BaseModel
from api.schemas.record import CreateRecord, RecordItem


def add_record_db(data: CreateRecord):
    with SessionLocal() as session:
        record = Record(**data.dict())
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


def get_record_by_tg_db(tg_id: int) -> list[RecordItem] | list:
    with SessionLocal() as session:
        user = get_user_db(tg_id)
        return session.query(Record).filter(Record.user_id == user.id).all() if user else []


class RecordByID(BaseModel):
    record: RecordItem
    user: int


def get_record_by_id_db(record_id: int) -> RecordByID | None:
    with SessionLocal() as session:
        record = session.query(Record).filter(Record.id == record_id).one_or_none()
        if record:
            return RecordByID(record=record, user=record.users.tg_id)
        return None


def get_record_all_db(sort: str = None) -> list[RecordItem] | list:
    with SessionLocal() as session:
        if sort == 'confirmed':
            return session.query(Record).where(Record.confirmation == 1).order_by('date_time').all()

        if sort == 'not_confirmed':
            return session.query(Record).where(Record.confirmation == 0).order_by('date_time').all()

        return session.query(Record).order_by('date_time').all()


def update_record_db(record_id: int, confirmation: bool):
    with SessionLocal() as session:
        record = session.query(Record) \
            .filter(Record.id == record_id) \
            .update({Record.confirmation: confirmation})
        session.commit()
        return record


def delete_record_db(record_id: int):
    with SessionLocal() as session:
        record = session.query(Record).filter(Record.id == record_id).delete()
        session.commit()
        return record
