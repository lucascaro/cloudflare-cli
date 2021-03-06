"""
Cloudflare helper.
"""
import click
import CloudFlare


def get_zone_id(ctx, param, zone_name):
    """Return the id for a zone by name."""
    del ctx #unused
    del param #unused
    cf = CloudFlare.CloudFlare()
    zones = cf.zones.get(params={'name': zone_name})
    if len(zones) != 1:
        raise click.ClickException('Invalid zone name: {}'.format(zone_name))
    return (zones[0]['id'], zones[0]['name'])

def get_all_zones():
    """Return a list of all available zones."""
    cf = CloudFlare.CloudFlare(raw=True)
    page_number = 0
    total_pages = 1
    all_zones = []
    while page_number < total_pages:
        page_number += 1
        raw_results = cf.zones.get(params={'per_page':100, 'page':page_number})
        zones = raw_results['result']
        all_zones += zones
        total_pages = raw_results['result_info']['total_pages']
    return all_zones

def purge_all(zone_id):
    """Purge all cache for a zone id."""
    cf = CloudFlare.CloudFlare()
    return cf.zones.purge_cache.delete(zone_id, data={'purge_everything': True})


def normalize_urls(zone_name, files):
    """Return a function that builds absolute URLs."""
    def normalize_url(url):
        """Prepend the zone name if the url is not absolute."""
        # print(url)
        if not url.startswith('http://') and not url.startswith('https://'):
            return 'https://{}/{}'.format(zone_name, url.replace('//', '/'))
        return url
    return list(map(normalize_url, files))

def purge_files(zone_id, zone_name, files):
    """Purge specific URLs in a zone id."""
    cf = CloudFlare.CloudFlare()
    urls = normalize_urls(zone_name, files)
    click.echo(urls)
    return cf.zones.purge_cache.delete(zone_id, data={'files': urls})
