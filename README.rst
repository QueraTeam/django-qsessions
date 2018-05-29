.. image:: https://user-images.githubusercontent.com/2115303/35397912-f00efbb4-0205-11e8-89b5-3d4f585a4588.png

.. image:: https://img.shields.io/pypi/v/django-qsessions.svg
   :target: https://pypi.python.org/pypi/django-qsessions/

.. image:: https://img.shields.io/travis/QueraTeam/django-qsessions.svg
   :target: https://travis-ci.org/QueraTeam/django-qsessions

.. image:: https://img.shields.io/github/license/QueraTeam/django-qsessions.svg
   :target: https://github.com/QueraTeam/django-qsessions/blob/master/LICENSE.txt

-------

django-qsessions is a session backend for Django that extends Django's ``cached_db`` session backend
and ``Session`` model to add following features:

- Sessions have a foreign key to User

- Sessions store IP and User Agent


Comparison
==========

Here is a brief comparison between Django's session backends (db, cache, cached_db), `django-user-sessions`_, and django-qsessions.

+-------------------------+----+--------+-----------+----------------------+------------------+
|                         | db | cache  | cached_db | django-user-sessions | django-qsessions |
+=========================+====+========+===========+======================+==================+
| Better Performance      |    | ✔✔     | ✔         |                      | ✔                |
+-------------------------+----+--------+-----------+----------------------+------------------+
| Persistent              | ✔  |        | ✔         | ✔                    | ✔                |
+-------------------------+----+--------+-----------+----------------------+------------------+
| Foreign Key to User     |    |        |           | ✔                    | ✔                |
+-------------------------+----+--------+-----------+----------------------+------------------+
| Store IP and User Agent |    |        |           | ✔                    | ✔                |
+-------------------------+----+--------+-----------+----------------------+------------------+




Requirements
============

+----------------+-----------------+
| Python version | Django versions |
+================+=================+
| 3.6            | 2.0, 1.11, 1.10 |
+----------------+-----------------+
| 3.5            | 2.0, 1.11, 1.10 |
+----------------+-----------------+
| 3.4            | 2.0, 1.11, 1.10 |
+----------------+-----------------+
| 2.7            | 1.11, 1.10      |
+----------------+-----------------+

Installation
============

Please note that if your system is in production and there are lots of active sessions
using another session backend, you need to migrate sessions manually.

(1) First, make sure you've `configured your cache`_. If you have multiple caches defined in
    ``CACHES``, Django will use the default cache. To use another cache, set ``SESSION_CACHE_ALIAS``
    to the name of that cache.

(2) Install the latest version from PyPI:

    .. code-block:: sh

        pip install django-qsessions

(3) In settings:

    - In ``INSTALLED_APPS`` replace ``'django.contrib.sessions'`` with ``'qsessions'``.

    - In ``MIDDLEWARE`` or ``MIDDLEWARE_CLASSES`` replace
      ``'django.contrib.sessions.middleware.SessionMiddleware'`` with
      ``'qsessions.middleware.SessionMiddleware'``.

    - Set ``SESSION_ENGINE`` to ``'qsessions.backends.cached_db'``.

(4) Run migrations to create ``qsessions.models.Session`` model.

    .. code-block:: sh

        python manage.py migrate qsessions

For enabling location detection using GeoIP2 (``session.location``):

(5) Install ``geoip2`` package:

    .. code-block:: sh

        pip install geoip2

(6) Set ``GEOIP_PATH`` to a directory for storing GeoIP2 database.

(7) Run the following command to download latest GeoIP2 database. You can add this command to a cron
    job to update GeoIP2 DB automatically.

    .. code-block:: sh

        python manage.py download_geoip_db

For clearing expired sessions from DB, run ``python manage.py clearsessions``. It's recommended to
add it to a daily cron job.

Why not ``django-user-sessions``?
=================================

`django-user-sessions`_ has the same functionality,
but it's based on ``db`` backend. Using a cache will improve performance.

We got ideas and some codes
from django-user-sessions. Many thanks to `Bouke Haarsma`_ for writing
django-user-sessions.

TODO
====

- Write better documentation.

  - Explain how it works (in summary)
  - Explain how to query sessions based on users, and delete sessions
  - Add more details to existing documentation.

- Write more tests

- Performance benchmark (and compare with Django's `cached_db`)

Contributions are welcome!

License
=======

MIT

.. _`configured your cache`: https://docs.djangoproject.com/en/dev/topics/cache/
.. _`django-user-sessions`: https://github.com/Bouke/django-user-sessions
.. _`Bouke Haarsma`: https://github.com/Bouke
