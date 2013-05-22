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
from fabric.context_managers import settings, hide


class FabricProvider(object):
    """Fabric Provider that wraps any call setting environment variables"""

    def __init__(self, env):
        """Receives a L{environment.RemoteEnvironment} object."""
        self.env = env

    def execute_method(self, func):
        def environment_func(**kwargs):
            with settings(hide('stdout', 'status', 'running'),
                          host_string=self.env['host'],
                          key_filename=self.env['ssh_key_file'],
                          port=self.env['port'], user=self.env['username']):
                return func(**kwargs)

        return environment_func
