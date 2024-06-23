#!/usr/bin/env python3

import click

from smartThings import addSmartThingsResults
from loftTemperature import addLoftTemperature
from nest import addNestResults


@click.group()
@click.option("--base-url", help="The base URL for the API", required=True)
@click.option("--debug/--no-debug", default=False, help="Debug")
@click.pass_context
def cli(ctx, base_url, debug):
    ctx.ensure_object(dict)

    ctx.obj["BASE_URL"] = base_url
    ctx.obj["DEBUG"] = debug


cli.add_command(addSmartThingsResults)
cli.add_command(addLoftTemperature)
cli.add_command(addNestResults)

if __name__ == "__main__":
    cli(obj={})
