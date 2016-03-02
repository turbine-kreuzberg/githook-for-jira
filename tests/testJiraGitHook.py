#!/usr/bin/env python
#
#  XXX  Identifying information about tests here.
#
#===============
#  This is based on a skeleton test file, more information at:
#
#     https://github.com/linsomniac/python-unittest-skeleton

import unittest

import git
import sys

from mock import mock
sys.path.append('..')      # XXX Probably needed to import your code
from jiraGitHook.jiraGitHook import JiraGitHook

class MockHTTPResponse(object):
	def __init__(self, status, body):
		self.status = status
		self.body = body

	def read(self):
		return self.body

class TestJiraGitHook(unittest.TestCase):

    def setUp(self):
        self.g = git.Git('.')
        JiraGitHook.get_username = mock.Mock(return_value='surname.lastname')
        JiraGitHook.get_jira_url = mock.Mock(return_value='http://test.jira.me')

    def tearDown(self):
        pass
    def test_mocked_get_username(self):
        jiraGitHook = JiraGitHook()

        self.assertEquals(jiraGitHook.get_username(self.g), 'surname.lastname')
    def test_get_jira_api_url(self):
        jiraGitHook = JiraGitHook()

        self.assertEquals(jiraGitHook.get_jira_api_url(self.g, 'MUH-99'), 'http://test.jira.me/rest/api/2/issue/MUH-99/comment')

    def test_git_api_url_not_set(self):
        jiraGitHook = JiraGitHook()
        jiraGitHook.get_commit_message_body = mock.Mock(return_value='the message')
        jiraGitHook.get_gitlab_url = mock.Mock(return_value='http://git.me/project')
        jiraGitHook.get_jira_url = mock.Mock(return_value=None)
        subject = "this is MYTICKET-44"

        self.assertEquals(jiraGitHook.git_hook(subject), "jira api url is not sete!")

    def test_git_message_body_not_set(self):
        jiraGitHook = JiraGitHook()

        subject = "this is MYTICKET-44"

        self.assertEquals(jiraGitHook.git_hook(subject), "message body not set. use empty line after subject!")

    def test_ticket_not_set(self):
        jiraGitHook = JiraGitHook()
        subject = "some line."

        self.assertEquals(jiraGitHook.git_hook(subject), "no ticket id found!")

    #@mock.patch('getpass.getpass')
    #def test_git_hook_wrong_url(self, getpw):
    #    getpw.return_value = 'pass'
    #    self.g = git.Git('.')
    #    subject = "this is MYTICKET-44"
    #    jiraGitHook = JiraGitHook()
    #    jiraGitHook.set_jira_url_in_git_config = mock.Mock(return_value='http://test.jira.moope/rest/api/2/issue//comment')

    #    self.assertEquals(jiraGitHook.git_hook(subject), "connection error!")

    @mock.patch('getpass.getpass')
    def test_git_hook_add_commit(self, getpw):
        getpw.return_value = 'pass'
        subject = "this is MYTICKET-44"
        jiraGitHook = JiraGitHook()
        jiraGitHook.get_commit_message_body = mock.Mock(return_value='the message')
        jiraGitHook.get_gitlab_url = mock.Mock(return_value='http://git.me/project')
        jiraGitHook.send_commit_message_to_jira = mock.Mock(return_value=MockHTTPResponse(200, ''))

        self.assertEquals(jiraGitHook.git_hook(subject).status, 200)

    def test_prepared_request(self):
        jiraGitHook = JiraGitHook()
        prepared_request = jiraGitHook.prepare_request('http://someurl/ticket/comment', 'the message', 'Basic: somestring')

        self.assertEquals(prepared_request.body, '{"body": "the message"}')
        self.assertEquals(prepared_request.url, 'http://someurl/ticket/comment')

    def test_create_jira_message(self):
        'http://git.votum-media.net/bio/bio-circle/commit/4e63307c35eaa0288d820be9dc2b5f0157435579'
        jiraGitHook = JiraGitHook()
        jira_message = jiraGitHook.create_jira_message(self.g, 'http://git.me/project','4e63307c35eaa0288d820be9dc2b5f0157435579', 'the message')

        self.assertEquals(jira_message,
                          "the message \n\nhttp://git.me/project/commit/4e63307c35eaa0288d820be9dc2b5f0157435579")







unittest.main()