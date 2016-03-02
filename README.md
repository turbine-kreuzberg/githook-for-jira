[![Build Status](https://api.travis-ci.org/votum/githook-for-jira.svg?branch=master)](https://travis-ci.org/votum/githook-for-jira)

# githook for jira

username in git config must be in shape of surename.lastname
commit message must be in shape of:

```
some text BIO-25 some text

the long message
will be send to Jira as comment.
```

subject of commit message is parsed for Ticket ID.

## installation 
the githook can be installed by ansible with this role

https://github.com/votum/ansible-role-githook-for-jira

set parameters in default/main.yml to your needs.

