from utils.static_data import list_services, files
from keyboards.inline.button import services_items, callback_service
from loader import dp, bot
from aiogram.types import Message, CallbackQuery


@dp.message_handler(text='🩺Подготовка', state='*')
async def training_info(message: Message):
    await message.answer_document(document=files['memo'])
    # await message.answer(text='Выберите услугу:', reply_markup=services_items(event='training'))


# @dp.callback_query_handler(callback_service.filter(event='training'))
# async def get_info(call: CallbackQuery, callback_data: dict):
#     service_id = int(callback_data['payload'])
#     services = next((item for item in list_services if item['id'] == service_id), None)
#     await call.message.answer(text=services['description'])
#     await bot.answer_callback_query(call.id)

