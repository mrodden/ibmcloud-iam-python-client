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

import requests

from ibmcloud_iam import token as tapi

"""
PDP stands for the Policy Determination Point and
is a service that other services use to check authorization
of actions on resources in IBM Cloud.
"""

DEFAULT_IAM_ENDPOINT = "https://iam.cloud.ibm.com"


class PDPClient(object):
    def __init__(self, api_key: str, iam_endpoint=None):
        if not api_key:
            raise ValueError("Invalid or empty 'api_key'")

        if iam_endpoint is not None:
            if not iam_endpoint.startswith("https://"):
                raise ValueError("Invalid or empty 'iam_endpoint'")

            self._endpoint = iam_endpoint
        else:
            self._endpoint = DEFAULT_IAM_ENDPOINT

        self._tm = tapi.TokenManager(api_key, self._endpoint)

        self._session = requests.Session()

        self._advanced_obligations = False

        def bearer_auth(req):
            req.headers["Authorization"] = "Bearer %s" % self._tm.get_token()
            return req

        self._session.auth = bearer_auth

    def _is_authorized(self, subject, action, resource):
        req_data = {
            "subject": subject,
            "resource": resource,
            "action": action,
        }

        headers = {}

        # NOTE(mrodden): this enables some advanced caching response
        # mode in the response objects for the /v2/authz API,
        # we don't use it in the client here, since I could not
        # understand how it is supposed to be useful
        if self._advanced_obligations:
            headers["X-Accept-Advanced-Obligation"] = "true"

        resp = self._session.post(
            url="%s/v2/authz" % self._endpoint,
            json=[req_data],
            headers=headers,
        )

        return resp

    def is_authorized(self, subject, action, resource):
        """
        Retrieve a policy decision for a single Subject, Action, Resource tuple.

        Uses the `/v2/authz` endpoint.
        https://test.cloud.ibm.com/apidocs/iam-policy-decision-point-api#authz
        """
        resp = self._is_authorized(subject, action, resource)
        resp.raise_for_status()
        return resp.json()

    def subject_as_attributes(self, token: str):
        claims = tapi.validate_token(token, self._endpoint + "/identity/keys")

        if "iam_id" not in claims:
            raise ValueError("Token missing 'iam_id' claim.")

        if "scope" not in claims:
            raise ValueError("Token missing 'scope' claim.")

        return {"attributes": {"id": claims["iam_id"], "scope": claims["scope"]}}

    def subject_as_token_body(self, token: str):
        # this method is simpler but doesn't match up with the responses that we are caching
        _ = tapi.validate_token(token, self._endpoint + "/identity/keys")
        _, body, _ = token.split(".")
        return {"accessTokenBody": body}
