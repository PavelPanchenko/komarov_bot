from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from api.database.models import Record
from api.database.record import get_record_by_id_db, get_record_by_tg_db, get_record_all_db, update_record_db, \
    delete_record_db
from loader import bot

from utils.static_data import files
from utils.types import RecordSort
from utils.variables import success_confirm_record

records_rout = APIRouter(prefix='/record')


@records_rout.get('s', response_model=list[Record], tags=['Записи'], name='Записи')
async def list_records(
        sort: Optional[RecordSort] = Query(default=None, description='not_confirmed | confirmed', title='Params:')):
    if sort:
        return await get_record_all_db(sort.name)
    return await get_record_all_db()


@records_rout.get('s/{tg_id}', response_model=list[Record], tags=['Записи'], name='Все записи пользователя')
async def get_record(tg_id: int) -> list[Record]:
    return await get_record_by_tg_db(tg_id=tg_id)


@records_rout.get('/{record_id}', response_model=Record, tags=['Записи'], name='Запись пользователя по ID')
async def get_record(record_id: int):
    return await get_record_by_id_db(record_id=record_id)


@records_rout.patch('/{record_id}', tags=['Записи'], name='Подтвердить запись')
async def confirmation(record_id: int, msg: str = None):
    rc = await get_record_by_id_db(record_id)
    if rc:
        if rc.confirmation:
            raise HTTPException(status_code=status.HTTP_200_OK, detail='Запись уже была подтверждена')

        await rc.update(confirmation=True)

        await bot.send_document(
            chat_id=rc.user_id.id,
            document=files['memo'],
            caption=msg if msg else success_confirm_record.format(rc.date_time, rc.location))
        return status.HTTP_200_OK
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Запись не найдена')


@records_rout.delete('/{record_id}', tags=['Записи'], name='Удалить запись')
async def delete_record(record_id: int):
    return await delete_record_db(record_id)
