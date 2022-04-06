#!/usr/bin/env python

import sys

import click
import leglight

# in here as the leglight module is not correctly adding the update_service method
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


def get_default_keylight(timeout):
    all_lights = leglight.discover(timeout)
    return next((l for l in all_lights), None)


def get_keylight(serial, timeout):
    all_lights = leglight.discover(timeout)
    return next((l for l in all_lights if l.serialNumber == serial), None)


@click.group()
@click.option(
    "-s",
    "--serial",
    required=False,
    default=None,
    help="Serial number of the light to operate on",
)
@click.option(
    "-t",
    "--timeout",
    default=2,
    type=int,
    help="The network timeout when discovering the lights",
)
@click.pass_context
def keylight(ctx, serial, timeout):
    """A simple CLI to control Elgato Keylights"""
    ctx.ensure_object(dict)

    # this allows us to just operate on the only or first keylight found on a network
    if not serial:
        light = get_default_keylight(timeout)
    else:
        light = get_keylight(serial, timeout)

    if not light:
        click.echo("Unable to find any keylights", err=True)
        sys.exit(-1)

    ctx.obj["light"] = light
    ctx.obj["timeout"] = timeout


@keylight.command(short_help="Turn on a keylight")
@click.pass_context
def on(ctx):
    """Turn on a single keylight"""
    click.echo(f"Turning on {ctx.obj['light'].serialNumber}")
    ctx.obj["light"].on()


@keylight.command(short_help="Turn off a keylight")
@click.pass_context
def off(ctx):
    """Turn off a single keylight"""
    click.echo(f"Turning off {ctx.obj['light'].serialNumber}")
    ctx.obj["light"].off()


@keylight.command(short_help="Toggle a keylight")
@click.pass_context
def toggle(ctx):
    """Toggle a single keylight"""
    click.echo(
        f"Toggling {ctx.obj['light'].serialNumber} to {'Off' if ctx.obj['light'].isOn else 'On'}"
    )
    if ctx.obj["light"].isOn:
        ctx.obj["light"].off()
    else:
        ctx.obj["light"].on()


@keylight.command(short_help="Set the brightness")
@click.argument("brightness", type=click.IntRange(0, 100))
@click.pass_context
def set_brightness(ctx, brightness):
    """Set the brightness of a single keylight"""
    click.echo(
        f"Setting brightness for {ctx.obj['light'].serialNumber} to {brightness}%"
    )
    ctx.obj["light"].brightness(brightness)


@keylight.command(short_help="Set the color temperature")
@click.argument("color_temp", type=click.IntRange(2900, 7000))
@click.pass_context
def set_color_temperature(ctx, color_temp):
    """Set the color temperature of a single keylight"""
    click.echo(
        f"Setting color temperature for {ctx.obj['light'].serialNumber} to {color_temp}K"
    )
    ctx.obj["light"].color(color_temp)


@keylight.command(short_help="Display information about a single keylight")
@click.pass_context
def info(ctx):
    """Display information about a single keylight"""
    click.echo(f"Getting information from {ctx.obj['light'].serialNumber}")
    info = ctx.obj["light"].info()

    click.echo(
        f"Light {ctx.obj['light'].serialNumber} at {ctx.obj['light'].address}:{ctx.obj['light'].port}"
    )
    click.echo(f"State             : {'ON' if info['on'] else 'OFF'}")
    click.echo(f"Brightness        : {info['brightness']} %")
    click.echo(f"Color Temperature : {info['temperature']} K")


@keylight.command(short_help="List all keylights on your network")
@click.pass_context
def list(ctx):
    """List all keylights found on your network"""
    all_lights = leglight.discover(ctx.obj["timeout"])

    click.echo(f"Found {len(all_lights)} lights")

    for light in all_lights:
        click.echo(f"Light {light.serialNumber} at {light.address}:{light.port}")


def start():
    keylight(obj={})


if __name__ == "__main__":
    keylight(obj={})
