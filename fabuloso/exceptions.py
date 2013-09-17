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
class EnvironmentNotFound(Exception):

    message = "Environment '%(env_name)s' not found"

    def __init__(self, **kwargs):
        super(EnvironmentNotFound, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs


class EnvironmentAlreadyExists(Exception):

    message = "Environment '%(env_name)s' already exists. Choose another name"

    def __init__(self, **kwargs):
        super(EnvironmentAlreadyExists, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs


class RepositoryNotFound(Exception):

    message = "Repository '%(repo_name)s' not found"

    def __init__(self, **kwargs):
        super(RepositoryNotFound, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs


class RepositoryAlreadyExists(Exception):

    message = "Repository '%(repo_name)s' already exists. Choose another name"

    def __init__(self, **kwargs):
        super(RepositoryAlreadyExists, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs


class KeyNotFound(Exception):

    message = "Key '%(key_name)s' not found"

    def __init__(self, **kwargs):
        super(KeyNotFound, self).__init__(self.message % kwargs)
        self.msg = self.message % kwargs
