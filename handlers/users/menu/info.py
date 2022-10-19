from aiogram.dispatcher import FSMContext

from keyboards.default.buttons import info_menu_buttons
from loader import dp
from aiogram.types import Message, ChatType
from aiogram.dispatcher.filters import ChatTypeFilter


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), text='❕Информация', state='*')
async def info_menu(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    await message.answer(text='<pre>Информация:</pre>', reply_markup=info_menu_buttons)
