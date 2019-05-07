import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

dev_requirements = [
    'geoip2==2.9.0',  # for testing GeoIP2
    'pytest==4.0.2',
    'pytest-cov==2.6.0',
    'pytest-django==3.4.4',
]

setup(
    name='django-qsessions',
    version='0.2.1',
    description='Extends Django\'s cached_db session backend',
    long_description=README,
    author='Mohammad Javad Naderi',
    url='https://github.com/QueraTeam/django-qsessions',
    download_url='https://pypi.python.org/pypi/django-qsessions',
    license='MIT',
    packages=find_packages('.', include=('qsessions', 'qsessions.*')),
    include_package_data=True,
    install_requires=[
        'Django>=1.10',
        'user-agents>=1.1.0',
        'django-ipware>=1.1.5',
    ],
    extras_require={'dev': dev_requirements},
    tests_require=dev_requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Security',
    ],
)
