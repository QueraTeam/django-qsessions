QSessions
=========

QSessions extends Django's cached_db session backend and Session model to add following features:

- Sessions have a foreign key to User
- Sessions store IP and User Agent

## Installation


Full documentation is located in `docs`.

Install:

    pip install git+https://github.com/QueraTeam/django-clamav.git
    pip install git+ssh://git@gitlab.com/codamooz/django-semanticui.git
    pip install git+ssh://git@gitlab.com/codamooz/django-qform.git

Add following to INSTALLED_APPS:

```
INSTALLED_APPS = (
    ...
    'django_fsm',
    'fsm_admin',
    'django_extensions',
    'nonefield',
    'semanticui',
    'django_clamav',
    'qform',
    ...
)
```