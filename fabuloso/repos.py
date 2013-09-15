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
from sh import git

import ConfigParser
import os
import shutil

class Repositorer(object):

    def __init__(self, catalog_dir):
        self._catalog_dir = catalog_dir
        self._config = ConfigParser.ConfigParser()
        self._index = os.path.join(catalog_dir, 'repos.cfg')
        if not os.path.exists(self._index):
            # create empty file
            open(self._index, 'a').close()
        
    def add_repo(self, name, url, auth_tuple=None):
        self._config.read(self._index)
        if not self._config.has_section(name):
            self._clone_repo(name, url, auth_tuple)
            self._config.add_section(name)
            self._config.set(name, 'type', 'git')
            self._config.set(name, 'url', url)
            with open(self._index, 'w') as index_file:
                self._config.write(index_file)
        else:
            raise Exception("Repository '%s' already exists" % (name))

    def del_repo(self, name):
        self._config.read(self._index)
        if not self._config.has_section(name):
            raise Exception("Repository '%s' does not exist" % (name))
        else:
            self._config.remove_section(name)
            with open(self._index, 'w') as index_file:
                self._config.write(index_file)
            path = os.path.join(self._catalog_dir, name)
            shutil.rmtree(path)


    def _clone_repo(self, name, url, auth_tuple):
        path = os.path.join(self._catalog_dir, name)
        if not auth_tuple:
            git.clone(url, path)
        else:
            # TODO: implement for private repos
            git.clone(url, path)
