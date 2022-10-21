from typing import Optional

from fastapi import APIRouter, UploadFile, File

from api.database.user import get_user_all_db
from loader import bot

notification_rout = APIRouter(prefix='/notify')


@notification_rout.post('', tags=['Notify'])
async def send_notify(tg_id: int, message: str = None, file: UploadFile = File(default=None)):
    if file and message:
        file_bytes = file.file.read()
        await bot.send_document(chat_id=tg_id, document=(file.filename, file_bytes), caption=message)
        return {'file': file, 'message': message}
    if file:
        file_bytes = file.file.read()
        await bot.send_document(chat_id=tg_id, document=(file.filename, file_bytes), caption=message)
        return {'file': file}
    await bot.send_message(chat_id=tg_id, text=message)
    return {'message': message}


@notification_rout.post('/all', tags=['Notify'])
async def send_all_notify(message: str, file: UploadFile = File(default=None)):
    users = get_user_all_db()
    count_send = 0
    for user in users:
        if file and message:
            file_bytes = file.file.read()
            await bot.send_document(chat_id=user.tg_id, document=(file.filename, file_bytes), caption=message)
        if file:
            file_bytes = file.file.read()
            await bot.send_document(chat_id=user.tg_id, document=(file.filename, file_bytes), caption=message)
        await bot.send_message(chat_id=user.tg_id, text=message)
        count_send += 1
    return f'Отправлено {count_send} из {len(users)}'
