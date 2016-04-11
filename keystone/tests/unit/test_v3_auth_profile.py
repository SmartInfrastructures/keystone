# Copyright 2016 OpenStack Foundation
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

# TODO(dancn) replace with logging
from __future__ import print_function

import json

from oslo_config import cfg

from keystone.tests.unit import test_v3
from keystone.tests.unit.test_v3_auth import TokenAPITests
from keystone.tests.unit.utils import wip


CONF = cfg.CONF


class TestUUIDTokenAPIsProfile(test_v3.RestfulTestCase, TokenAPITests):
    """This is only to try to understand the api"""
    def config_overrides(self):
        super(TestUUIDTokenAPIsProfile, self).config_overrides()
        self.config_fixture.config(
            group='token',
            provider='keystone.token.providers.uuid.Provider')

    def setUp(self):
        super(TestUUIDTokenAPIsProfile, self).setUp()
        self.doSetUp()

    @wip("TODO")
    def test_profile1_v3_token_id(self):
        import hotshot
        import hotshot.stats

        prof = hotshot.Profile("/tmp/stones.prof")
        benchtime, stones = prof.runcall(self.test_v3_token_id)
        prof.close()
        stats = hotshot.stats.load("stones.prof")
        stats.strip_dirs()
        stats.sort_stats('time', 'calls')
        stats.print_stats(20)

    @wip("TODO")
    def test_profile2_v3_token_id(self):

        from osprofiler import notifier

        def send_info_to_file_collector(info, context=None):
            with open("traces", "a") as f:
                f.write(json.dumps(info))

        notifier.set(send_info_to_file_collector)

        from osprofiler import profiler

        profiler.init('random')
        profiler.start("point_name", {"any_key": "with_any_value"})

        self.test_v3_token_id()

        profiler.stop({"any_info_about_point": "in_this_dict"})

    @wip("TODO")
    def test_profile3_v3_token_id(self):
        import cProfile
        import pstats
        self.pr = cProfile.Profile()
        self.pr.enable()
        self.test_v3_token_id()
        self.pr.disable()
        p = pstats.Stats(self.pr)
        p.strip_dirs()
        p.sort_stats('cumtime')
        p.sort_stats('time')
        p.print_stats()

    @wip("TODO")
    def test_profile4_v3_token_id(self):
        from pycallgraph.output import GraphvizOutput
        from pycallgraph import PyCallGraph

        with PyCallGraph(output=GraphvizOutput()):
            self.test_v3_token_id()

    @wip("TODO")
    def test_profile5_v3_token_id(self):
        from pycallgraph import Config
        from pycallgraph import PyCallGraph

        from pycallgraph.output import GraphvizOutput
        # from pycallgraph import GlobbingFilter

        config = Config(max_depth=8)
        # config.trace_filter = GlobbingFilter(include=[
        #     'keystone.*',
        # ])

        graphviz = GraphvizOutput(output_file='/vagrant/profile.png')

        with PyCallGraph(output=graphviz, config=config):
            self.test_v3_token_id()

    @wip("TODO")
    def test_profile6_v3_token_id(self):
        import sys
        import trace
        tracer = trace.Trace(
            ignoredirs=[sys.prefix, sys.exec_prefix],
            count=False,
            trace=False,
            countcallers=True)
        tracer.runfunc(self.test_v3_token_id)

        results = tracer.results()
        # TODO(dancn): how to print like with the command line
        # $ python -m trace --listfuncs --trackcalls trace_example/main.py
        results.write_results(
            show_missing=True,
            summary=True,
            coverdir='coverdir3'
        )

    @wip("TODO")
    def test_profile7_v3_token_id(self):
        # http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html
        import linecache
        import sys

        # This will take looong time to finish, so end brutally
        sys.exit()

        def traceit(frame, event, arg):
            if event == "line":
                lineno = frame.f_lineno
                filename = frame.f_globals.get('__file__', 'NO_FILE')
                if (
                        filename.endswith(".pyc") or
                        filename.endswith(".pyo")
                ):
                    filename = filename[:-1]
                name = frame.f_globals.get("__name__", 'NO_NAME')
                line = linecache.getline(filename, lineno) if filename != 'NO_FILE' else "NO_LINE"  # noqa
                print("{}:{}: {}".format(name, lineno, line.rstrip()))
            return traceit
        sys.settrace(traceit)
        self.test_v3_token_id()
        sys.settrace()

    def test_profile8_v3_token_id(self):
        # http://eli.thegreenplace.net/2012/08/22/easy-tracing-of-nested-function-calls-in-python
        pass

    def test_profile9_v3_token_id(self):
        # pyreverse -o png -p keystone /home/praveens/git/keystone
        pass
