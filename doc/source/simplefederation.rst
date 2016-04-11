..
    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy
    of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations
    under the License.

.. _simplefederation-label:

=================
Simple Federation
=================

Original plan
=============

- :download:`See the original plan in odt <simplefederation/FinalSpecCopyKeyrock2KeystoneFederation.odt>`
- :download:`See the original plan in pdf <simplefederation/FinalSpecCopyKeyrock2KeystoneFederation.pdf>`


Configuration
=============

Add a section to ``keystone.conf`` as in the example with remote idp
and the remote idp service user and password::

    [simplefederation]
    idp=http://user1:password1@idp1.provider1.test:35357
    idp=http://user2:password2@idp2.provider2.test:35357


Ongoing Work
============

- The original plan is, at best a simplified view of reality


Developer doc
=============

Upstream documentation:

- <http://developer.openstack.org/api-ref-identity-v3.html#authenticatePasswordUnscoped>
- <http://developer.openstack.org/api-ref-identity-v3.html#validateToken>


Build
+++++

Use something like::

    . .venv/bin/activate
    pip install wheel
    python setup.py sdist
    python setup.py bdist
    python setup.py bdist_wheel


Testing
+++++++

Check the style with::

    tox -e pep8

Generate the example conf with::

    tox -e sample_config

Generate the doc with::

    tox -e docs

See also: <https://wiki.openstack.org/wiki/Testr>

Some useful notes::

    # Remove stale .pyc, after branch switch

    find . -name "*.pyc" -delete

    # Run some test
    . .venv/bin/activate

    ostestr
    testr

    tox -e py27 -- 'TestUUIDTokenAPIsSP'
    tox -e py27 -- 'TestUUIDTokenAPIs*'

    tox -e pep8 -- 'keystone/tests/unit/test_v3_simplefederation.py'
    tox -e pep8 -- 'keystone/tests/unit/test_v3_auth.py'
    tox -e py27 -- 'keystone/tests/unit/test_v3_simplefederation.py;
    tox -e py27 -- 'keystone.tests.unit.test_v3_auth.TestUUIDTokenAPIs.test_simplefederation'
    tox -e py27 -- 'SimpleFederationTests'
    tox -e py27 -- 'TestUUIDTokenAPIs.test_v3_token_id'
    tox -e py27 -- 'TestUUIDTokenAPIs.test_validate_token$'
    tox -e py27 -- 'TestUUIDTokenAPIsProfile'
    tox -e py27 -- 'TestUUIDTokenAPIs.test_(v3_token_id|validate_token$)'
    tox -e py27 -- 'TestUUIDTokenAPIs.test_(v3_token_id|validate_token$)'


The subset UUID token test suite can be run with::

    OS_DEBUG=True \
    .tox/py27/bin/python -m subunit.run \
    keystone.tests.unit.test_v3_auth.TestUUIDTokenAPIs | \
    .tox/py27/bin/subunit-trace

Regressions on all the test suite can be tracked down with::

    . .venv/bin/activate
    COUNT=$((${COUNT:-0} + 1)); time annotate-output tox -e py27 | tee testrun-output-${COUNT}
    .tox/py27/bin/testr last --subunit | .tox/py27/bin/subunit-filter --no-success --no-skip | .tox/py27/bin/subunit-ls > testrun-failed-${COUNT}
    .tox/py27/bin/testr run --load-list=testrun-failed-${COUNT}

Regressions on ``TestUUIDTokenAPIsSP`` can be tracked down with::

    COUNT=$((${COUNT:-0} + 1)); time annotate-output tox -e py27 -- 'TestUUIDTokenAPIsSP' | tee testrun-output-${COUNT}
    .tox/py27/bin/testr last --subunit | .tox/py27/bin/subunit-filter --no-success --no-skip | .tox/py27/bin/subunit-ls > testrun-failed-${COUNT}
    cat testrun-failed-${COUNT}
    .tox/py27/bin/testr run --load-list=testrun-failed-${COUNT}


Profile does not seem to work::

    . .venv/bin/activate
    pip install nose
    time nosetests keystone.tests.unit.test_v3_auth:TestUUIDTokenAPIs.test_v3_token_id
    tox -e py27 -- TestUUIDTokenAPIs.test_v3_token_id
    tox -e debug -- TestUUIDTokenAPIs.test_v3_token_id
    time nosetests --with-profile keystone.tests.unit.test_v3_auth:TestUUIDTokenAPIs.test_v3_token_id


But will fail (and I hope that is not related to
<http://bugs.python.org/issue900092>::

    Traceback (most recent call last):
      File "/home/vagrant/.virtualenvs/kd/bin/nosetests", line 11, in <module>
        sys.exit(run_exit())
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/core.py", line 121, in __init__
        **extra_args)
      File "/usr/lib/python2.7/unittest/main.py", line 95, in __init__
        self.runTests()
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/core.py", line 207, in runTests
        result = self.testRunner.run(self.test)
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/core.py", line 66, in run
        result.printErrors()
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/result.py", line 110, in printErrors
        self.config.plugins.report(self.stream)
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/plugins/manager.py", line 99, in __call__
        return self.call(*arg, **kw)
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/plugins/manager.py", line 167, in simple
        result = meth(*arg, **kw)
      File "/home/vagrant/.virtualenvs/kd/local/lib/python2.7/site-packages/nose/plugins/prof.py", line 102, in report
        prof_stats = stats.load(self.pfile)
      File "/usr/lib/python2.7/hotshot/stats.py", line 15, in load
        return StatsLoader(filename).load()
      File "/usr/lib/python2.7/hotshot/stats.py", line 54, in load
        assert not self._stack
    AssertionError


See more at:

- <https://wiki.openstack.org/wiki/KeystonePerformance>
- <https://wiki.openstack.org/wiki/Testr#Debugging_.28pdb.29_Tests>


Notes
=====

An example request made by glance to keystone admin::

    GET /v3/auth/tokens HTTP/1.1
    Host: 192.168.50.101:35357
    # ### the token provided by the user to glance:
    X-Subject-Token: 3494845d9eca4d36833c068f7e03765d
    # ### the token of glance itself:
    X-Auth-Token: 62926efb503644358bab69ebdf7c30a9
    Accept-Encoding: gzip, deflate, compress
    Accept: application/json
    User-Agent: python-keystoneclient


Upstream work
=============

The upstream does not seems to have federation functional testing
right now!

- <http://lists.openstack.org/pipermail/openstack-dev/2016-April/091262.html>
- <https://review.openstack.org/#/q/project:openstack/keystone+message:federation+after:2015-11-01>
