from aiogram import types
from aiogram.types import BotCommandScope, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats

from loader import bot


async def set_default_commands():
    await bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
        ],
        scope=BotCommandScope(type='all_private_chats')
    )

    await bot.set_my_commands(
        [
            types.BotCommand("admin", "Меню для админов"),
        ],
        scope=BotCommandScope(type="all_chat_administrators", chat_id=-1001503490441)
    )
