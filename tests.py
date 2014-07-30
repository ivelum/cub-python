from datetime import datetime
from unittest import TestCase
from cub import config, User
from cub.timezone import utc


class APITest(TestCase):
    def setUp(self):
        config.api_key = 's_23a00c357cb44c358b6d35feb5d4cac6'

    def test_login_and_get_by_token(self):
        user = User.login('den', 'denden')
        self.assertEqual('den', user.username)
        self.assertEqual('slow', user.first_name)
        self.assertEqual('poke', user.last_name)
        self.assertTrue(isinstance(user.date_joined, datetime))
        utc_now = datetime.utcnow().replace(tzinfo=utc)
        self.assertTrue(user.date_joined < utc_now)

        user2 = User.get(user.token)
        self.assertEqual(user2.username, user.username)
        self.assertEqual(user2.first_name, user.first_name)
        self.assertEqual(user2.last_name, user.last_name)
        self.assertEqual(user2.date_joined, user.date_joined)
