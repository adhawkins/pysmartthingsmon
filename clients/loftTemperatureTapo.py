import click

import asyncio

from WebService import WebService

from tapo import ApiClient
from tapo.responses import T31XResult

from pprint import pprint


async def addLoftTemperatureTapoWorker(base_url, debug):
    webservice = WebService(base_url)
    loftRoom = webservice.findRoomName("Loft")

    if loftRoom:
        # loft = requests.get("http://nas.gently.org.uk:5000/").json()

        # webservice.addReading(
        #     loftRoom["id"], ambient=loft[0]["internal temperature"])

        tapo_username = "andy@gently.org.uk"
        tapo_password = "N8y79ETrf9ukGc"
        ip_address = "tapo-hub.gently.org.uk"

        client = ApiClient(tapo_username, tapo_password)
        hub = await client.h100(ip_address)

        child_device_list = await hub.get_child_device_list()

        for child in child_device_list:
            if isinstance(child, T31XResult):
                # print(
                #     "Found T31X child device with nickname: {}, id: {}, temperature: {:.2f} {}, humidity: {}%.".format(
                #         child.nickname,
                #         child.device_id,
                #         child.current_temperature,
                #         child.temperature_unit,
                #         child.current_humidity,
                #     )
                # )

                webservice.addReading(
                    loftRoom["id"], ambient=child.current_temperature, humidity=child.current_humidity)


@click.command()
@click.pass_context
def addLoftTemperatureTapo(ctx):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    asyncio.run(addLoftTemperatureTapoWorker(base_url, debug))
