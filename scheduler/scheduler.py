from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

job_stores = {
    'default': SQLAlchemyJobStore(url='sqlite:///data/jobs.db')
}

job_defaults = {
    'coalesce': False,
    'max_instances': 10
}

scheduler = AsyncIOScheduler(job_defaults=job_defaults, jobstores=job_stores)
