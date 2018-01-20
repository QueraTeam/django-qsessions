# QSessions

QSessions extends Django's cached_db session backend and Session model to add following features:

- Sessions have a foreign key to User
- Sessions store IP and User Agent

## Installation

1. `pip install git+https://github.com/QueraTeam/django-qsessions.git`
2. In `INSTALLED_APPS` replace `'django.contrib.sessions'` with `'qsessions'`.
3. In `MIDDLEWARE` or `MIDDLEWARE_CLASSES` replace `'django.contrib.sessions.middleware.SessionMiddleware'` with `'qsessions.middleware.SessionMiddleware'`.
4. Add `SESSION_ENGINE = 'qsessions.backends.cached_db'`.
5. Run `python manage.py migrate qsessions`.

For enabling location detection using GeoIP2 (`session.location`):

6. `pip install geoip2`
7. Set `GEOIP_PATH` to a directory for GeoIP2 database.
8. `python manage.py download_geoip_db` (You can add it to a cron to update DB automatically)

For clearing expired sessions from DB, run `python manage.py clearsessions`. It's recommended to add it to a daily cron job.

## Why we don't use `django-user-sessions`?

It has the same functionality, but it's based on `db` backend. We need a cache
to be able to handle lots of sessions.

We got ideas and some codes from [django-user-sessions](https://github.com/Bouke/django-user-sessions).

## TODO

- Write tests

Contributions are welcome!

## License

MIT