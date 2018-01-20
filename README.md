# Django QSessions

QSessions extends Django's `cached_db` session backend and `Session` model to add following features:

- Sessions have a foreign key to User
- Sessions store IP and User Agent

## Installation

1. Make sure you've [configured your cache](https://docs.djangoproject.com/en/dev/topics/cache/).
If you have multiple caches defined in `CACHES`, Django will use the default cache. To use another
cache, set `SESSION_CACHE_ALIAS` to the name of that cache.
2. `pip install django-qsessions`
3. In `INSTALLED_APPS` replace `'django.contrib.sessions'` with `'qsessions'`.
4. In `MIDDLEWARE` or `MIDDLEWARE_CLASSES` replace `'django.contrib.sessions.middleware.SessionMiddleware'` with `'qsessions.middleware.SessionMiddleware'`.
5. Add `SESSION_ENGINE = 'qsessions.backends.cached_db'`.
6. Run `python manage.py migrate qsessions`.

For enabling location detection using GeoIP2 (`session.location`):

7. `pip install geoip2`
8. Set `GEOIP_PATH` to a directory for storing GeoIP2 database.
9. `python manage.py download_geoip_db` (You can add it to a cron job to update GeoIP2 DB automatically)

For clearing expired sessions from DB, run `python manage.py clearsessions`. It's recommended to add it to a daily cron job.

## Why we don't use `django-user-sessions`?

`django-user-sessions` has the same functionality, but it's based on `db` backend. We need a cache
to improve performance and be able to handle lots of sessions.

We got ideas and some codes from [django-user-sessions](https://github.com/Bouke/django-user-sessions).

## TODO

- Write better documentation.
  - Explain how it works (in summary)
  - Explain how to query sessions based on users, and delete sessions
  - Add more details to existing documentation.
- Write tests (for latest Python and Django versions)
- Performance benchmark (and compare with Django's `cached_db`)

Contributions are welcome!

## License

MIT