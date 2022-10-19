from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from api.database.record import get_record_by_id_db, get_record_by_tg_db
from api.schemas.record import RecordItem
from loader import bot

from api.database import record
from utils.types import RecordSort
from utils.variables import success_confirm_record

records_rout = APIRouter(prefix='/record')


@records_rout.get('s', response_model=list[RecordItem], tags=['Записи'], name='Записи')
async def list_records(
        sort: Optional[RecordSort] = Query(default=None, description='not_confirmed | confirmed', title='Params:')):
    if sort:
        return record.get_record_all_db(sort.name)
    return record.get_record_all_db()


@records_rout.get('s/{tg_id}', tags=['Записи'], name='Все записи пользователя')
async def get_record(tg_id: int) -> list:
    return record.get_record_by_tg_db(tg_id=tg_id)


@records_rout.get('/{record_id}', tags=['Записи'], name='Запись пользователя по ID')
async def get_record(record_id: int):
    return record.get_record_by_id_db(record_id=record_id)


@records_rout.patch('/{record_id}', tags=['Записи'], name='Подтвердить запись')
async def confirmation(record_id: int, msg: str = None):
    rc = get_record_by_id_db(record_id)
    if rc['record'].confirmation:
        raise HTTPException(status_code=status.HTTP_200_OK, detail='Запись уже была подтверждена')

    record.update_record_db(record_id, True)

    await bot.send_message(chat_id=rc['user'],
                           text=msg if msg else success_confirm_record.format(rc['record'].date_time))
    return status.HTTP_200_OK


@records_rout.delete('/{record_id}', tags=['Записи'], name='Удалить запись')
async def delete_record(record_id: int):
    record.delete_record_db(record_id)
    return {}
