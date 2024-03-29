from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel

from api.database.user import get_user_all_db
from loader import bot

notification_rout = APIRouter(prefix='/notify')


class Notify(BaseModel):
    message: str = None
    file: UploadFile = File(...)


@notification_rout.post('', tags=['Notify'])
async def send_notify(tg_id: int, message: str = Form(default=None),  file: UploadFile = File(default=None)):
    if file and message:
        file_bytes = file.file.read()
        await bot.send_document(chat_id=tg_id, document=(file.filename, file_bytes), caption=message)
        return {'file': file, 'message': message}
    if file:
        file_bytes = file.file.read()
        await bot.send_document(chat_id=tg_id, document=(file.filename, file_bytes), caption=message)
        return {'file': file}
    await bot.send_message(chat_id=tg_id, text=message)
    return {'message': 'success'}


@notification_rout.post('/all', tags=['Notify'])
async def send_all_notify(message: str = Form(default=None), file: UploadFile = File(default=None)):
    print(message)
    users = await get_user_all_db()
    count_send = 0

    if file and message:
        file_bytes = file.file.read()
        for user in users:
            await bot.send_document(chat_id=user.id, document=(file.filename, file_bytes), caption=message)
            count_send += 1
        return f'Отправлено {count_send} из {len(users)}'

    if file and not message:
        file_bytes = file.file.read()
        for user in users:
            await bot.send_document(chat_id=user.id, document=(file.filename, file_bytes))
            count_send += 1
        return f'Отправлено {count_send} из {len(users)}'

    if message and not file:
        for user in users:
            await bot.send_message(chat_id=user.id, text=message)
            count_send += 1
        return f'Отправлено {count_send} из {len(users)}'
