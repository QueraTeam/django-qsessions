import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-qsessions',
    version='0.1.6',
    description='Extends Django\'s cached_db session backend',
    long_description=README,
    author='Mohammad Javad Naderi',
    url='https://github.com/QueraTeam/django-qsessions',
    download_url='https://pypi.python.org/pypi/django-qsessions',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.10',
        'user-agents>=1.1.0',
        'django-ipware>=1.1.5',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'Topic :: Security',
    ],
)
