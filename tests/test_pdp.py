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

import base64
import json
import os
import unittest

from ibmcloud_iam import pdp
from ibmcloud_iam import token


class PDPTestCase(unittest.TestCase):
    @unittest.skipIf(not os.environ.get("IBMCLOUD_API_KEY"), "IBMCLOUD_API_KEY not set")
    def test_subject_as_token_body(self):
        apikey = os.environ.get("IBMCLOUD_API_KEY")
        tm = token.TokenManager(api_key=apikey)
        tok = tm.get_token()

        claims = token.validate_token(tok)
        pdpc = pdp.PDPClient(apikey)

        subject = pdpc.subject_as_token_body(tok)
        self.assertIn("accessTokenBody", subject)

        body = subject["accessTokenBody"]
        padding = "=" * (len(body) % 4)

        decoded = base64.urlsafe_b64decode(body + padding)
        body_claims = json.loads(decoded.decode("utf8"))
        self.assertEqual(claims, body_claims)

    @unittest.skipIf(not os.environ.get("IBMCLOUD_API_KEY"), "IBMCLOUD_API_KEY not set")
    def test_subject_as_attributes(self):
        apikey = os.environ.get("IBMCLOUD_API_KEY")
        tm = token.TokenManager(api_key=apikey)
        tok = tm.get_token()

        claims = token.validate_token(tok)
        pdpc = pdp.PDPClient(apikey)

        subject = pdpc.subject_as_attributes(tok)
        self.assertIn("attributes", subject)
        attrs = subject["attributes"]
        self.assertIn("id", attrs)
        self.assertIn("scope", attrs)

        self.assertEqual(claims["iam_id"], attrs["id"])
        self.assertEqual(claims["scope"], attrs["scope"])
