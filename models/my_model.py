from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from helpers.db import Base


class MyModel(Base):
    __tablename__ = "my_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    field1: Mapped[str] = mapped_column(String(255), nullable=False)
    field2: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class MyModelSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    field1: str
    field2: bool
    created_at: datetime
    updated_at: datetime


class MyModelRequest(BaseModel):
    field1: str
    field2: bool


class MyModelResponse(BaseModel):
    message: str
    model: Optional[MyModelSchema] = None
