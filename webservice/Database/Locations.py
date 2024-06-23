from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import List

from .Base import Base


class Locations(Base):
    __tablename__ = "locations"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    latitude: Mapped[float] = mapped_column(nullable=True)
    longitude: Mapped[float] = mapped_column(nullable=True)
    region_radius: Mapped[int] = mapped_column(nullable=True)
    temperature_scale: Mapped[str] = mapped_column(nullable=True)
    locale: Mapped[str] = mapped_column(nullable=True)
    country_code: Mapped[str] = mapped_column(nullable=True)
    timezone_id: Mapped[str] = mapped_column(nullable=True)
