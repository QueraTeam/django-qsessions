from django.core.management.base import BaseCommand
from django.conf import settings
import urllib.request
import tarfile
import os


class Command(BaseCommand):
    help = 'Update GeoIP2 database'

    def handle(self, verbosity=0, **options):
        db_path = getattr(settings, 'GEOIP_PATH', None)
        if not db_path:
            if verbosity >= 1:
                self.stderr.write("No GEOIP_PATH defined, not downloading database.")
            return

        if not os.path.exists(db_path):
            os.makedirs(db_path)

        for url in [
            "http://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz",
            "http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz",
        ]:
            filename = os.path.join(db_path, os.path.basename(url))
            if verbosity >= 1:
                self.stdout.write('Downloading and extracting {url}...'.format(url=url))
            urllib.request.urlretrieve(url, filename)
            self.extract_tar(db_path, filename)
            os.remove(filename)

    @staticmethod
    def extract_tar(db_path, tar_path):
        with tarfile.open(tar_path) as tarball:
            for tarinfo in tarball:
                if tarinfo.name.endswith('.mmdb'):
                    tarinfo.name = os.path.basename(tarinfo.name)
                    tarball.extract(tarinfo, path=db_path)
