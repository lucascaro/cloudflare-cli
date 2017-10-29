"""
    Cloudflare CLI
"""
import click
from . import cf

@click.group()
def cli():
    """Simple Cloudflare command line interface."""

def abort_if_false(ctx, param, value):
    """Abort the command if thre is no value."""
    del param #unused
    if not value:
        ctx.abort()

@cli.command(name='purge-all')
@click.argument('zone', callback=cf.get_zone_id)
@click.option('-y', '--yes', is_flag=True, callback=abort_if_false,
              expose_value=False, default=False,
              prompt='Are you sure you want to purge all files?')
def purge_all(zone):
    """Purge all files in a zone."""
    zone_id, zone_name = zone
    click.echo('Purge all files on zone {} ({})'.format(zone_name, zone_id))
    cf.purge_all(zone_id)


@cli.command()
@click.argument('zone', callback=cf.get_zone_id)
@click.argument('files', nargs=-1)
@click.option('-i', '--input', '_input', type=click.File('r'))
def purge(zone, files, _input):
    """Purge the cache for a zone."""
    click.echo(zone)
    zone_id, zone_name = zone
    if files:
        click.echo('Purge cache for {} in {}'.format(files, zone_name))
        cf.purge_files(zone_id, zone_name, files)
    if _input:
        click.echo('Purge cache from file in {}'.format(zone_name))
        files = _input.read().splitlines()
        cf.purge_files(zone_id, zone_name, files)

@cli.group(name='zone')
def zone_group():
    """Interact with zones."""

@zone_group.command(name='list')
def list_command():
    """List all zones."""
    click.echo('All available zones:')
    zones = cf.get_all_zones()
    for zone in zones:
        print(zone['id'], zone['name'])
