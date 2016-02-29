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
import os
import sys
import getpass
from git.test.lib import (
    TestBase,
    assert_equal,
    assert_not_equal,
    with_rw_repo,
    fixture_path,
    StringProcessAdapter
)
from mock import mock

sys.path.append('..')      # XXX Probably needed to import your code
from jiraGitHook import JiraGitHook

class MockHTTPResponse(object):
	def __init__(self, status, body):
		self.status = status
		self.body = body

	def read(self):
		return self.body

class TestJiraGitHook(unittest.TestCase):

    def setUp(self):
        self.g = git.Git('.')
        try:
            self.g.config('--global','--unset', 'user.jira')
        except:
            pass

    def tearDown(self):
        try:
            self.g.config('--global','--unset', 'user.jira')
        except:
            pass

    def test_git_api_url_not_set(self):
        jiraGitHook = JiraGitHook()
        subject = "this is MYTICKET-44"

        assert_equal(jiraGitHook.git_hook(subject), "jira api url is not set!")

    def test_ticket_not_set(self):
        jiraGitHook = JiraGitHook()
        subject = "some line."

        assert_equal(jiraGitHook.git_hook(subject), "no ticket id found!")

    @mock.patch('getpass.getpass')
    def test_git_hook_wrong_url(self, getpw):
        getpw.return_value = 'pass'
        self.g = git.Git('.')
        jira_url = 'http://test.jira.me/rest/api/2/issue//comment'
        subject = "this is MYTICKET-44"
        jiraGitHook = JiraGitHook()
        jiraGitHook.set_jira_url_in_git_config(self.g, jira_url)

        assert_equal(jiraGitHook.git_hook(subject), "connection error!")

    @mock.patch('getpass.getpass')
    def test_git_hook_add_commit(self, getpw):
        api_mock = mock.Mock()
        #api_mock.send.return_value = MockHTTPResponse(201, '')

        getpw.return_value = 'pass'
        self.g = git.Git('.')
        jira_url = 'http://test.jira.me/rest/api/2/issue//comment'
        subject = "this is MYTICKET-44"
        jiraGitHook = JiraGitHook()
        jiraGitHook.send_commit_message_to_jira = mock.Mock(return_value=MockHTTPResponse(201, ''))
        ret = jiraGitHook.set_jira_url_in_git_config(self.g, jira_url)
        #ret = jiraGitHook.git_hook(subject)
        assert_equal(jiraGitHook.git_hook(subject).status, 201)





unittest.main()