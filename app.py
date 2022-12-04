import logging

import sqlalchemy
import uvicorn as uvicorn
from aiogram import Dispatcher, Bot
from aiogram.types import Update
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# from api.database.base import engine, Base
from api.database.models import database, metadata, DATABASE_URL
from api.routs.files import files_routs
# from api.routs.notifications import notification_rout
from api.routs.notifications import notification_rout
from api.routs.user import users_rout
from api.routs.record import records_rout
from api.routs.websocket import socket_routs
from loader import dp, bot
# from scheduler.tasks import helper
from settings.config import BOT_TOKEN, HOST, PORT
from utils.set_bot_commands import set_default_commands
import middlewares, filters, handlers

# engine = sqlalchemy.create_engine(DATABASE_URL)
# metadata.create_all(engine)


# Base.metadata.create_all(engine)


app = FastAPI(title='Telegram Bot API', swagger_ui_parameters={"defaultModelsExpandDepth": -1})
app.state.database = database

app.include_router(users_rout)
app.include_router(records_rout)
# app.include_router(location_routs)
app.include_router(files_routs)
app.include_router(socket_routs)
app.include_router(notification_rout)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEBHOOK_PATH = f'/bot/{BOT_TOKEN}'
WEBHOOK_URL = HOST + WEBHOOK_PATH


@app.post('/bot/{BOT_TOKEN}', tags=['Only for Telegram api'], include_in_schema=False)
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
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()

    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    await bot.delete_my_commands()
    await set_default_commands()

    # scheduler.start()

    # await helper()


@app.on_event('shutdown')
async def on_shutdown():
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

    bot_session = await bot.get_session()
    await bot_session.close()
    await bot.delete_webhook()
    # await scheduler.shutdown(wait=False)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
