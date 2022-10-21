import base64
import os.path

from loader import bot
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from api.database.address import get_addresses_db, add_address_db, update_address_db, delete_address_db
from api.database.files import add_file_db, get_all_files, get_files_by_id_db, delete_file_db
from api.database.user import get_user_db
from starlette import status

from settings.config import HOST

files_routs = APIRouter(prefix='/files')


@files_routs.get('', tags=['Файлы'])
async def get_files():
    return get_all_files()


@files_routs.get('/{user_id}/{file_type}/{file_name}', tags=['Файлы'], include_in_schema=False)
async def get_file(user_id: int, file_type: str, file_name: str):
    file_path = os.path.join('files', f'{user_id}/{file_type}/{file_name}')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {'error': 'File not found'}


@files_routs.delete('/{file_id}', tags=['Файлы'])
async def get_file(file_id: int):
    file = get_files_by_id_db(file_id)
    if file:
        file_path = file.file_path.split(f'{HOST}/')[-1]
        if os.path.exists(file_path):
            os.remove(file_path)
        delete_file_db(file_id)
        return status.HTTP_200_OK
    return status.HTTP_404_NOT_FOUND

#
# @files_routs.post('/send{tg_id}', tags=['Файлы'], name='Отправить файл пользователю')
# async def add_location(tg_id: int, file: UploadFile = File(description='type: jpg, png, jpeg, pdf, txt')):
#     if file.content_type in ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf', 'text/plain']:
#         file_bytes = file.file.read()
#         await bot.send_document(chat_id=tg_id, document=(file.filename, file_bytes))
#         encode_string = base64.b64encode(file_bytes)
#         return add_file_db(tg_id, file_name=file.filename, file_content=encode_string)
#     else:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not supported format")
#         # await bot.send_photo(chat_id=tg_id, photo=(file.filename, file.file.read()), caption=file.filename)
