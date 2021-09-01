# Copyright 2021 Mathew Odden
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import time
import unittest

from ibmcloud_iam import token


class TokenTestCase(unittest.TestCase):
    @unittest.skipIf(not os.environ.get("IBMCLOUD_API_KEY"), "IBMCLOUD_API_KEY not set")
    def test_token(self):
        apikey = os.environ.get("IBMCLOUD_API_KEY")
        if not apikey:
            raise ValueError("'IBMCLOUD_API_KEY' not set.")

        tm = token.TokenManager(api_key=apikey)
        tok = tm.get_token()

        claims = token.validate_token(tok)
        self.assertTrue(claims)

    def test_validate_iss(self):
        claims = {}
        self.assertRaises(AssertionError, token._validate_iss, claims)

        claims = {"iss": "http://notiam.example.org"}
        self.assertRaises(AssertionError, token._validate_iss, claims)

        claims = {"iss": "https://iam.cloud.ibm.com"}
        token._validate_iss(claims)

    def test_validate_iat(self):
        claims = {}
        self.assertRaises(AssertionError, token._validate_iat, claims)

        claims = {"iat": "not-a-int"}
        self.assertRaises(AssertionError, token._validate_iat, claims)

        claims = {"iat": time.time() + 1000}
        self.assertRaises(AssertionError, token._validate_iat, claims)

        claims = {"iat": time.time()}
        token._validate_iat(claims)
