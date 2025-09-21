# Django QSessions

[![pypi](https://img.shields.io/pypi/v/django-qsessions.svg)](https://pypi.python.org/pypi/django-qsessions/)
[![tests ci](https://github.com/QueraTeam/django-qsessions/workflows/tests/badge.svg)](https://github.com/QueraTeam/django-qsessions/actions)
[![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/quera-org/24a6d63ff9d29d9be5399169f8199ca0/raw/pytest-coverage__main.json)](https://github.com/QueraTeam/django-qsessions/actions)
[![MIT](https://img.shields.io/github/license/QueraTeam/django-qsessions.svg)](https://github.com/QueraTeam/django-qsessions/blob/master/LICENSE.txt)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**django-qsessions** offers two extended session backends for Django.
They extend Django's `db` and `cached_db` backends (and `Session` model)
with following extra features:

- Sessions have a foreign key to User
- Sessions store IP and User Agent

These features help you implement "Session Management" and show a list
of active sessions to the user. You can display IP, location and user
agent for each session and add an option to revoke sessions.

## Comparison

Here is a brief comparison between Django's session backends (db, cache,
cached_db), and django-qsessions.

<table>
  <thead>
  <tr>
    <th rowspan="2"></th>
    <th colspan="3">django</th>
    <th colspan="2">qsessions</th>
  </tr>
  <tr>
    <th>cache</th>
    <th>db</th>
    <th>cached_db</th>
    <th>db</th>
    <th>cached_db</th>
  </tr>
  <tr>
  </thead>
  <tbody>
    <td>Performance</td>
    <td>✔✔</td>
    <td></td>
    <td>✔</td>
    <td></td>
    <td>✔</td>
  </tr>
  <tr>
    <td>Persistence</td>
    <td></td>
    <td>✔</td>
    <td>✔</td>
    <td>✔</td>
    <td>✔</td>
  </tr>
  <tr>
    <td>Foreign Key to User</td>
    <td></td>
    <td></td>
    <td></td>
    <td>✔</td>
    <td>✔</td>
  </tr>
  <tr>
    <td>Store IP and User Agent</td>
    <td></td>
    <td></td>
    <td></td>
    <td>✔</td>
    <td>✔</td>
  </tr>
</tbody>
</table>

## Compatibility

- Python: **3.9**, **3.10**, **3.11**, **3.12**, **3.13**
- Django: **4.2**, **5.0**, **5.1**, **5.2**

## Installation

If your system is in production and there are active sessions using
another session backend, you need to migrate them manually. We have no
migration script.

1.  If you want to use the `cached_db` backend, make sure you've
    [configured your
    cache](https://docs.djangoproject.com/en/dev/topics/cache/). If you
    have multiple caches defined in `CACHES`, Django will use the
    default cache. To use another cache, set `SESSION_CACHE_ALIAS` to
    the name of that cache.

2.  Install the latest version from PyPI:

    ```sh
    pip install django-qsessions
    ```

3.  In settings:

    - In `INSTALLED_APPS` replace `'django.contrib.sessions'` with
      `'qsessions'`.
    - In `MIDDLEWARE` or `MIDDLEWARE_CLASSES` replace
      `'django.contrib.sessions.middleware.SessionMiddleware'` with
      `'qsessions.middleware.SessionMiddleware'`.
    - Set `SESSION_ENGINE` to:
      - `'qsessions.backends.cached_db'` if you want to use
        `cached_db` backend.
      - `'qsessions.backends.db'` if you want to use `db` backend.

4.  Run migrations to create `qsessions.models.Session` model.

    ```sh
    python manage.py migrate qsessions
    ```

### Use GeoIP2 (optional)

To enable location detection using GeoIP2, you'll need to follow a few extra steps:

1.  Install `django-qsessions` with the `geoip2` extra:

    ```sh
    pip install "django-qsessions[geoip2]"
    ```

2.  Set `GEOIP_PATH` to a directory in Django settings for storing GeoIP2
    database.

3.  Run the following command to download the latest GeoIP2 database. You
    can add this command to a cron job to update the GeoIP2 DB
    automatically. Due to [Maxmind license
    changes](https://blog.maxmind.com/2019/12/18/significant-changes-to-accessing-and-using-geolite2-databases/),
    you will need to acquire and use a license key for downloading the
    databases. You can pass the key on the command line or in the
    `MAXMIND_LICENSE_KEY` environment variable.

    ```sh
    python manage.py download_geoip_db -k mykey
    ```

## Usage

django-qsessions has a custom `Session` model with following extra
fields: `user`, `user_agent`, `created_at`, `updated_at`, `ip`.

Get a user's sessions:

```python
user.session_set.filter(expire_date__gt=timezone.now())
```

Delete a session:

```python
# Deletes the session from both the database and the cache.
session.delete()
```

Logout a user:

```python
user.session_set.all().delete()
```

Get session creation time (user login time):

```python
>>> session.created_at
datetime.datetime(2018, 6, 12, 17, 9, 17, 443909, tzinfo=<UTC>)
```

Get IP and user agent:

```python
>>> session.ip
'127.0.0.1'
>>> session.user_agent
'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'
```

Get user device (parsed user-agent string):

```python
>>> session.device
'K / Android 10 / Chrome Mobile 118.0.0.0'
>>> session.device_info.device
Device(family='K', brand='Generic_Android', model='K')
>>> session.device_info.os
OS(family='Android', major='10', minor=None, patch=None, patch_minor=None)
>>> session.device_info.user_agent
UserAgent(family='Chrome Mobile', major='118', minor='0', patch='0', patch_minor='0')
```


And if you have configured GeoIP2,
you can get location info using `.location` and `.location_info`:

```python
>>> session.location
'Tehran, Iran'

>>> session.location_info
{'city': 'Tehran', 'continent_code': 'AS', 'continent_name': 'Asia', 'country_code': 'IR', 'country_name': 'Iran', 'time_zone': 'Asia/Tehran', ...}
```

Admin page:

![image](https://user-images.githubusercontent.com/2115303/41525284-b0b258b0-72f5-11e8-87f1-8770e0094f4c.png)

### Caveats

- `session.updated_at` is not the session's exact last activity. It's
  updated each time the session object is saved in DB. (e.g. when user
  logs in, or when ip, user agent, or session data changes)
- The IP address is directly read from `request.META["REMOTE_ADDR"]`.
  If you are using a reverse proxy,
  you should configure it
  to pass the real IP address in the `REMOTE_ADDR` header.
  You can also write a custom middleware
  to set `REMOTE_ADDR` from the value of other headers
  (`X-Forwarded-For`, `X-Real-IP`, ...)
  in a safe way suitable for your environment.
  More info: [Why Django removed SetRemoteAddrFromForwardedFor](https://docs.djangoproject.com/en/5.2/releases/1.1/#removed-setremoteaddrfromforwardedfor-middleware).

## Development

- Create and activate a python virtualenv.
- Install development dependencies in your virtualenv with `pip install -e '.[dev]'`
- Install pre-commit hooks with `pre-commit install`
- Run tests with coverage:
  - `py.test --cov`

## TODO

- Write better documentation.
  - Explain how it works (in summary)
  - Add more details to existing documentation.
- Write more tests
- Performance benchmark (and compare with Django's `cached_db`)

Contributions are welcome!

## License

MIT
