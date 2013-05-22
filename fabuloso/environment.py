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


class RemoteEnvironment(dict):
    """Maintains information about remote connection.

    Stores all the data needed to set a remote connection.
    """
    def __init__(self, env={}):
        """ Initialize gist object variables. """

        super(RemoteEnvironment, self).__init__(env)

    @property
    def username(self):
        return self['username']

    @username.setter
    def username(self, username):
        self['username'] = username

    @property
    def host(self):
        return self['host']

    @host.setter
    def host(self, host):
        self['host'] = host

    @property
    def ssh_key_file(self):
        return self['ssh_key_file']

    @ssh_key_file.setter
    def ssh_key_file(self, ssh_key_file):
        self['ssh_key_file'] = ssh_key_file

    @property
    def port(self):
        return self['port']

    @port.setter
    def port(self, port):
        self['port'] = port
