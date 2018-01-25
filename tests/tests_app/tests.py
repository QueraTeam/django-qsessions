from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import CreateError
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from qsessions import IP_SESSION_KEY, USER_AGENT_SESSION_KEY
from qsessions.backends.cached_db import SessionStore
from qsessions.models import Session


class MiddlewareTest(TestCase):
    def test_unmodified_session(self):
        self.client.get('/', HTTP_USER_AGENT='TestUA/1.1')
        self.assertNotIn(settings.SESSION_COOKIE_NAME, self.client.cookies)

    def test_modify_session(self):
        self.client.get('/modify_session/', HTTP_USER_AGENT='TestUA/1.1')
        self.assertIn(settings.SESSION_COOKIE_NAME, self.client.cookies)
        session = Session.objects.get(
            pk=self.client.cookies[settings.SESSION_COOKIE_NAME].value
        )
        self.assertEqual(session.user_agent, 'TestUA/1.1')
        self.assertEqual(session.ip, '127.0.0.1')

    def test_login(self):
        admin_login_url = reverse('admin:login')
        user = User.objects.create_superuser('bouke', '', 'secret')
        response = self.client.post(admin_login_url,
                                    data={
                                        'username': 'bouke',
                                        'password': 'secret',
                                        'this_is_the_login_form': '1',
                                        'next': '/admin/'},
                                    HTTP_USER_AGENT='TestUA/1.1')
        self.assertRedirects(response, '/admin/')
        session = Session.objects.get(
            pk=self.client.cookies[settings.SESSION_COOKIE_NAME].value
        )
        self.assertEqual(user, session.user)

    def test_long_ua(self):
        self.client.get('/modify_session/',
                        HTTP_USER_AGENT=''.join('a' for _ in range(500)))


class SessionStoreTest(TestCase):
    def setUp(self):
        self.store = SessionStore(user_agent='TestUA/1.1', ip='127.0.0.1')

    def test_untouched_init(self):
        self.assertFalse(self.store.modified)
        self.assertFalse(self.store.accessed)

    def test_auth_session_key(self):
        self.assertFalse(auth.SESSION_KEY in self.store)
        self.assertFalse(self.store.modified)
        self.assertTrue(self.store.accessed)

        self.store.get(auth.SESSION_KEY)
        self.assertFalse(self.store.modified)

        self.store[auth.SESSION_KEY] = 1
        self.assertTrue(self.store.modified)

    def test_save(self):
        self.store[auth.SESSION_KEY] = 1
        self.store.save()

        session = Session.objects.get(pk=self.store.session_key)
        self.assertEqual(session.user_agent, 'TestUA/1.1')
        self.assertEqual(session.ip, '127.0.0.1')
        self.assertEqual(session.user_id, 1)
        self.assertAlmostEqual(now(), session.updated_at,
                               delta=timedelta(seconds=5))

    def test_load_unmodified(self):
        self.store[auth.SESSION_KEY] = 1
        self.store.save()
        store2 = SessionStore(session_key=self.store.session_key,
                              user_agent='TestUA/1.1', ip='127.0.0.1')
        store2.load()
        self.assertEqual(store2.user_agent, 'TestUA/1.1')
        self.assertEqual(store2.ip, '127.0.0.1')
        self.assertEqual(store2.user_id, 1)
        self.assertEqual(store2.modified, False)

    def test_load_modified(self):
        self.store[auth.SESSION_KEY] = 1
        self.store.save()
        store2 = SessionStore(session_key=self.store.session_key,
                              user_agent='TestUA/1.1', ip='8.8.8.8')
        store2.load()
        self.assertEqual(store2.user_agent, 'TestUA/1.1')
        self.assertEqual(store2.ip, '8.8.8.8')
        self.assertEqual(store2.user_id, 1)
        self.assertEqual(store2.modified, True)

    def test_duplicate_create(self):
        s1 = SessionStore(session_key='DUPLICATE', user_agent='TestUA/1.1', ip='127.0.0.1')
        s1.create()
        s2 = SessionStore(session_key='DUPLICATE', user_agent='TestUA/1.1', ip='127.0.0.1')
        s2.create()
        self.assertNotEqual(s1.session_key, s2.session_key)

        s3 = SessionStore(session_key=s1.session_key, user_agent='TestUA/1.1', ip='127.0.0.1')
        with self.assertRaises(CreateError):
            s3.save(must_create=True)

    def test_delete(self):
        # not persisted, should just return
        self.store.delete()

        # create, then delete
        self.store.create()
        session_key = self.store.session_key
        self.store.delete()

        # non-existing sessions, should not raise
        self.store.delete()
        self.store.delete(session_key)

    def test_clear(self):
        """
        Clearing the session should clear all non-browser information
        """
        self.store[auth.SESSION_KEY] = 1
        self.store.clear()
        self.store.save()

        session = Session.objects.get(pk=self.store.session_key)
        self.assertEqual(session.user_id, None)


class ModelTest(TestCase):
    def test_get_decoded(self):
        store = SessionStore(user_agent='TestUA/1.1', ip='127.0.0.1')
        store[auth.SESSION_KEY] = 1
        store['foo'] = 'bar'
        store.save()

        session = Session.objects.get(pk=store.session_key)
        self.assertEqual(session.get_decoded(), {
            'foo': 'bar', auth.SESSION_KEY: 1,
            IP_SESSION_KEY: '127.0.0.1',
            USER_AGENT_SESSION_KEY: 'TestUA/1.1'
        })

    def test_very_long_ua(self):
        ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; ELT; ' \
             'BTRS29395; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ;  ' \
             'Embedded Web Browser from: http://bsalsa.com/; .NET CLR 2.0.50727; ' \
             '.NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; ' \
             '.NET CLR 1.1.4322; ELT; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; FDM; ' \
             '.NET4.0C; .NET4.0E; ELT)'
        store = SessionStore(user_agent=ua, ip='127.0.0.1')
        store.save()

        session = Session.objects.get(pk=store.session_key)
        self.assertEqual(session.user_agent, ua[:300])


class ClearsessionsCommandTest(TestCase):
    def test_can_call(self):
        Session.objects.create(expire_date=datetime.now() - timedelta(days=1),
                               ip='127.0.0.1')
        call_command('clearsessions')
        self.assertEqual(Session.objects.count(), 0)
