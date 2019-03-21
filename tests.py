from datetime import datetime
from unittest import TestCase

from cub import config, User
from cub.models import Organization, Member, Group, \
    objects_from_json, Country, Lead, CubObject
from cub.timezone import utc
from cub.transport import urlify


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

    def test_leads(self):
        leads = Lead.list(count=2)
        self.assertTrue(len(leads) <= 2)
        for lead in leads:
            self.assertTrue(lead.data)
            self.assertTrue(lead.id is not None)
            self.assertTrue(lead.email is not None)
            ld = Lead.get(id=lead.id)
            self.assertEqual(lead.email, ld.email)
            self.assertFalse(lead.deleted)

    def test_nested_query(self):
        cub_obj = CubObject(id='cub_1')
        cases = (
            ({'str': 'str', 'int': 1,
              'True': True, 'False': False, 'None': None,
              'true': 'true', 'false': 'false', 'null': 'null', 'number': '1'},
             {'str': 'str', 'int': 1,
              'True': 'true', 'False': 'false', 'None': 'null',
              'true': '"true"', 'false': '"false"', 'null': '"null"',
              'number': '"1"'}),
            ({'obj': cub_obj},
             {'obj': 'cub_1'}),
            ({'dict': {'key': 'val'}},
             {'dict[key]': 'val'}),
            ({'dict': {'key': 'val'}},
             {'dict[key]': 'val'}),
            ({'list': [1, 'str', None], 'dict': {'dkey': 'dval'}, 'key': 'val'},
             {'list[0]': 1, 'list[1]': 'str', 'list[2]': 'null',
              'dict[dkey]': 'dval', 'key': 'val'}),
            ({'empty_list': [], 'empty_dict': {}},
             {}),
            ({'root': {'dict': ['val']}},
             {'root[dict][0]': 'val'}),
            ({'root': {'dict': ['val1', 'val2']}},
             {'root[dict][0]': 'val1', 'root[dict][1]': 'val2'}),
            ({'root': {'dict1': ['val1'], 'dict2': ['val2']}},
             {'root[dict1][0]': 'val1', 'root[dict2][0]': 'val2'}),
            ({'root': [{'key': 'val'}]},
             {'root[0][key]': 'val'}),
            ({'root': [[[1], 1], 1]},
             {'root[0][0][0]': 1, 'root[0][1]': 1, 'root[1]': 1}),
            ({'list': [
                 {'name': 'John', 'age': 20},
                 {'name': 'Kate', 'age': 18},
                 {'name': 'Smith', 'age': 30},
             ]},
             {'list[0][name]': 'John', 'list[0][age]': 20,
              'list[1][name]': 'Kate', 'list[1][age]': 18,
              'list[2][name]': 'Smith', 'list[2][age]': 30}),
        )
        for data, expected in cases:
            self.assertEqual(urlify(data), expected)
