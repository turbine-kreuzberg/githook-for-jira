#!/usr/bin/env python

# you may set this to your custom JIRA project key format
# or explicitly specify a single project name, e.g. 'EXAMPLE'
project_format = '[A-Z][A-Z]+'

# if not using JIRA, set this to your ticket system's issue pattern
issue_pattern = '{}-[\d]+'.format(project_format)

import sys, os, re, git, getpass
import requests, base64
import json
from requests import Session
from requests.auth import HTTPBasicAuth

class git_hook_for_jira:
	def build_commit_json(self, message):

		return json.dumps({"body": message})

	def get_user():
		email = g.config('--get','user.name')

		return email

	def get_auth(self, paswd):
		base64string = base64.encodestring('%s:%s' % (get_user(), paswd)).replace('\n', '')

		return "Basic %s" % (base64string) 
		

	def prepare_request(self, url, message, paswd):
		headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8', "Authorization": get_auth(paswd)}
		request = requests.Request('POST',url, data=build_commit_json(message), headers=headers)

		return request.prepare()

	def send_commit_message_to_jira(self, prepeared_request):
		s = Session(prepeared_request)

		return s.send(prepeared_request)

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


g = git.Git('.')
ticket = g.log('-1', '--pretty=%s')
ticket = re.search(issue_pattern,ticket)
message = g.log('-1', '--pretty=%b')


username = g.config('--get','user.email')
print build_commit_json(message)
print 'username from git %s' % (get_user())
paswd = getpass.getpass('password: ')

if ticket:
	ticket = ticket.group(0)
	url = 'https://votum-projects.atlassian.net/rest/api/2/issue/%s/comment' % (ticket)
	send_commit_message_to_jira(prepare_request(url, message, paswd))
	
else:
    print "no ticket id found"

#curl -D- -u username:password -X POST --data "{\"body\": \"$message\"}" -H "Content-Type: application/json" 