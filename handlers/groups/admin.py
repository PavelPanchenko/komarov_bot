from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import ChatTypeFilter, Command
from aiogram.types import CallbackQuery, ChatType, Message, ContentType

from api.database.record import get_record_by_id_db, delete_record_db, get_record_all_db
from api.database.user import get_user_all_db, get_user_by_id_db
from keyboards.inline.button import callback_record, accept_record_button, admin_menu_button, \
    admin_menu_record_button, admin_cancel_message_all_users_button
from loader import dp, bot
from states.state import MessageAll
from utils.static_data import files
from utils.variables import success_confirm_record, reject_confirm_record, send_admins_record_message, \
    confirmed_rec_message, unconfirmed_rec_message, for_all_users_message, users_empty_message


@dp.callback_query_handler(
    ChatTypeFilter(ChatType.SUPERGROUP), callback_record.filter(event='accept_record'))
async def admin_accept_handler(call: CallbackQuery, callback_data: dict):
    record_id = int(callback_data['payload'])
    record = await get_record_by_id_db(record_id)
    if record:
        await record.update(confirmation=True)
        await bot.send_document(
            chat_id=record.user_id.id,
            document=files['memo'],
            caption=success_confirm_record.format(record.date_time, record.location))
        await call.answer(text='Пользователь уведомлен', show_alert=True)
        return await call.message.edit_reply_markup(reply_markup=accept_record_button(record_id, accepted_btn=False))
    await call.message.delete()
    await call.message.answer('Запись больше не существует')


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), callback_record.filter(event='reject_record'))
async def admin_accept_handler(call: CallbackQuery, callback_data: dict, state: FSMContext):
    record_id = int(callback_data['payload'])
    record = await get_record_by_id_db(record_id)
    if record:
        await bot.send_message(chat_id=record.user_id.id, text=reject_confirm_record.format(record.date_time))
        await call.answer(text='Пользователь уведомлен', show_alert=True)
        await delete_record_db(record_id)
    await call.message.delete()


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), callback_record.filter(event='close_record'))
async def close_record(call: CallbackQuery, callback_data: dict):
    record_id = int(callback_data['payload'])
    await delete_record_db(record_id)
    await call.message.delete()


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), text='admin_menu', state='*')
async def back_admin_menu(call: CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await call.message.edit_reply_markup(reply_markup=admin_menu_button)


@dp.message_handler(ChatTypeFilter(ChatType.SUPERGROUP), Command(['admin']))
async def get_admin_menu(message: Message):
    user = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if user.status in ['creator', 'administrator']:
        await message.answer(text='Меню для администраторов', reply_markup=admin_menu_button)


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), text='menu_record')
async def get_admin_menu_records(call: CallbackQuery):
    await call.message.edit_text('Какие записи хотите посмотреть?', reply_markup=admin_menu_record_button)


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), text='menu_record_items')
async def get_appointment(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    appointments = await get_record_all_db(sort='confirmed')
    if not appointments:
        return await call.message.answer(text=confirmed_rec_message)
    for record in appointments:
        user = await get_user_by_id_db(record.id)
        await dp.bot.send_message(
            chat_id=call.message.chat.id,
            text=send_admins_record_message.format(
                record.id, f'<a href="{call.from_user.url}">{call.from_user.first_name}</a>', record.date_time,
                record.service, record.location),
            reply_markup=accept_record_button(record.id, accepted_btn=False))


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), text='menu_not_record_items')
async def get_appointment_unconfirmed(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    appointments = await get_record_all_db(sort='not_confirmed')

    if not appointments:
        return await call.message.answer(text=unconfirmed_rec_message)
    for record in appointments:
        user = await get_user_by_id_db(record.id)
        await dp.bot.send_message(
            chat_id=call.message.chat.id,
            text=send_admins_record_message.format(
                record.id, f'<a href="{call.from_user.url}">{call.from_user.first_name}</a>', record.date_time,
                record.service, record.location),
            reply_markup=accept_record_button(record.id))


@dp.callback_query_handler(ChatTypeFilter(ChatType.SUPERGROUP), text='send_all_message')
async def send_all_message(call: CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.answer(text=for_all_users_message, reply_markup=admin_cancel_message_all_users_button)
    await MessageAll.message.set()


@dp.message_handler(state=MessageAll.message)
async def get_message_all(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    all_users = await get_user_all_db()

    if not all_users:
        return await message.answer(users_empty_message)

    count = 0
    for user in all_users:
        try:

            if message.text:
                await bot.send_message(chat_id=user.id, text=message.text)

            if message.photo:
                await bot.send_photo(
                    chat_id=user.id, photo=message.photo[-1].file_id, caption=message.caption)

            if message.document:
                await bot.send_document(
                    chat_id=user.id, document=message.document.file_id, caption=message.caption)
            count += 1
        except Exception as ex:
            print(ex)
            continue
    await message.answer(
        text=f'{count} из {len(all_users)} пользователей получили уведомления',
        reply_markup=admin_menu_button)


@dp.message_handler(ChatTypeFilter(ChatType.SUPERGROUP),
                    content_types=[ContentType.TEXT, ContentType.PHOTO, ContentType.DOCUMENT])
async def send_msg(message: Message, state: FSMContext):
    print('message in admin', message)
    if message.reply_to_message:
        if message.reply_to_message.entities:
            user_id = message.reply_to_message.entities[1].user.id
        if message.reply_to_message.forward_from:
            user_id = message.reply_to_message.forward_from['id']

        if message.photo:
            file_id = message.photo[-1].file_id
            await bot.send_photo(chat_id=user_id, photo=file_id, caption=message.caption)
        if message.document:
            file_id = message.document.file_id
            await bot.send_document(chat_id=user_id, document=file_id, caption=message.caption)
