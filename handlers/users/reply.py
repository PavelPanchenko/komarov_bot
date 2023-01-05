import logging

from aiogram.dispatcher.filters import ChatTypeFilter, IsReplyFilter
from aiogram.types import Message, ChatType

from loader import dp, bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(ChatTypeFilter(ChatType.SUPERGROUP), IsReplyFilter(is_reply=True))
async def bot_echo(message: Message):
    print('message reply admin', message)
    msg = message.reply_to_message
    user_id = None
    try:
        if msg.entities:
            user_id = message.reply_to_message.entities[1].user.id
        if msg.forward_from:
            user_id = msg.forward_from['id']

        if message.text:
            await bot.send_message(chat_id=user_id, text=message.text)

        if message.photo:
            photo = message.photo[-1].file_id
            await bot.send_photo(chat_id=user_id, photo=photo, caption=message.caption)

    except Exception as ex:
        logging.warning(ex)
        await message.answer('<pre>ERROR❗️На это сообщение нельзя ответить</pre>')
