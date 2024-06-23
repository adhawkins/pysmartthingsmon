from sqlalchemy import create_engine, select, delete, exc, event
from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine

from .Base import Base
from .Locations import Locations
from .Rooms import Rooms
from .Readings import Readings


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    print("Setting connection params")
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
