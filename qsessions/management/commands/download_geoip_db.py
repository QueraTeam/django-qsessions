from django.core.management.base import BaseCommand
from django.conf import settings
import urllib.request
import tarfile
import os


class Command(BaseCommand):
    help = 'Update GeoIP2 database'

    CITY_DB = "http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz"
    COUNTRY_DB = "http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        db_path = getattr(settings, 'GEOIP_PATH', None)
        if not db_path:
            return

        if not os.path.exists(db_path):
            os.makedirs(db_path)

        db_path_city = os.path.join(db_path, 'city.tar.gz')
        db_path_country = os.path.join(db_path, 'country.tar.gz')

        urllib.request.urlretrieve(self.CITY_DB, db_path_city)
        urllib.request.urlretrieve(self.COUNTRY_DB, db_path_country)

        tar_city = tarfile.open(db_path_city)
        for tarinfo in tar_city:
            if tarinfo.name.endswith('.mmdb'):
                tarinfo.name = os.path.basename(tarinfo.name)
                tar_city.extract(tarinfo, path=db_path)
        tar_city.close()

        tar_country = tarfile.open(db_path_country)
        for tarinfo in tar_country:
            if tarinfo.name.endswith('.mmdb'):
                tarinfo.name = os.path.basename(tarinfo.name)
                tar_country.extract(tarinfo, path=db_path)
        tar_country.close()

        os.remove(db_path_city)
        os.remove(db_path_country)
