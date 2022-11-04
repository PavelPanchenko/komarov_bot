from api.database.record import get_record_by_tg_db, delete_record_db
from keyboards.inline.button import my_record_list_button, callback_record
from loader import dp, bot
from aiogram.types import Message, ChatType, CallbackQuery
from aiogram.dispatcher.filters import ChatTypeFilter

from settings.config import GROUP_ID
from utils.variables import send_client_record_message, reject_confirm_user_record, not_record_list_message


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), text='📁Мои записи', state='*')
async def my_records_list(message: Message):
    records = get_record_by_tg_db(message.chat.id)
    if not records:
        return await message.answer(text=not_record_list_message)
    for record in records:
        await message.answer(
            text=send_client_record_message.format(
                record.id, record.date_time, record.service, record.location,
                'Подтверждена' if record.confirmation else 'Не подтверждена'),
            reply_markup=my_record_list_button(record.id))


@dp.callback_query_handler(ChatTypeFilter(ChatType.PRIVATE), callback_record.filter(event='cancel_record'))
async def cancel_rec(call: CallbackQuery, callback_data: dict):
    record_id = callback_data['payload']
    await call.message.reply(text='<pre>Запись удалена</pre>')
    delete_record_db(record_id)
    await bot.send_message(chat_id=GROUP_ID, text=reject_confirm_user_record.format(record_id))


# @dp.callback_query_handler(ChatTypeFilter(ChatType.PRIVATE), callback_record.filter(event='record_transfer'))
# async def cancel_rec(call: CallbackQuery, callback_data: dict):
#     record_id = callback_data['payload']
#     await get_location_center(call.message, state)
