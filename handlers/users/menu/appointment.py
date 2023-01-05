import datetime
import logging

from aiogram.dispatcher import FSMContext

from api.database.record import add_record_db, delete_record_db
from api.schemas.record import CreateRecord

from utils.static_data import list_services, center_addresses
from keyboards.default.buttons import main_menu_buttons
from keyboards.inline.button import location_items, callback_center, accept_appointment_button, services_items, \
    callback_service, accept_record_button, get_working_time, callback_time, callback_record
from loader import dp, bot
from aiogram.types import Message, CallbackQuery

from settings.config import GROUP_ID
from utils.inline_calendar import InlineCalendar
from utils.variables import record_to_center_message, date_to_center_message, time_to_center_message, \
    data_to_center_message, send_data_record, service_message, send_admins_record_message, \
    opening_hours_message, reject_confirm_user_record

inline_calendar = InlineCalendar()


@dp.callback_query_handler(callback_record.filter(event='new_record'))
async def new_record(call: CallbackQuery, callback_data: dict, state: FSMContext):
    record_id = int(callback_data['payload'])
    await delete_record_db(record_id)
    await bot.send_message(chat_id=GROUP_ID, text=reject_confirm_user_record.format(record_id))
    await get_location_center(call.message, state=state)


@dp.message_handler(text='📑Новая запись', state='*')
async def get_location_center(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    location = center_addresses
    await message.answer(
        text=record_to_center_message,
        reply_markup=location_items(location))


@dp.callback_query_handler(callback_center.filter(event='center_list'))
async def get_location(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(callback_query_id=call.id)

    await call.message.delete()
    location_id = int(callback_data.get('payload'))

    address = next((item for item in center_addresses if item['id'] == location_id), None)

    await call.message.answer(text=f'<pre>Адрес: {address["address"]}</pre>')
    await state.update_data(location=address['address'])
    await appointment_date(call)


async def appointment_date(call):
    inline_calendar.init(
        datetime.date.today() + datetime.timedelta(days=1),
        datetime.date.today() + datetime.timedelta(days=1),
        datetime.date.today() + datetime.timedelta(weeks=16))
    await call.message.answer(text=date_to_center_message, reply_markup=inline_calendar.get_keyboard())


@dp.callback_query_handler(inline_calendar.filter())
async def calendar_callback_handler(q: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(q.id)

    picked_data = inline_calendar.handle_callback(q.from_user.id, callback_data)

    data = await state.get_data()

    if picked_data in ['NEXT_MONTH', 'PREVIOUS_MONTH']:
        return await bot.edit_message_reply_markup(
            chat_id=q.from_user.id, message_id=q.message.message_id,
            reply_markup=inline_calendar.get_keyboard(q.from_user.id))

    if isinstance(picked_data, datetime.date):
        address = next((item for item in center_addresses if item['address'] == data['location']), None)
        is_day_of = address['working'][picked_data.weekday()]
        if len(is_day_of):
            await state.update_data(picked_data=str(picked_data))
            await q.message.edit_text(text=str(picked_data), reply_markup=None)

            await appointment_time(q, state, picked_data)

        else:
            return await q.message.answer(
                text='<i>Выберите другую дату.</i>\n' + address['working_text'],
                reply_markup=inline_calendar.get_keyboard(q.from_user.id))


async def appointment_time(call, state, picked_data):
    data = await state.get_data()
    address = next((item for item in center_addresses if item['address'] == data['location']), None)
    working_time = address['working'][picked_data.weekday()]

    await call.message.answer(
        text=time_to_center_message,
        reply_markup=get_working_time(working_time)
    )


@dp.callback_query_handler(callback_time.filter(event='work_time'))
async def get_time(call: CallbackQuery, callback_data: dict, state: FSMContext):
    time = callback_data.get('payload')
    await state.update_data(time=time)
    await call.message.answer(text=service_message, reply_markup=services_items())


@dp.callback_query_handler(callback_service.filter(event='service'))
async def get_service(call: CallbackQuery, callback_data: dict, state: FSMContext):
    service_id = int(callback_data.get('payload'))
    services = next((item for item in list_services if item['id'] == service_id), None)

    await state.update_data(service=services['category'])

    data = await state.get_data()
    location, picked_data, time, service = data.values()
    await call.message.answer(
        text=data_to_center_message.format(location, picked_data, time, service),
        reply_markup=accept_appointment_button)


@dp.callback_query_handler(callback_center.filter(event='send_data'))
async def send_data(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(call.id)
    data = await state.get_data()

    try:
        match callback_data.get('payload'):
            case 'send':
                # Send to server data
                d_time = f"{data['picked_data']} {data['time'].split('-')[0]}"
                record_time = datetime.datetime.fromisoformat(d_time)

                # user = await get_user_db(tg_id=call.message.chat.id)
                payload = CreateRecord(location=data['location'], date_time=record_time, user_id=call.message.chat.id,
                                       service=data['service'])

                record = await add_record_db(payload)
                await dp.bot.send_message(
                    chat_id=GROUP_ID,
                    text=send_admins_record_message.format(
                        record.id, f'<a href="{call.from_user.url}">{call.from_user.first_name}</a>', record_time,
                        data['service'], data['location']),
                    reply_markup=accept_record_button(record.id))
                await call.message.answer(text=send_data_record, reply_markup=main_menu_buttons)
            case 'edit':
                await get_location_center(call.message, state)
    except Exception as ex:
        logging.warning(ex)
