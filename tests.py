from datetime import datetime
from unittest import TestCase

from cub import config, User
from cub.models import Organization, Member, Group, \
    objects_from_json, Country
from cub.timezone import utc


class APITest(TestCase):
    def setUp(self):
        config.api_key = 'sk_23a00c357cb44c358'
        self.test_user = {
            'credentials': {
                'username': 'support@ivelum.com',
                'password': 'SJW8Gg',
            },
            'details': {
                'original_username': 'ivelum',
                'first_name': 'do not remove of modify',
                'last_name': 'user for tests',
            }
        }

    def test_objects_from_json(self):
        group_sample = {
            'object': 'group',
            'id': 42,
            'name': 'lol',
            'deleted': True
        }
        group = objects_from_json(group_sample)
        self.assertTrue(isinstance(group, Group))
        self.assertEqual(group.id, group_sample['id'])
        self.assertEqual(group.name, group_sample['name'])
        self.assertEqual(group.deleted, group_sample['deleted'])

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
        self.assertFalse(user2.deleted)

    def test_user_reload(self):
        user = User.login(**self.test_user['credentials'])
        try:
            user.reload(expand='membership__organization')
        except Exception as e:
            self.fail(e)
        self.assertTrue(len(user.membership) > 0)
        member = user.membership[0]
        self.assertTrue(isinstance(member, Member))
        self.assertEqual(member.api_key, user.api_key)
        self.assertTrue(isinstance(member.organization, Organization))
        self.assertEqual(member.organization.api_key, user.api_key)
        self.assertFalse(member.deleted)

    def test_organizations(self):
        organizations = Organization.list(count=2)
        self.assertTrue(len(organizations) <= 2)
        for organization in organizations:
            self.assertTrue(organization.id is not None)
            self.assertTrue(organization.name is not None)
            org = Organization.get(id=organization.id)
            self.assertEqual(organization.name, org.name)
            self.assertFalse(organization.deleted)

    def test_countries(self):
        try:
            Country.list()
        except Exception as e:
            self.fail(e)
