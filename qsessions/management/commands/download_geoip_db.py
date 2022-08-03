import os
import re
import tarfile
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.http import urlencode


class Command(BaseCommand):
    help = "Update GeoIP2 database"

    def add_arguments(self, parser):
        default_license_key = os.environ.get("MAXMIND_LICENSE_KEY")
        parser.add_argument(
            "-k", "--maxmind-license-key", default=default_license_key, required=(not default_license_key)
        )

    def handle(self, maxmind_license_key, verbosity=0, **options):
        db_path = getattr(settings, "GEOIP_PATH", None)
        if not db_path:
            if verbosity >= 1:
                self.stderr.write("No GEOIP_PATH defined, not downloading database.")
            return

        if not os.path.exists(db_path):
            os.makedirs(db_path)

        for basename, url in [
            ("GeoLite2-City.tar.gz", self.get_download_url("GeoLite2-City", maxmind_license_key)),
            ("GeoLite2-Country.tar.gz", self.get_download_url("GeoLite2-Country", maxmind_license_key)),
        ]:
            filename = os.path.join(db_path, basename)
            if verbosity >= 1:
                redacted_url = re.sub("license_key=([^&]+)", "license_key=...", url)
                self.stdout.write(f"Downloading and extracting {redacted_url}...")
            urllib.request.urlretrieve(url, filename)
            self.extract_tar(db_path, filename, verbosity)
            os.remove(filename)

    @staticmethod
    def get_download_url(edition_id, maxmind_license_key):
        return "https://download.maxmind.com/app/geoip_download?%s" % urlencode(
            {"edition_id": edition_id, "license_key": maxmind_license_key, "suffix": "tar.gz"}
        )

    def extract_tar(self, db_path, tar_path, verbosity):
        with tarfile.open(tar_path) as tarball:
            for tarinfo in tarball:
                if tarinfo.name.endswith(".mmdb"):
                    tarinfo.name = os.path.basename(tarinfo.name)
                    tarball.extract(tarinfo, path=db_path)
                    if verbosity >= 2:
                        dest_path = os.path.join(db_path, tarinfo.name)
                        self.stdout.write(f"  => {dest_path}")
