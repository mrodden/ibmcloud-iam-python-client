# ibmcloud-iam-python-client

[![Build Status](https://app.travis-ci.com/mrodden/ibmcloud-iam-python-client.svg?branch=master)](https://app.travis-ci.com/mrodden/ibmcloud-iam-python-client)

This project is a collection of Python modules used for interacting with IBMCloud IAM API services.

Currently it includes support for:

  - Requesting IAM tokens using an intelligent caching mechanism (`TokenManager`)
  - Parsing IAM tokens and verifying their cryptographic signatures
  - Checking user action authorizations for a service, given a Subject, Action and Resource set (`PDPClient`)

It is meant to be a lightweight client library that can be used in other projects, such as a service or other client.

Some things that will be added soon in the future:

  - Caching authorization decisions from PDP
  - Support for list a users Roles assigned from IAM policies

# Usage

## Install

`pip install ibmcloud_iam`

## Getting tokens with TokenManager

```python
import os

from ibmcloud_api.token import TokenManager

tm = TokenManager(api_key=os.environ["IBMCLOUD_API_KEY"])

# whenever you need a token, just use 'tm.get_token()'
# get_token() will return a cached token if the token is not expired,
# or if expired or otherwise invalid, retrieve a new token for you

# gets a new token
print(tm.get_token())

# will return the same token as above, because of caching
print(tm.get_token())
```

## Parsing and Validating Tokens

```python
import os

from ibmcloud_api.token import TokenManager

tm = TokenManager(api_key=os.environ["IBMCLOUD_API_KEY"])

# validate_token will check the signature and parse and return the token claims
claims = ibmcloud_api.validate_token(tm.get_token())

print(claims)
```

## PDP Authorizations

Please see [example.py](example.py) for an example on how to use the `PDPClient`

# Contributing

Feedback is appreciated in the form of bug reports, enhancement suggestions, testing, or pull requests/patches.

Pull requests and patches will be subject to review and will have to meet the standards of the project to be merged. We are willing to help with fixing issues and polishing if you are willing to be patient and understanding.

For bug reports, feature requests, or other support, please open a Github Issue in this repo.

If you are an IBMer and have access to the IBM Slack group, feel free to direct message me with questions at `@mrodden`.
