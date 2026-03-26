import logging

from helpers.db import AsyncSessionLocal
from helpers.scheduler import scheduler
from models.my_model import MyModel
from services import my_model as service_my_model

logger = logging.getLogger(__name__)


@scheduler.scheduled_job("cron", hour=0, minute=1)
async def job_create_my_model():
    async with AsyncSessionLocal() as session:
        data = {"field1": "Test Job", "field2": False}
        obj = MyModel(**data)
        id = await service_my_model.create(obj, session)
        logger.info(f"Job executed: {id}")
        return id
