import sys
import unittest
import logging
import os
from tempfile import mkdtemp
from mock import MagicMock

from errbot.backends._slack.person import *

from errbot.backends.base import RoomDoesNotExistError


log = logging.getLogger(__name__)


class SlackPersonTests(unittest.TestCase):

    USER_INFO = {
        'user': {
            'name': 'test_username',
            'real_name': 'Test Real Name',
            'profile': {
                'email': 'test@mail.com'
            }
        }
    }

    def setUp(self):
        self.webClient = MagicMock()
        self.userid = 'Utest_user_id'
        self.channelid = 'Ctest_channel_id'
        self.p = SlackPerson(self.webClient, userid=self.userid, channelid=self.channelid)

    def test_username(self):
        self.webClient.users_info.return_value = SlackPersonTests.USER_INFO
        self.assertEqual(self.p.username, 'test_username')
        self.assertEqual(self.p.username, 'test_username')
        self.webClient.users_info.assert_called_once_with(user=self.userid)

    def test_username_not_found(self):
        self.webClient.users_info.return_value = {'user': None}
        self.assertEqual(self.p.username, '<Utest_user_id>')
        self.assertEqual(self.p.username, '<Utest_user_id>')
        self.webClient.users_info.assert_called_with(user=self.userid)
        self.assertEqual(self.webClient.users_info.call_count, 2)

    def test_fullname(self):
        self.webClient.users_info.return_value = SlackPersonTests.USER_INFO
        self.assertEqual(self.p.fullname, 'Test Real Name')
        self.assertEqual(self.p.fullname, 'Test Real Name')
        self.webClient.users_info.assert_called_once_with(user=self.userid)

    def test_fullname_not_found(self):
        self.webClient.users_info.return_value = {'user': None}
        self.assertEqual(self.p.fullname, '<Utest_user_id>')
        self.assertEqual(self.p.fullname, '<Utest_user_id>')
        self.webClient.users_info.assert_called_with(user=self.userid)
        self.assertEqual(self.webClient.users_info.call_count, 2)

    def test_email(self):
        self.webClient.users_info.return_value = SlackPersonTests.USER_INFO
        self.assertEqual(self.p.email, 'test@mail.com')
        self.assertEqual(self.p.email, 'test@mail.com')
        self.webClient.users_info.assert_called_once_with(user=self.userid)

    def test_email_not_found(self):
        self.webClient.users_info.return_value = {'user': None}
        self.assertEqual(self.p.email, '<Utest_user_id>')
        self.assertEqual(self.p.email, '<Utest_user_id>')
        self.webClient.users_info.assert_called_with(user=self.userid)
        self.assertEqual(self.webClient.users_info.call_count, 2)

    def test_channelname(self):
        self.webClient.conversations_list.return_value = {'channels': [{'id': self.channelid, 'name': 'test_channel'}]}
        self.assertEqual(self.p.channelname, 'test_channel')
        self.assertEqual(self.p.channelname, 'test_channel')
        self.webClient.conversations_list.assert_called_once_with()

    def test_channelname_channel_not_found(self):
        self.webClient.conversations_list.return_value = {'channels': [{'id': 'random', 'name': 'random_channel'}]}
        with self.assertRaises(RoomDoesNotExistError) as e:
            self.p.channelname

    def test_channelname_channel_empty_channel_list(self):
        self.webClient.conversations_list.return_value = {'channels': []}
        with self.assertRaises(RoomDoesNotExistError) as e:
            self.p.channelname

    def test_domain(self):
        with self.assertRaises(NotImplementedError) as e:
            self.p.domain

    def test_aclattr(self):
        self.p._username = 'aclusername'
        self.assertEqual(self.p.aclattr, '@aclusername')

    def test_person(self):
        self.p._username = 'personusername'
        self.assertEqual(self.p.person, '@personusername')
