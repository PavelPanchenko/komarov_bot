from aiogram.dispatcher.filters import ChatTypeFilter

from loader import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatType

from settings.config import GROUP_ID
from states.state import Support
from utils.variables import support_start_message, error_message


@dp.message_handler(text='Задать вопрос ❓', state='*')
async def support(message: Message, state: FSMContext):
    await state.reset_state(with_data=False)
    # await message.answer(text=support_start_message, reply_markup=support_close_button)
    await message.answer(text=support_start_message)
    await Support.active.set()


# @dp.message_handler(text='Закончить диалог', state='*')
# async def support_close(message: Message, state: FSMContext):
#     await state.reset_state(with_data=False)
#     if message.chat.type == ChatType.PRIVATE:
#         await message.answer(text=support_end_message, reply_markup=main_menu_buttons)
#         await state.reset_state(with_data=False)
#
#     if message.chat.type == ChatType.SUPERGROUP:
#         await message.answer(text=support_end_message, reply_markup=ReplyKeyboardRemove())
#         await state.update_data(recipient=None)


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), state=Support.active)
async def support_active(message: Message, state: FSMContext):
    await bot.forward_message(chat_id=GROUP_ID, from_chat_id=message.chat.id, message_id=message.message_id)
    await state.reset_state(with_data=False)


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE))
async def support_active(message: Message):
    await message.delete()
    await message.answer(text=error_message)
