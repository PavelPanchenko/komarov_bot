from aiogram import Dispatcher, Bot
from aiogram.types import Update
from starlette.middleware.cors import CORSMiddleware

from api.database.base import engine, Base
from api.routs.files import files_routs
from api.routs.location_center import location_routs
from api.routs.notifications import notification_rout
from api.routs.record import records_rout
from api.routs.user import users_rout
from api.routs.websocket import socket_routs
from scheduler.scheduler import scheduler
from scheduler.tasks import helper
from settings.config import BOT_TOKEN, HOST, PORT
import uvicorn as uvicorn
from fastapi import FastAPI
import logging

from loader import dp, bot
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

Base.metadata.create_all(engine)

app = FastAPI(title='Telegram Bot API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_rout)
app.include_router(records_rout)
# app.include_router(location_routs)
app.include_router(files_routs)
app.include_router(socket_routs)
app.include_router(notification_rout)

WEBHOOK_PATH = f'/bot/{BOT_TOKEN}'
WEBHOOK_URL = HOST + WEBHOOK_PATH


@app.post('/bot/{BOT_TOKEN}', tags=['Only for Telegram api'])
async def bot_webhook(update: dict):
    try:
        telegram_update = Update(**update)
        Dispatcher.set_current(dp)
        Bot.set_current(bot)
        await dp.process_update(telegram_update)
    except Exception as ex:
        logging.warning(ex)


@app.on_event('startup')
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    await bot.delete_my_commands()
    # Устанавливаем дефолтные команды
    await set_default_commands()
    # await database.connect()

    # Уведомляет про запуск
    # await on_startup_notify()
    # scheduler.start()

    await helper()


@app.on_event('shutdown')
async def on_shutdown():
    bot_session = await bot.get_session()
    await bot_session.close()
    await bot.delete_webhook()
    # await database.disconnect()
    # await scheduler.shutdown(wait=False)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
