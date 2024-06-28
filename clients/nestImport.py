import mysql.connector
import click
import mysql.connector
from datetime import datetime

from WebService import WebService


@click.command()
@click.pass_context
@click.option("--db-host", help="The database host name", required=True)
@click.option("--db-user", help="The database user name", required=True)
@click.option("--db-password", help="The database password", required=True)
@click.option("--db-database", help="The database name", required=True)
def nestImport(ctx, db_host, db_user, db_password, db_database):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    db = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_database)
    cursor = db.cursor()

    webservice = WebService(base_url)
    loftRoom = webservice.findRoomName("Loft")
    livingRoom = webservice.findRoomName("Living Room")

    readings = webservice.readings()

    earliestLoft = None
    earliestLivingRoom = None

    for reading in readings:
        readingTimestamp = datetime.fromisoformat(
            reading['timestamp']).astimezone()

        if reading['room_id'] == loftRoom['id']:
            if not earliestLoft or readingTimestamp < earliestLoft:
                earliestLoft = readingTimestamp

        if reading['room_id'] == livingRoom['id']:
            if not earliestLivingRoom or readingTimestamp < earliestLivingRoom:
                earliestLivingRoom = readingTimestamp

    if loftRoom and livingRoom:
        cursor.execute("SELECT * FROM measurements ORDER BY timestamp")

        for (timestamp, set_point, ambient, humidity, state, loft) in cursor:
            timestamp = timestamp.astimezone()
            if loft and timestamp < earliestLoft:
                reading = webservice.addReading(
                    loftRoom['id'], timestamp=timestamp, ambient=loft)

            if set_point and ambient and humidity and state and timestamp < earliestLivingRoom:
                reading = webservice.addReading(
                    livingRoom['id'], timestamp=timestamp, set_point=set_point, ambient=ambient, humidity=humidity, state=state)
