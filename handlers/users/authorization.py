import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove, ChatType, Message
from aiogram.dispatcher.filters import ChatTypeFilter

from api.database.models import User
from api.database.user import get_user_db, add_user_db
from api.schemas.user import CreateUser
from api.users_list import allowed_users_list
from keyboards.default.buttons import authorization_button, main_menu_buttons
from loader import dp, bot
from settings.config import GROUP_ID
from utils.variables import authorization_message, success_authorization_message, error_authorization_message, \
    loading_icon, main_menu_message


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.delete()
    is_user = await get_user_db(tg_id=int(message.chat.id))
    if is_user:
        await message.answer(text=main_menu_message, reply_markup=main_menu_buttons)
    else:
        await message.answer(text=authorization_message.format(message.chat.first_name),
                             reply_markup=authorization_button)


@dp.message_handler(content_types=['contact'])
async def check_auth(message: types.Message):
    await add_user_db(CreateUser(
        id=int(message.chat.id),
        full_name=message.chat.full_name,
        phone_number=message.contact.phone_number))
    await message.delete()

    if allowed_users_list(message.contact.phone_number):
        loading = await message.answer_sticker(sticker=loading_icon, reply_markup=ReplyKeyboardRemove())
        await asyncio.sleep(2.5)
        await bot.delete_message(chat_id=message.chat.id, message_id=loading['message_id'])
        await message.answer(text=success_authorization_message, reply_markup=main_menu_buttons)
    else:
        await message.answer(text=error_authorization_message)


@dp.message_handler(ChatTypeFilter(ChatType.PRIVATE), text='🔙Главное меню')
async def info_menu(message: Message):
    await message.answer(text='<i>Главное меню:</i>', reply_markup=main_menu_buttons)


# @dp.message_handler(content_types=['document'])
# async def get_files(message: Message):
#     if message.document:
#         await message.answer(text=message.document.file_id)
