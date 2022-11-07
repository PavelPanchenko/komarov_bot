from api.database.models import Record
from api.schemas.record import CreateRecord, RecordItem


async def add_record_db(data: CreateRecord):
    record = Record(**data.dict())
    return await record.save()


async def get_record_by_tg_db(tg_id: int) -> list[Record]:
    return await Record.objects.filter(user_id=tg_id).order_by('date_time').all()


async def get_record_by_id_db(record_id: int) -> Record:
    return await Record.objects.get_or_none(id=record_id)


async def get_record_all_db(sort: str = None) -> list[Record]:
    print(sort)
    if sort == 'confirmed':
        return await Record.objects.filter(confirmation=True).order_by('date_time').all()

    if sort == 'not_confirmed':
        return await Record.objects.filter(confirmation=False).order_by('date_time').all()

    return await Record.objects.order_by('date_time').all()


async def update_record_db(record_id: int, confirmation: bool):
    record = await Record.objects.get_or_none(id=record_id)
    if record:
        return await record.update(confirmation=confirmation)
    return record


async def delete_record_db(record_id: int):
    record = await Record.objects.get_or_none(id=record_id)
    if record:
        await record.delete()
        return record.id
    return record
