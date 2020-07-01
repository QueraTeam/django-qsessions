# 0.5.0

- Drop support for Python 2.
- Use `ipware.get_client_ip` instead of `ipware.ip.get_real_ip` (which is removed since `django-ipware==3.0.0`)
- Format source code using [black](https://github.com/psf/black)

Thanks [@sevdog](https://github.com/sevdog)

# 0.4.1

- Updated `download_geoip_db` management command to use new Maxmind download URLs, and provide license key.

Thanks [@akx](https://github.com/akx)

# 0.4.0

- Added Django 3.0 to support matrix.
- Removed Python 3.4 from support matrix.

# 0.3.0

- Added `qsessions.backends.db` session backend.

Thanks [@willstott101](https://github.com/willstott101)

# 0.2.1

- Added support for Django 2.2.

Thanks [@akx](https://github.com/akx)

# 0.2.0

- Added support for Python 3.7, Django 2.1.
- Used pytest for testing.
- Improved session delete performance (reduce number of queries)
- Refactored codes

Thanks [@akx](https://github.com/akx), [@saeed617](https://github.com/saeed617)

# 0.1.6

- Improve docs

# 0.1.5

- Fixed a bug when User Agent is an empty string

# 0.1.4

- Fixed migrations for `created_at` field.
