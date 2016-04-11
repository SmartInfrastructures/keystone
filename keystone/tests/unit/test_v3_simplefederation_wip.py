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


import os

from oslo_config import cfg
from oslo_log import log

from keystone.tests.unit import test_v3
from keystone.tests.unit.utils import wip


CONF = cfg.CONF
LOG = log.getLogger(__name__)
ROOTDIR = os.path.dirname(os.path.abspath(__file__))


class FakeIDP(object):

    def __init__(self):
        pass

    def issue_unscoped_token(self):
        token = False
        return token


class FakeSP(object):

    def __init__(self):
        pass

    def validate_unscoped_token(self, token):
        return token


class SimpleFederationTests(test_v3.RestfulTestCase):

    @wip('Simple Federation unscoped token')
    def test_unscoped_topen(self):
        """Test simple workflow for issuing and cheking granting unscoped
           tokens.

        * Request an unscoped token from a keystone as IDP (Identity
          Provider)

        * Validate the token using a keystone as SP (Service Provider)

        """

        idp = FakeIDP()
        sp = FakeSP()

        token_resp = idp.issue_unscoped_token()
        valid = sp.validate_unscoped_token(token_resp)
        self.assertTrue(valid)
