import os.path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette import status

from api.database.files import get_all_files, get_files_by_id_db, delete_file_db
from settings.config import HOST

files_routs = APIRouter(prefix='/files')


@files_routs.get('', tags=['Файлы'])
async def get_files():
    return await get_all_files()


@files_routs.get('/{user_id}/{file_type}/{file_name}', tags=['Файлы'], include_in_schema=False)
async def get_file(user_id: int, file_type: str, file_name: str):
    file_path = os.path.join('files', f'{user_id}/{file_type}/{file_name}')
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')


@files_routs.delete('/{file_id}', tags=['Файлы'])
async def get_file(file_id: int):
    file = await get_files_by_id_db(file_id)
    if file:
        file_path = file.file_path.split(f'{HOST}/')[-1]
        if os.path.exists(file_path):
            os.remove(file_path)
        await delete_file_db(file_id)
        return status.HTTP_200_OK
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File not found')
