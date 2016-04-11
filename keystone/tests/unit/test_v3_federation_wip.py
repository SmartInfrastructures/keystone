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

from oslo_log import log

from keystone.contrib.federation import controllers as federation_controllers

from keystone.tests.unit.test_v3_federation import FederatedSetupMixin
from keystone.tests.unit.test_v3_federation import FederationTests

from keystone.tests.unit import simplefederation_fixtures  # NOQA
from keystone.tests.unit import utils


LOG = log.getLogger(__name__)


class FederatedSetupMixinWIP(FederatedSetupMixin):

    # TODO(dancn): factorize what we need and move to separate file
    def _issue_unscoped_simplefederated_token(
            self,
            idp=None,
            assertion='EMPLOYEE_ASSERTION',
            environment=None):
        api = federation_controllers.Auth()
        context = {'environment': environment or {}}
        self._inject_assertion(context, assertion)
        if idp is None:
            idp = self.IDP
        r = api.federated_authentication(context, idp, self.PROTOCOL)
        r.headers['X-Subject-Token'] = 'ffffffffffffffffffffffffffffffff'
        # import pdb; pdb.set_trace()
        LOG.info("dancn: %s", r)
        return r


class FederatedTokenTestsWIP(FederationTests, FederatedSetupMixin):

    # TODO(dancn): factorize what we need and move to separate file
    @utils.wip('Simple Federation')
    def test_validate_simplefederated_unscoped_token(self):
        # 1. Get unscoped token from remote idp
        resp = self._issue_unscoped_simplefederated_token()
        LOG.debug('dancn 1: %s', resp)
        # import pdb; pdb.set_trace()
        unscoped_token_id = resp.headers.get('X-Subject-Token')
        headers = {'X-Subject-Token': unscoped_token_id}
        # 2. validate the unscoped token
        resp = self.get('/auth/tokens', headers=headers)
        token_data = resp.result
        self.assertEqual(self.v2_token_data['access']['user']['id'],
                         token_data['token']['user']['id'])
