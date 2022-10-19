import base64

from aiogram.dispatcher import FSMContext

from api.database.files import add_file_db
from keyboards.inline.button import callback_button
from loader import dp, bot
from aiogram.types import Message

from settings.config import GROUP_ID
from states.state import Appointments
from utils.variables import send_document_message, error_format_files_message, success_format_files_message


@dp.message_handler(text='Отправить файл 📇', state='*')
async def send_document(message: Message):
    await message.answer(text=send_document_message)
    await Appointments.file.set()


@dp.message_handler(content_types=['document', 'photo'], state=Appointments.file)
async def get_files(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)

    await bot.forward_message(chat_id=GROUP_ID, from_chat_id=message.from_user.id, message_id=message.message_id)

    if message.document:
        file_info = await bot.get_file(message.document.file_id)
        file_name = message.document['file_name']

    if message.photo:
        file_info = await bot.get_file(message.photo[len(message.photo) - 1].file_id)
        file_name = file_info.file_path.split('/')[-1]

    downloaded_file = await bot.download_file(file_info.file_path)
    encode_string = base64.b64encode(downloaded_file.getvalue())

    add_file_db(
        tg_id=message.chat.id,
        file_name=file_name,
        file_content=encode_string,
    )

    await message.answer(text=success_format_files_message)


    # else:
    #     await message.answer(text=error_format_files_message)
