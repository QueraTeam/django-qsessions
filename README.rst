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
using another session backend, you need to migrate them manually. We have no migration script.

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

Usage
=====

django-qsessions has a custom ``Session`` model with following fields:
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
    for session in user.session_set.all():
        session.delete()


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

And if you have configured GeoIP2, you can call ``.location()``:

.. code-block:: python
    >>> session.location()
    'Tehran, Iran'

Admin page:

.. image:: https://user-images.githubusercontent.com/2115303/41525284-b0b258b0-72f5-11e8-87f1-8770e0094f4c.png

Caveats
-------

- Please note that bulk deleting sessions (``user.session_set.all().delete()``) does not properly
  delete sessions. It only deletes them from database, and they will remain in cache. But
  calling ``delete`` on a single session deletes it from both DB and cache. Contributions on fixing
  this are welcome.

- ``session.updated_at`` is not the session's last activity. It's updated each time the session
  object in DB is saved. (e.g. when user logs in, or when ip, user agent, or session data changes)

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
