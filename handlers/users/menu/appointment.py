import datetime
import logging

from aiogram.dispatcher import FSMContext

from api.database.record import add_record_db
from api.database.user import get_user_db
from api.schemas.record import CreateRecord
from utils.static_data import list_services, center_addresses
from keyboards.default.buttons import main_menu_buttons
from keyboards.inline.button import location_items, callback_center, accept_appointment_button, services_items, \
    callback_service, accept_record_button
from loader import dp, bot
from aiogram.types import Message, CallbackQuery

from settings.config import GROUP_ID
from states.state import Appointments
from utils.inline_calendar import InlineCalendar
from utils.variables import record_to_center_message, date_to_center_message, time_to_center_message, \
    data_to_center_message, send_data_record, service_message, send_admins_record_message, \
    opening_hours_message

inline_calendar = InlineCalendar()


@dp.message_handler(text='📑Новая запись', state='*')
async def get_location_center(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    # location = get_addresses_db()
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
    # all_location = get_addresses_db()
    # await call.message.edit_reply_markup(reply_markup=location_items(all_location))

    # address = get_addresses_by_id_db(location_id)

    # address = center_addresses[location_id]
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
    if picked_data in ['NEXT_MONTH', 'PREVIOUS_MONTH']:
        return await bot.edit_message_reply_markup(
            chat_id=q.from_user.id, message_id=q.message.message_id,
            reply_markup=inline_calendar.get_keyboard(q.from_user.id))

    if isinstance(picked_data, datetime.date):
        await state.update_data(picked_data=str(picked_data))
        await q.message.edit_text(text=str(picked_data), reply_markup=None)

        await appointment_time(q)


async def appointment_time(call):
    await call.message.answer(text=time_to_center_message)
    await Appointments.time.set()


@dp.message_handler(state=Appointments.time)
async def get_time(message: Message, state: FSMContext):
    try:
        time = datetime.datetime.strptime(message.text, '%H:%M').time()

        if datetime.time(hour=9, minute=0) <= time <= datetime.time(hour=19, minute=0):
            await state.reset_state(with_data=False)
            await state.update_data(time=time)
            return await input_data(message)
        else:
            return await message.answer(text=opening_hours_message + '\nПовторите ввод')
    except ValueError:
        await message.answer(text='Формат времени указан не верно. Повторите ввод')


async def input_data(message):
    await message.answer(text=service_message, reply_markup=services_items())


@dp.callback_query_handler(callback_service.filter(event='service'))
async def get_service(call: CallbackQuery, callback_data: dict, state: FSMContext):
    service_id = int(callback_data.get('payload'))
    services = next((item for item in list_services if item['id'] == service_id), None)

    await state.update_data(service=services['category'])

    if 'subcategory' in services:
        return await call.message.edit_text(
            text='Выберите подкатегорию:',
            reply_markup=services_items(items=services['subcategory'], event='sub_service'))

    data = await state.get_data()
    location, picked_data, time, service = data.values()
    await call.message.answer(
        text=data_to_center_message.format(location, picked_data, time, service),
        reply_markup=accept_appointment_button)


@dp.callback_query_handler(callback_service.filter(event='sub_service'))
async def select_sub_services(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(call.id)

    service_id = int(callback_data.get('payload'))

    data = await state.get_data()
    location, picked_data, time, service = data.values()
    for item in list_services:
        if service in item['category']:
            update_service = f'{service} | {item["subcategory"][service_id -1]["category"]}'
            await state.update_data(service=update_service)
    await call.message.answer(
        text=data_to_center_message.format(location, picked_data, time, update_service),
        reply_markup=accept_appointment_button)


@dp.callback_query_handler(callback_center.filter(event='send_data'))
async def send_data(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await bot.answer_callback_query(call.id)
    data = await state.get_data()

    try:
        match callback_data.get('payload'):
            case 'send':
                # Send to server data
                record_time = f"{data['picked_data']} {data['time']}"

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
