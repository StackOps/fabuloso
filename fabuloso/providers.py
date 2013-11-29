#!/usr/bin/python
#   Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from fabric.context_managers import settings
from exceptions import FabulosoError
import traceback


class Provider(object):
    """Base provider class"""

    def set_environment(self, env):
        self.env = env

    def execute_method(self, method, **kwargs):
        raise NotImplementedError("Provider base class does not implement"
                                  " this method")


class FabricProvider(Provider):
    """Fabric Provider that wraps any call setting environment variables"""

    def __init__(self):
        super(FabricProvider, self).__init__()

    def execute_method(self, method, **kwargs):
        try:
            with settings(host_string=self.env['host'],
                          key_filename=self.env['ssh_key_file'],
                          port=self.env['port'], user=self.env['username'],
                          keepalive=15, disable_known_hosts=True):
                return method(**kwargs)
        except SystemExit:
            traceback.print_exc()
            raise FabulosoError


class DummyProvider(Provider):
    """Dummy Provider.

    This provider does not actually do nothing and it is just developed for
    test purposes.
    """

    def __init__(self, env):
        super(DummyProvider, self).__init__()

    def execute_method(self, method, **kwargs):
        pass
