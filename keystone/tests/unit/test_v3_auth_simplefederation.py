# Copyright 2012 OpenStack Foundation
#
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

import json
import mock  # TODO(dancn): get rid of mock
import requests_mock

from oslo_config import cfg

from six.moves.urllib import request as urlrequest

from keystoneclient.common import cms

from keystone.tests import unit as tests

from keystone.tests.unit import test_v3
from keystone.tests.unit.test_v3_auth import TokenAPITests

from keystone.tests.unit.simplefederation_fixtures import srv_token_data_adm
from keystone.tests.unit.simplefederation_fixtures import srv_token_headers_adm
from keystone.tests.unit.simplefederation_fixtures import token_invalid_id
from keystone.tests.unit.simplefederation_fixtures import token_valid_id


CONF = cfg.CONF


class TestUUIDTokenAPIsSP(test_v3.RestfulTestCase, TokenAPITests):

    def config_overrides(self):
        # We use the same config of TestUUIDTokenAPIs
        super(TestUUIDTokenAPIsSP, self).config_overrides()
        self.config_fixture.config(
            group='token',
            provider='keystone.token.providers.uuid.Provider')

    def config_files(self):
        config_files = super(TestUUIDTokenAPIsSP, self).config_files()
        config_files.append(tests.dirs.tests_conf(
            'test_simplefederation.conf'))
        return config_files

    def fakeurlopen(url, post_data):
        from keystone.tests.unit.simplefederation_fixtures import token_data
        if post_data['X-Subject-Token'] == token_valid_id:
            return token_data

    def setUp(self):
        super(TestUUIDTokenAPIsSP, self).setUp()
        self.doSetUp()

    def test_v3_token_id(self):
        auth_data = self.build_authentication_request(
            user_id=self.user['id'],
            password=self.user['password'])
        resp = self.v3_authenticate_token(auth_data)
        token_data = resp.result
        token_id = resp.headers.get('X-Subject-Token')
        self.assertIn('expires_at', token_data['token'])
        self.assertFalse(cms.is_asn1_token(token_id))

    # Those are a proxy to allow the direct call for debugging by
    # using stacktest.  Since this is a subclass and a direct call
    # will result in the following error:
    #
    # TypeError: unbound method proxy_test_check_token() must be
    # called with TokenAPITests instance as first argument (got
    # nothing instead)

    def proxy_test_check_token(self):
        self.test_check_token()

    def proxy_test_validate_token(self):
        self.test_validate_token()

    # Now the simplefederation tests

    def test_simplefederation_check_valid_token(self):
        """Test check simplefederation valid token on second idp"""
        with requests_mock.Mocker() as m:
            idp1 = CONF.simplefederation.idp[1]
            m.get(idp1 + '/v3/auth/tokens',
                  headers=srv_token_headers_adm,
                  text=json.dumps(srv_token_data_adm),
                  status_code=200)
            # TODO(dancn): mock also the admin request...
            headers = {'X-Subject-Token': token_valid_id}
            self.head('/auth/tokens', headers=headers, expected_status=200)

    def test_simplefederation_check_invalid_token(self):
        """Test check simplefederation invalid token"""
        headers = {'X-Subject-Token': token_invalid_id}
        self.head('/auth/tokens', headers=headers, expected_status=404)

    def test_simplefederation_validate_valid_token(self):
        """Test validate simplefederation valid token on second idp"""
        with requests_mock.Mocker() as m:
            idp1 = CONF.simplefederation.idp[1]
            m.get(idp1 + '/v3/auth/tokens',
                  headers=srv_token_headers_adm,
                  text=json.dumps(srv_token_data_adm),
                  status_code=200)
            # TODO(dancn): mock also the admin request...
            headers = {'X-Subject-Token': token_valid_id}
            self.get('/auth/tokens', headers=headers, expected_status=200)

    def test_simplefederation_validate_invalid_token(self):
        """Test validate simplefederation invalid token"""
        # TODO(dancn): get rid of mock
        with mock.patch.object(urlrequest, 'urlopen', self.fakeurlopen):
            headers = {'X-Subject-Token': token_invalid_id}
            self.get('/auth/tokens', headers=headers, expected_status=404)
