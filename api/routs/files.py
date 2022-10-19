import base64

from loader import bot
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from api.database.address import get_addresses_db, add_address_db, update_address_db, delete_address_db
from api.database.files import get_files_by_tg_id_db, add_file_db
from api.database.user import get_user_db
from starlette import status

files_routs = APIRouter(prefix='/files')


@files_routs.get('', tags=['Файлы'])
async def get_files_by_tg_id(tg_id: int):
    return get_files_by_tg_id_db(tg_id)


@files_routs.post('/send{tg_id}', tags=['Файлы'], name='Отправить файл пользователю')
async def add_location(tg_id: int, file: UploadFile = File(description='type: jpg, png, jpeg, pdf, txt')):
    if file.content_type in ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf', 'text/plain']:
        file_bytes = file.file.read()
        await bot.send_document(chat_id=tg_id, document=(file.filename, file_bytes))
        encode_string = base64.b64encode(file_bytes)
        return add_file_db(tg_id, file_name=file.filename, file_content=encode_string)
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not supported format")
        # await bot.send_photo(chat_id=tg_id, photo=(file.filename, file.file.read()), caption=file.filename)
