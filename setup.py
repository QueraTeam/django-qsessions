import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-qsessions',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    description='Extends Django\'s cached_db sessions backend',
    long_description=README,
    url='https://gitlab.com/codamooz/reusable-libs/django-qsessions',
    install_requires=[
        'Django>=1.11.2',
        'user-agents>=1.1.0',
        'django-ipware>=1.1.5',
    ]
)
