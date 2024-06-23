import click

from NestThermostat import NestThermostat
from WebService import WebService

from pprint import pprint


@click.command()
@click.option("--project-id", help="The nest API project ID", required=True)
@click.option("--auth-file", help="File to store auth data", required=True)
@click.option("--secrets-file", help="File containing secrets information", required=True)
@click.pass_context
def addNestResults(ctx, project_id, auth_file, secrets_file):
    base_url = ctx.obj["BASE_URL"]
    debug = ctx.obj["DEBUG"]

    webservice = WebService(base_url)
    livingRoom = webservice.findRoomName("Living Room")

    if livingRoom:
        nest = NestThermostat(auth_file, secrets_file, project_id)

        measurement = nest.getMeasurement()

        reading = webservice.addReading(
            livingRoom['id'],
            ambient=measurement.ambient,
            humidity=measurement.humidity,
            set_point=measurement.target,
            state=measurement.state
        )
