QSessions
=========

QSessions extends Django's cached_db session backend and Session model to add following features:

- Sessions have a foreign key to User
- Sessions store IP and User Agent

## Installation

1. `pip install git+ssh://git@gitlab.com/codamooz/reusable-libs/django-qsessions.git`
2. In `INSTALLED_APPS` replace `'django.contrib.sessions'` with `'qsessions'`.
3. In `MIDDLEWARE` or `MIDDLEWARE_CLASSES` replace `'django.contrib.sessions.middleware.SessionMiddleware'` with `'qsessions.middleware.SessionMiddleware'`.
4. Add `SESSION_ENGINE = 'qsessions.backends.cached_db'`.
5. Run `python manage.py migrate qsessions`.
