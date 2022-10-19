from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///data/jobs.sqlite')
    }

job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }

scheduler = AsyncIOScheduler(job_defaults=job_defaults, jobstores=jobstores)


# def my_listener(event):
#     if event.exception:
#         print('The job crashed :(')
#     else:
#         print('The job worked :)')
#
#
# scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
