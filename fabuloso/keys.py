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
import os

import ConfigParser

class KeyManager(object):
    """ Handles the ssh keys to connect remotely."""

    def __init__(self, keys_dir):
        self._keys_dir = keys_dir
        self._config = ConfigParser.ConfigParser()
        self._index = os.path.join(keys_dir, 'keys.cfg')
        self._cd = os.path.dirname(os.path.abspath(self._index))
        if not os.path.exists(self._index):
            # create empty file
            open(self._index, 'a').close()

    def get_keys(self):
        self._config.read(self._index)
        return self._config.sections()

    
    def get_key_file(self, key_name):
        self._config.read(self._index)
        if not self._config.has_section(key_name):
            raise Exception("Key '%s' does not exist" % key_name)
        return os.path.join(self._cd,
                            self._config.get(key_name, 'file'))

    def import_key(self, key_name, key_file):
        self._conf
