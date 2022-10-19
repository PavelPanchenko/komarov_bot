from typing import Optional

from fastapi import APIRouter, UploadFile, File

from loader import bot

notification_rout = APIRouter(prefix='/notify')


@notification_rout.post('', tags=['Notify'])
async def send_notify(tg_id: int, message: str = None, file: UploadFile = File(default=None)):
    print(file)
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
async def send_all_notify(message: str, file: UploadFile(...) = None):
    msg = message
    return {'message': msg}
