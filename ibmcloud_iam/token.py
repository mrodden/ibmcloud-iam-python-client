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

import time
import types
from typing import Dict, Optional

import jwt
from redstone.auth import TokenManager  # noqa: F401


DEFAULT_IAM_KEY_URL = "https://iam.cloud.ibm.com/identity/keys"
EXPIRE_LEEWAY = 5  # seconds


def validate_token(token: str, iam_key_url: Optional[str] = None) -> Dict:
    if iam_key_url is None:
        iam_key_url = DEFAULT_IAM_KEY_URL

    kc = jwt.PyJWKClient(iam_key_url)

    # need to modify the keys data from IAM
    # to include a 'use': 'sig' so JWK sees them as signing keys
    def new_get_set(self):
        data = self.fetch_data()
        for key in data["keys"]:
            key["use"] = "sig"
        return jwt.PyJWKSet.from_dict(data)

    kc.get_jwk_set = types.MethodType(new_get_set, kc)

    public_key = kc.get_signing_key_from_jwt(token)

    claims = jwt.decode(
        token,
        public_key.key,
        algorithms=["RS256"],
        leeway=EXPIRE_LEEWAY,
        options={"verify_signature": True},
    )
    _validate_iss(claims)
    _validate_iat(claims)
    return claims


def _validate_iss(claims: Dict):
    if "iss" in claims and claims["iss"].startswith("https://iam"):
        return

    raise AssertionError("Invalid or missing 'iss' header in token.")


def _validate_iat(claims: Dict):
    if "iat" not in claims:
        raise AssertionError("Invalid or missing 'iat' header in token.")

    try:
        iat = int(claims["iat"])
    except ValueError:
        raise AssertionError("Invalid or missing 'iat' header in token.")

    if iat > (time.time() + EXPIRE_LEEWAY):
        raise AssertionError("'iat' too far in the future.")
