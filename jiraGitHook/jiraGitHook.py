#!/usr/bin/env python

# you may set this to your custom JIRA project key format
# or explicitly specify a single project name, e.g. 'EXAMPLE'


project_format = '[A-Z][A-Z]+'

# if not using JIRA, set this to your ticket system's issue pattern
issue_pattern = '{}-[\d]+'.format(project_format)

import getpass
import requests, base64, re
import json, git
from requests import Session

class JiraGitHook:
	def build_commit_json(self, message):

		return json.dumps({"body": message})

	def get_username(self, g):
		email = g.config('--global', '--get', 'user.name')

		return email

	def stringToBase64(self, s):
		return base64.b64encode(s.encode('utf-8'))

	def get_auth(self, username, paswd):
		base64string = self.stringToBase64(('%s:%s' % (username, paswd)).replace('\n', ''))

		return "Basic %s" % (base64string) 
		

	def prepare_request(self, url, message, auth):
		headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', "Authorization": auth}
		request = requests.Request('POST',url, data=self.build_commit_json(message), headers=headers)

		return request.prepare()

	def send_commit_message_to_jira(self, prepeared_request):
		s = Session()
		try:
			return s.send(prepeared_request)
		except:
			return "connection error!"

	def pretty_print_POST(self, req):
	    """
	    At this point it is completely built and ready
	    to be fired; it is "prepared".

	    However pay attention at the formatting used in 
	    this function because it is programmed to be pretty 
	    printed and may differ from the actual request.
	    """
	    print('{}\n{}\n{}\n\n{}'.format(
	        '-----------START-----------',
	        req.method + ' ' + req.url,
	        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
	        req.body,
	    ))

	def get_jira_url(self, g):
		try:
			return g.config('--get','user.jira')
		except Exception:
			return None

	def get_gitlab_url(self, g):
		try:
			return g.config('--get','user.gitlab')
		except Exception:
			return None

	def get_jira_api_url(self,g, ticket):

		jira_url = self.get_jira_url(g)
		if jira_url:
			return '%s/rest/api/2/issue/%s/comment' % (jira_url, ticket)
		return None

	def set_jira_url_in_git_config(self, g, jira_url):
		return g.config('--global','user.jira', jira_url)

	def get_commit_message_body(self, g):
		return g.log('-1', '--pretty=%b')

	def get_commit_hash(self, g):
		return g.log('-1', '--pretty=%H')

	def create_jira_message(self, g, gitlab_url, commit_hash, commit_subject, commit_message_body):
		return "%s\n\n%s \n\n%s/commit/%s" % (commit_subject, commit_message_body, gitlab_url, commit_hash)

	def git_hook(self, subject = None, do_debug = None):
		g = git.Git('.')

		if not subject:
			subject = g.log('-1', '--pretty=%s')

		ticket = re.search(issue_pattern, subject)

		if ticket:
			ticket = ticket.group(0)
			commit_message_body = self.get_commit_message_body(g)
			if not commit_message_body:
				return "message body not set. use empty line after subject!"

			gitlab_url = self.get_gitlab_url(g)
			if not gitlab_url:
				return "gitlab url not set!"

			jira_url = self.get_jira_api_url(g, ticket)
			if not jira_url:
				return "jira api url is not set!"

			#todo validate username is surname.lastname
			username = self.get_username(g)
			paswd = getpass.getpass('password: ')
			auth_string = self.get_auth(username, paswd)
			commit_hash = self.get_commit_hash(g)
			message = self.create_jira_message(g, gitlab_url, commit_hash, subject, commit_message_body)
			prepared_request = self.prepare_request(jira_url, message, auth_string)
			# debug
			if do_debug:
				print ('\nusername: %s' % (username))
				print (self.pretty_print_POST(prepared_request))
			return self.send_commit_message_to_jira(prepared_request)

		return ("no ticket id found!")