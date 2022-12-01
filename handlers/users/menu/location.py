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
    center = next((item for item in center_addresses if item['id'] == location_id), None)

    await call.message.answer(f'<pre>Локация по адресу: {center["address"]}</pre>')

    # location = geolocator.geocode(center['address'], language='ru')

    await call.message.answer_location(
        latitude=center['coord']['lat'],
        longitude=center['coord']['long'],
        # live_period=3600,
        heading=45
    )
