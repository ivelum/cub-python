from datetime import datetime
from unittest import TestCase
from cub import config, User
from cub.timezone import utc


class APITest(TestCase):
    def setUp(self):
        config.api_key = 'sk_23a00c357cb44c358'
        self.test_user = {
            'credentials': {
                'username': '!bjDTCAdtQRldwG67secVBBHc3ifmyhcqfJzvFLFF',
                'password': 'denden',
            },
            'details': {
                'original_username': 'den',
                'first_name': 'slow',
                'last_name': 'poke',
            }
        }

    def test_user_login_and_get_by_token(self):
        user = User.login(**self.test_user['credentials'])
        for k, v in self.test_user['details'].items():
            self.assertEqual(v, getattr(user, k))
        self.assertTrue(isinstance(user.date_joined, datetime))
        utc_now = datetime.utcnow().replace(tzinfo=utc)
        self.assertTrue(user.date_joined < utc_now)

        user2 = User.get(user.token)
        self.assertEqual(user2.username, user.username)
        self.assertEqual(user2.first_name, user.first_name)
        self.assertEqual(user2.last_name, user.last_name)
        self.assertEqual(user2.date_joined, user.date_joined)

    def test_user_reload(self):
        user = User.login(**self.test_user['credentials'])
        try:
            user.reload()
        except Exception as e:
            self.fail(e)
