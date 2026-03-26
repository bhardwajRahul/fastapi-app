import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.my_model import MyModel

logger = logging.getLogger(__name__)


async def create(obj: MyModel, db: AsyncSession) -> Optional[int]:
    try:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj.id
    except Exception:
        logger.exception("[my model : create]")
        await db.rollback()
        return None


async def get_random_row(db: AsyncSession) -> Optional[MyModel]:
    try:
        stmt = select(MyModel).order_by(MyModel.id.desc()).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except Exception:
        logger.exception("[my model : get random row]")
        return None


async def update(id: int, obj: MyModel, db: AsyncSession) -> Optional[MyModel]:
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            item.field1 = obj.field1
            item.field2 = obj.field2
            await db.commit()
            await db.refresh(item)
            return item
        return None
    except Exception:
        logger.exception("[my model : update]")
        await db.rollback()
        return None


async def delete(id: int, db: AsyncSession) -> bool:
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            await db.delete(item)
            await db.commit()
            return True
        return False
    except Exception:
        logger.exception("[my model : delete]")
        await db.rollback()
        return False


async def find_by_id(id: int, db: AsyncSession) -> Optional[MyModel]:
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except Exception:
        logger.exception("[my model : find by id]")
        return None
