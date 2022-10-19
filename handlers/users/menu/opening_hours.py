from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.types import Message

from utils.variables import opening_hours_message


@dp.message_handler(text='🗓График', state='*')
async def show_opening_hours(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await message.answer(
        text=opening_hours_message)
