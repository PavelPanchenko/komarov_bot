import datetime

from api.database.record import get_record_all_db, delete_record_db
from api.database.user import get_user_by_id_db
from loader import bot
from scheduler.scheduler import scheduler


@scheduler.scheduled_job('cron', hour=11, minute=00, id='helper')
async def helper():
    current_day = datetime.datetime.now()
    all_records = await get_record_all_db('confirm')
    for record in all_records:
        """send notification to user"""
        if current_day.date() == (record.date_time.date() - datetime.timedelta(days=1)):
            user = await get_user_by_id_db(record.user_id.id)
            await bot.send_message(
                chat_id=user.tg_id,
                text=f"Напоминаем, что вы записаны на прием {record.date_time} по адресу {record.location}")

        if record.date_time.date() < current_day.date():
            """remove record from db"""
            await delete_record_db(record.id)
