from api.database.address import get_addresses_db, get_addresses_by_id_db
from keyboards.inline.button import location_items, callback_center
from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from geopy.geocoders import Nominatim

from utils.static_data import center_addresses

geolocator = Nominatim(user_agent="tg_bot")


@dp.message_handler(text='🚗Как добраться', state='*')
async def location_map(message: Message):
    # addresses = get_addresses_db()
    addresses = center_addresses
    await message.answer('<pre>Выберите адрес:</pre>', reply_markup=location_items(addresses, event='geo'))


@dp.callback_query_handler(callback_center.filter(event='geo'))
async def get_location(call: CallbackQuery, callback_data: dict):
    await bot.answer_callback_query(callback_query_id=call.id)

    await call.message.delete()

    location_id = int(callback_data.get('payload'))
    # center_name = get_addresses_by_id_db(location_id)
    center_name = center_addresses[location_id]

    # addresses = get_addresses_db()
    # await call.message.edit_reply_markup(reply_markup=location_items(addresses))
    await call.message.answer(f'<pre>Локация по адресу: {center_name["address"]}</pre>')

    location = geolocator.geocode(center_name['address'], language='ru')
    print(location.latitude)

    await call.message.answer_location(
        latitude=location.latitude,
        longitude=location.longitude,
        # live_period=3600,
        heading=45
    )
