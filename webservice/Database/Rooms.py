from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.exc import List

from .Base import Base


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[str] = mapped_column(primary_key=True)
    location_id: Mapped[str] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE"),
        autoincrement=False,
    )
    name: Mapped[str]
    background_image: Mapped[str] = mapped_column(nullable=True)

    locationdetails: Mapped["Locations"] = relationship()
