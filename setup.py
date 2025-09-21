import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="UTF-8") as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dev_requirements = [
    "pre-commit",
    "pytest>=7",
    "pytest-cov",
    "pytest-django",
]

geoip_requirements = ["geoip2>=4.1.0"]

setup(
    name="django-qsessions",
    version="2.1.0",
    description="Extended session backends for Django",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Mohammad Javad Naderi",
    url="https://github.com/QueraTeam/django-qsessions",
    download_url="https://pypi.python.org/pypi/django-qsessions",
    license="MIT",
    packages=find_packages(".", include=("qsessions", "qsessions.*")),
    include_package_data=True,
    install_requires=["Django >= 4.2", "ua-parser[regex] >= 1.0.1"],
    extras_require={
        "dev": dev_requirements + geoip_requirements,
        "geoip2": geoip_requirements,
    },
    tests_require=dev_requirements,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Django :: 5.1",
        "Framework :: Django :: 5.2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: Session",
        "Topic :: Security",
    ],
)
