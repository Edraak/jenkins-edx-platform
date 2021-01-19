from calendar import timegm
import datetime
from mock import patch, Mock

from django.test import TestCase

from edraak_jwt.helpers import get_jwt_payload
from student.tests.factories import UserFactory


class EdraakJwtTests(TestCase):
    """
    Test Edraak JWT Cookie management
    """

    def setUp(self):
        self.user = UserFactory()

    def xxtest_jwt_payload(self):
        now = datetime.datetime.utcnow()
        expected_payload = {
            u'username': self.user.username,
            u'email': self.user.email,
            u'orig_iat': timegm(now.utctimetuple()),
            u'exp': now + datetime.timedelta(minutes=3),
        }

        with patch('edraak_jwt.helpers.datetime') as mock_datetime:
            mock_datetime.utcnow = Mock(return_value=now)
            payload = get_jwt_payload(self.user)

        self.assertDictEqual(expected_payload, payload)

    def xxtest_payload_of_token(self):
        ss = datetime.timedelta(days=14).total_seconds()
        print('ss = {}'.format(ss))
        print(get_jwt_payload('refresh', self.user, 'qweqweqweqwe', ss))
        self.assertTrue(False)
