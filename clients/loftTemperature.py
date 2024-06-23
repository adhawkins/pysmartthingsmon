import click
import requests

from WebService import WebService

from pprint import pprint


@click.command()
@click.pass_context
def addLoftTemperature(ctx):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    webservice = WebService(base_url)
    loftRoom = webservice.findRoomName("Loft")

    if loftRoom:
        loft = requests.get("http://nas.gently.org.uk:5000/").json()

        webservice.addReading(
            loftRoom["id"], ambient=loft[0]["internal temperature"])
