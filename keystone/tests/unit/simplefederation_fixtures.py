# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Fixtures and fake responses for Simple Federation Mapping."""

token_valid_id = 'ffffffffffffffffffffffffffffffffffffffff'

token_invalid_id = 'fffffffffffffffffffffffffffffffffffffff0'

srv_token_headers_adm = {
    'X-Subject-Token': token_valid_id,
    'Vary': 'X-Auth-Token',
    'Content-Type': 'application/json',
    'x-openstack-request-id': 'req-7c5f4a0d-3590-459a-9f54-6a0b11b90060'
}

srv_token_data_adm = {
    "token": {
        "audit_ids": [
            "Sn5dabZEQVqYX71fA6lGrg"
        ],
        "expires_at": "2016-04-04T20:00:37.895471Z",
        "extras": {},
        "issued_at": "2016-04-04T19:00:37.895493Z",
        "methods": [
            "password"
        ],
        "user": {
            "domain": {
                "id": "default",
                "name": "Default"
            },
            "id": "e873b9eeda36433a81c3da74b605ea05",
            "name": "admin"
        }
    }
}
