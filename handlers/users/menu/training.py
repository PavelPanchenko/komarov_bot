from aiogram.types import Message

from loader import dp
from utils.static_data import files


@dp.message_handler(text='🩺Подготовка', state='*')
async def training_info(message: Message):
    await message.answer_document(document=files['memo'])
