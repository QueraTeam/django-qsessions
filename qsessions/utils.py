import warnings
from django.contrib.gis.geoip2 import HAS_GEOIP2


def ip_to_location(ip):
    """
    Transform an IP address into an approximate location.

    Example output:

    * Zwolle, The Netherlands
    * The Netherlands
    * None
    """
    if not HAS_GEOIP2:
        return None

    from django.contrib.gis.geoip2 import GeoIP2
    try:
        g = GeoIP2()
    except Exception as e:
        warnings.warn(str(e))
        return None

    try:
        loc = g.city(ip)
    except Exception:
        try:
            loc = g.country(ip)
        except Exception as e:
            warnings.warn(str(e))
            loc = None

    if not loc:
        return None

    if loc['country_name']:
        if 'city' in loc and loc['city']:
            return '{}, {}'.format(loc['city'], loc['country_name'])
        return loc['country_name']

    return None
