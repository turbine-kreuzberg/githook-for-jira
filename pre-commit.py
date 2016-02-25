#!/usr/bin/env python

# you may set this to your custom JIRA project key format
# or explicitly specify a single project name, e.g. 'EXAMPLE'
project_format = '[A-Z][A-Z]+'

# if not using JIRA, set this to your ticket system's issue pattern
issue_pattern = '{}-[\d]+'.format(project_format)

import sys, os, re, git, getpass
import requests
import json
#from subprocess import check_output

#teststring = "#muh"


def build_commit_json(message):
	return "{\"body\": \"%s\"}" % (message)

def get_user():
	return g.config('--get','user.email')

def send_commit_message_to_jira(url, ticket, message, paswd):
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, data=build_commit_json(message), headers=headers, auth=(get_user(), paswd))
	print r




g = git.Git('.')
ticket = g.log('-1', '--pretty=%s')
ticket = re.search(issue_pattern,ticket)
message = g.log('-1', '--pretty=%b')
url = 'https://votum-projects.atlassian.net/rest/api/2/issue/'

username = g.config('--get','user.email')
print message
print 'username from git %s' % (username)
paswd = getpass.getpass('password: ')

if ticket:
	send_commit_message_to_jira (url, ticket.group(0), message, paswd)

else:
    print "no ticket id found"

#curl -D- -u username:password -X POST --data "{\"body\": \"$message\"}" -H "Content-Type: application/json" 