from fastapi import APIRouter, Query, HTTPException
from starlette import status

from api.database.address import get_addresses_db, add_address_db, update_address_db, delete_address_db

location_routs = APIRouter(prefix='/location')


@location_routs.get('', tags=['Адресса центров'], name='Локации')
async def list_location():
    return get_addresses_db()


@location_routs.post('/add', tags=['Адресса центров'], name='Добавить локацию')
async def add_location(addresses: list[str] = Query(default=None, max_length=32)):
    try:
        for address in addresses:
            add_address_db(address)
        return status.HTTP_201_CREATED
    except Exception as ex:
        print(ex)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Error')


@location_routs.put('/update/{location_id}', tags=['Адресса центров'], name='Обновить локацию')
async def update_location(location_id: int, address: str = Query(default=None, max_length=32)):
    address = update_address_db(location_id, address)
    if address:
        return {"status": True}
    return {"status": False}


@location_routs.delete('/delete/{location_id}', tags=['Адресса центров'], name='Удалить локацию')
async def delete_location(location_id: int):
    address = delete_address_db(location_id)
    return address
