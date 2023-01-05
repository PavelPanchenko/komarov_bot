import os.path
import shutil

from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from api.database.files import add_file_db
from api.database.models import UserFile
from loader import dp, bot
from settings.config import GROUP_ID, HOST
from states.state import Appointments
from utils.variables import send_document_message, success_format_files_message


@dp.message_handler(text='📌Отправить файл', state='*')
async def send_document(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await message.answer(text=send_document_message)
    await Appointments.file.set()


@dp.message_handler(content_types=['document', 'photo'], state=Appointments.file)
async def get_files(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    file_name = ''

    await bot.forward_message(chat_id=GROUP_ID, from_chat_id=message.from_user.id, message_id=message.message_id)

    if message.document:
        file_info = await bot.get_file(message.document.file_id)
        file_name = message.document['file_name']

    if message.photo:
        file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_name = file_info.file_path.split('/')[-1]

    downloaded_file = await bot.download_file(file_info.file_path)

    if not os.path.isdir(f"files/{message.chat.id}/{file_info.file_path.split('/')[0]}"):
        os.makedirs(f"files/{message.chat.id}/{file_info.file_path.split('/')[0]}")

    file_location = f"files/{message.chat.id}/{file_info.file_path}"
    if not os.path.exists(file_location):
        with open(file_location, "wb") as file_object:
            shutil.copyfileobj(downloaded_file, file_object)

        await add_file_db(UserFile(
            user_id=message.chat.id,
            file_name=file_name,
            file_size=file_info.file_size,
            file_path=f'{HOST}/' + file_location)
        )

    await message.answer(text=success_format_files_message)
