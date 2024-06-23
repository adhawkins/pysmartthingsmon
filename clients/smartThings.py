import click
import asyncio
import aiohttp
import pysmartthings

from auth import TOKEN
from WebService import WebService


from pprint import pprint


async def main(base_url, debug):
    locations = []

    webservice = WebService(base_url)

    async with aiohttp.ClientSession() as session:
        api = pysmartthings.SmartThings(session, TOKEN)

        for location in await api.locations():
            if not webservice.locationExists(location.location_id):
                webservice.addLocation(location.location_id, location.name, location.latitude, location.longitude,
                                       location.region_radius, location.temperature_scale, location.locale, location.country_code, location.timezone_id)

            for room in await location.rooms():
                if not webservice.roomExists(room.room_id):
                    webservice.addRoom(
                        room.room_id, room.location_id, room.name, room.background_image)

        for device in await api.devices():
            if device.label == "Air Con":
                await device.status.refresh()
                values = device.status.values

                webservice.addReading(
                    device.room_id,
                    ambient=values["temperature"],
                    set_point=values["coolingSetpoint"],
                    humidity=values["humidity"],
                    state=("COOLING" if values["switch"] == "on" else "OFF")
                )


@click.command()
@click.pass_context
def addSmartThingsResults(ctx):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(base_url, debug))
