from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import List
from sqlalchemy.types import TypeDecorator

import datetime

from .Base import Base

from pprint import pprint


class TZDateTime(TypeDecorator):
    impl = DateTime
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            if not value.tzinfo or value.tzinfo.utcoffset(value) is None:
                raise TypeError("tzinfo is required")
            value = value.astimezone(
                datetime.timezone.utc).replace(tzinfo=None)

        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = value.replace(tzinfo=datetime.timezone.utc).astimezone()

        return value


class Readings(Base):
    __tablename__ = "readings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[str] = mapped_column(
        ForeignKey("rooms.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    timestamp: Mapped[DateTime] = mapped_column(
        TZDateTime, server_default=func.now())
    set_point: Mapped[float] = mapped_column(nullable=True)
    ambient: Mapped[float]
    humidity: Mapped[float] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    away: Mapped[int] = mapped_column(nullable=True)

    roomdetails: Mapped["Rooms"] = relationship()
