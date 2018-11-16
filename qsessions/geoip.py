from __future__ import unicode_literals

import warnings
from django.contrib.gis.geoip2 import HAS_GEOIP2


def ip_to_location_info(ip):
    """
    Get a dictionary of location info for a given IP address.

    The format of the dictionary is the same provided by the functions
    in django.contrib.gis.geoip2.base.GeoIP2.
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
        return g.city(ip)
    except Exception:
        try:
            return g.country(ip)
        except Exception as e:
            warnings.warn(str(e))


def ip_to_location(ip):
    """
    Transform an IP address into an approximate location.

    Example output:

    * Zwolle, The Netherlands
    * The Netherlands
    * None
    """
    loc = ip_to_location_info(ip)
    if not loc:
        return None

    if loc.get('country_name'):
        if loc.get('city'):
            return '{}, {}'.format(loc['city'], loc['country_name'])
        return loc['country_name']

    return None
