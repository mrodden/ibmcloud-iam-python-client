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

import json
import os

from ibmcloud_iam import pdp as pdpapi
from ibmcloud_iam.token import TokenManager


def main():
    # production IAM endpoints
    endpoint = "https://iam.cloud.ibm.com"

    # this gets a user token for our example to be complete,
    # normally 'user_token' is sent by a client to your service
    # inside the client requests (HTTP Authorization Header)
    tm = TokenManager(api_key, iam_endpoint=endpoint)
    api_key = os.environ.get("IBMCLOUD_API_KEY")
    user_token = tm.get_token()

    # validate the user token, it also returns the validated claims
    # as a Dict if you need them
    token_claims = ibmcloud_iam.token.validate_token(user_token, endpoint)

    # this is your service ID API key, which was created when
    # registering/onboarding a new service to IBM Cloud
    service_id_key = os.environ.get("SERVICE_ID_KEY")

    # build our PDP client using the service ID key and point it at the
    # correct IAM endpoints
    pdp = pdpapi.PDPClient(service_id_key, iam_endpoint=endpoint)

    # build subject attributes directly from a user token,
    # this also validates the token again behind the scenes
    sub = pdp.subject_as_attributes(user_token)

    # there are two options for building the resource objects
    # using CRNs is easier, but attributes allow for more advanced ACLs

    # build resource using CRN
    resource = {
        "crn": "crn:v1:bluemix:public:books:us-south:a/1111222233334444:9e386139-0000-000-8101-103771fa7793::",
    }

    # build resource using attributes
    resource = {
        "attributes": {
            "serviceName": "books",
            "accountId": "1111222233334444",
            "ctype": "public",
            "serviceInstance": "9e386139-0000-000-8101-103771fa7793",
        }
    }

    # service action to be authorized
    action = "books.dashboard.view"

    # do the authorization check / call to PDP
    resp = pdp.is_authorized(sub, action, resource)

    # print the full body response from PDP
    # the "permitted" field on the response is a boolean indicating
    # if the request is authorized or not
    print(json.dumps(resp), indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
