# 2.1.0 (Sep 21, 2025)

- Add support for Django 5.2.
- Make `geoip2` an optional dependency. It can be installed using the `geoip2` extra.

# 2.0.0 (Feb 23, 2025)

- Add support for Python 3.13 and drop support for Python 3.8.

Backward-incompatible changes:

- The IP is now read directly from the value of `REMOTE_ADDR`
  (instead of relying on **django-ipware**)
  for the same reason Django
  [removed](https://docs.djangoproject.com/en/5.2/releases/1.1/#removed-setremoteaddrfromforwardedfor-middleware)
  `SetRemoteAddrFromForwardedFor` middleware in 1.1.
  If you are using a reverse proxy,
  you should configure it
  to pass the real IP address in the `REMOTE_ADDR` header,
  or you can write a custom version of
  [`SetRemoteAddrFromForwardedFor` middleware](https://github.com/django/django/blob/91f18400cc0fb37659e2dbaab5484ff2081f1f30/django/middleware/http.py#L33)
  which suits your environment.
- `session.location` and `session.location_info` are now properties
  instead of methods.
- `session.device` is now a property instead of a method and returns string.
- The device object can be accessed using the new property `session.device_info`.
- User agent parsing is now done using `ua-parser` instead of `user-agents`.
  - The device object is now an instance of `ua_parser.core.Result`
    instead of `user_agents.parsers.UserAgent`.


# 1.1.5 (Jun 22, 2024)

- Add support for Python 3.12 and drop support for Python 3.7.
- Add support for Django 4.2, 5.0 and drop support for Django 3.2, 4.1.
- Fix a bug in admin ("add" and "edit" session).
- **Nov 3, 2024:** Add support for Django 5.1.

Thanks [@ataylor32](https://github.com/ataylor32), [@browniebroke](https://github.com/browniebroke)

# 1.1.4 (Sep 11, 2022)

- Add Django 4.1 support.
- Drop support for Python 3.6.
- Drop support for Django 2.2, 3.0, 3.1.

Thanks [@akx](https://github.com/akx)

# 1.1.3 (Dec 24, 2021)

- Add Django 4.0 support.
- Drop support for Django 1.11, 2.0, 2.1.

# 1.1.2 (Oct 17, 2020)

- Use gettext_lazy instead of ugettext_lazy.

Thanks [@akx](https://github.com/akx)

# 1.1.1 (Sep 10, 2020)

- Set development status to Production/Stable in setup.py.

# 1.1.0 (Sep 9, 2020)

- Link to user in admin page.

Thanks [@YazdanRa](https://github.com/YazdanRa)

# 1.0.1 (Sep 9, 2020)

- Fix N+1 problem in admin page by adding `user` to `select_related`.
- Update MANIFEST.in

Thanks [@jayvdb](https://github.com/jayvdb)

# 1.0.0 (Aug 19, 2020)

I think everything is OK for releasing `1.0.0` since django-qsessions is working fine in production for long time.

- Drop support for Django 1.10.
- Drop support for Python 3.5, since its end of life is near. Plus, maxminddb doesn't support 3.5 anymore.
- Add Django 3.1 to support matrix.

# 0.5.0 (Jul 2, 2020)

- Drop support for Python 2.
- Use `ipware.get_client_ip` instead of `ipware.ip.get_real_ip` (which is removed since `django-ipware==3.0.0`)
- Format source code using [black](https://github.com/psf/black)

Thanks [@sevdog](https://github.com/sevdog)

# 0.4.1 (Jan 21, 2020)

- Updated `download_geoip_db` management command to use new Maxmind download URLs, and provide license key.

Thanks [@akx](https://github.com/akx)

# 0.4.0 (Jan 21, 2020)

- Added Django 3.0 to support matrix.
- Removed Python 3.4 from support matrix.

# 0.3.0 (Nov 2, 2019)

- Added `qsessions.backends.db` session backend.

Thanks [@willstott101](https://github.com/willstott101)

# 0.2.1 (May 8, 2019)

- Added support for Django 2.2.

Thanks [@akx](https://github.com/akx)

# 0.2.0 (Dec 25, 2018)

- Added support for Python 3.7, Django 2.1.
- Used pytest for testing.
- Improved session delete performance (reduce number of queries)
- Refactored codes

Thanks [@akx](https://github.com/akx), [@saeed617](https://github.com/saeed617)

# 0.1.6 (Jun 18, 2018)

- Improve docs

# 0.1.5 (May 15, 2018)

- Fixed a bug when User Agent is an empty string

# 0.1.4 (Feb 5, 2018)

- Fixed migrations for `created_at` field.
