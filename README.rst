================
Django QSessions
================

.. image:: https://img.shields.io/pypi/v/django-qsessions.svg
   :target: https://pypi.python.org/pypi/django-qsessions/

.. image:: https://github.com/QueraTeam/django-qsessions/workflows/Tests/badge.svg
   :target: https://github.com/QueraTeam/django-qsessions/actions

.. image:: https://img.shields.io/github/license/QueraTeam/django-qsessions.svg
   :target: https://github.com/QueraTeam/django-qsessions/blob/master/LICENSE.txt

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black

**django-qsessions** offers two extended session backends for Django.
They extend Django's ``db`` and ``cached_db`` backends (and ``Session`` model)
with following extra features:

- Sessions have a foreign key to User
- Sessions store IP and User Agent

These features help you implement "Session Management" and show a list of active sessions to the user.
You can display IP, location and user agent for each session and add an option to revoke sessions.


Comparison
==========

Here is a brief comparison between Django's session backends (db, cache, cached_db), and django-qsessions.

+-------------------------+-------------------------+----------------+
|                         | django                  | qsessions      |
+                         +-------+-----+-----------+----+-----------+
|                         | cache | db  | cached_db | db | cached_db |
+=========================+=======+=====+===========+====+===========+
| Performance             | ✔✔    |     | ✔         |    | ✔         |
+-------------------------+-------+-----+-----------+----+-----------+
| Persistence             |       | ✔   | ✔         | ✔  | ✔         |
+-------------------------+-------+-----+-----------+----+-----------+
| Foreign Key to User     |       |     |           | ✔  | ✔         |
+-------------------------+-------+-----+-----------+----+-----------+
| Store IP and User Agent |       |     |           | ✔  | ✔         |
+-------------------------+-------+-----+-----------+----+-----------+


Compatibility
=============

- Python: **3.7**, **3.8**, **3.9**, **3.10**
- Django: **3.2**, **4.0**, **4.1**

Installation
============

If your system is in production and there are active sessions using another session backend,
you need to migrate them manually. We have no migration script.

(1) If you want to use the ``cached_db`` backend, make sure you've
    `configured your cache`_. If you have multiple caches defined in ``CACHES``, Django
    will use the default cache. To use another cache, set ``SESSION_CACHE_ALIAS`` to the
    name of that cache.

(2) Install the latest version from PyPI:

    .. code-block:: sh

        pip install django-qsessions

(3) In settings:

    - In ``INSTALLED_APPS`` replace ``'django.contrib.sessions'`` with ``'qsessions'``.

    - In ``MIDDLEWARE`` or ``MIDDLEWARE_CLASSES`` replace
      ``'django.contrib.sessions.middleware.SessionMiddleware'`` with
      ``'qsessions.middleware.SessionMiddleware'``.

    - Set ``SESSION_ENGINE`` to:

      - ``'qsessions.backends.cached_db'`` if you want to use ``cached_db`` backend.
      - ``'qsessions.backends.db'`` if you want to use ``db`` backend.

(4) Run migrations to create ``qsessions.models.Session`` model.

    .. code-block:: sh

        python manage.py migrate qsessions

To enable location detection using GeoIP2 (optional):

(5) Install ``geoip2`` package:

    .. code-block:: sh

        pip install geoip2

(6) Set ``GEOIP_PATH`` to a directory for storing GeoIP2 database.

(7) Run the following command to download latest GeoIP2 database. You can add this
    command to a cron job to update GeoIP2 DB automatically.
    Due to `Maxmind license changes`_ you will need to acquire and use a license key for
    downloading the databases.  You can pass the key on the command line, or in the ``MAXMIND_LICENSE_KEY``
    environment variable.

    .. code-block:: sh

        python manage.py download_geoip_db -k mykey

Usage
=====

django-qsessions has a custom ``Session`` model with following extra fields:
``user``, ``user_agent``, ``created_at``, ``updated_at``, ``ip``.

Getting a user's sessions:

.. code-block:: python

    user.session_set.filter(expire_date__gt=timezone.now())

Deleting a session:

.. code-block:: python

    # Deletes session from both DB and cache
    session.delete()

Logout a user:

.. code-block:: python

    user.session_set.all().delete()

Session creation time (user login time):

.. code-block:: python

    >>> session.created_at
    datetime.datetime(2018, 6, 12, 17, 9, 17, 443909, tzinfo=<UTC>)

IP and user agent:

.. code-block:: python

    >>> session.ip
    '127.0.0.1'
    >>> session.user_agent
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

And if you have configured GeoIP2, you can call ``.location()``, ``.location_info()``:

.. code-block:: python

    >>> session.location()
    'Tehran, Iran'

    >>> session.location_info()
    {'city': 'Tehran', 'continent_code': 'AS', 'continent_name': 'Asia', 'country_code': 'IR', 'country_name': 'Iran', 'time_zone': 'Asia/Tehran', ...}

Admin page:

.. image:: https://user-images.githubusercontent.com/2115303/41525284-b0b258b0-72f5-11e8-87f1-8770e0094f4c.png

Caveats
-------

- ``session.updated_at`` is not the session's last activity. It's updated each time the session
  object in DB is saved. (e.g. when user logs in, or when ip, user agent, or session data changes)

Why not ``django-user-sessions``?
=================================

`django-user-sessions`_ has the same functionality,
but only extends the ``db`` backend. Using a cache can improve performance.

We got ideas and some codes from django-user-sessions.
Many thanks to `Bouke Haarsma`_ for writing django-user-sessions.

Development
===========

- Create and activate a python virtualenv.

- Install development dependencies in your virtualenv with ``pip install -e '.[dev]'``

- Install pre-commit hooks with ``pre-commit install``

- Run tests with coverage:

  - ``py.test --cov --ds tests.settings_db``
  - ``py.test --cov --ds tests.settings_cached_db``

TODO
====

- Write better documentation.

  - Explain how it works (in summary)
  - Add more details to existing documentation.

- Write more tests

- Performance benchmark (and compare with Django's ``cached_db``)

Contributions are welcome!

License
=======

MIT

.. _`configured your cache`: https://docs.djangoproject.com/en/dev/topics/cache/
.. _`django-user-sessions`: https://github.com/Bouke/django-user-sessions
.. _`Bouke Haarsma`: https://github.com/Bouke
.. _`Maxmind license changes`: https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/
