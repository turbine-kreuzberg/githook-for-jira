#!/usr/bin/env python

# you may set this to your custom JIRA project key format
# or explicitly specify a single project name, e.g. 'EXAMPLE'
project_format = '[A-Z][A-Z]+'

# if not using JIRA, set this to your ticket system's issue pattern
issue_pattern = '{}-[\d]+'.format(project_format)

import sys, os, re, git, getpass
#from subprocess import check_output

#teststring = "#muh"
g = git.Git('.')
ticket=g.log('-1', '--pretty=%s')
ticket = re.search(issue_pattern,ticket)

username = g.config('--get','user.email')

print 'username from git %s' % (username)
paswd = getpass.getpass('password: ')

if ticket:
    "muh %s\n" % (ticket.group(0))

else:
    print "no ticket id found"

#curl -D- -u username:password -X POST --data "{\"body\": \"$message\"}" -H "Content-Type: application/json" https://votum-projects.atlassian.net/rest/api/2/issue/