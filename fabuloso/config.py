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
import ConfigParser
import os


class ConfigureEditor(object):
    """Object that handles the read and write actions
       over the configuration files"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ This class is a singleton. """
        if not cls._instance:
            cls._instance = super(ConfigureEditor, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._base_dir = os.path.expanduser('~/.config/fabuloso/')
        self._config = ConfigParser.ConfigParser()

        if not os.path.exists(self._base_dir):
            os.makedirs(self_base_dir)

        self._keys_dir = os.path.join(self._base_dir, 'keys')
        if not os.path.exists(self._keys_dir):
            os.makedirs(self._keys_dir)
        self._keys_cfg = os.path.join(self._base_dir, 'keys.cfg')
        if not os.path.exists(self._keys_cfg):
            open(self._keys_cfg, 'a').close()

        self._repos_dir = os.path.join(self._base_dir, 'repos')
        if not os.path.exists(self._repos_dir):
            os.makedirs(self._repos_dir)
        self._repos_cfg = os.path.join(self._base_dir, 'repos.cfg')
        if not os.path.exists(self._repos_cfg):
            # create empty file
            open(self._repos_cfg, 'a').close()

        self._environments_cfg = os.path.join(self._base_dir, 'environments.cfg')
        if not os.path.exists(self._environments_cfg):
            open(self._environments_cfg, 'a').close()

    def get_catalog_dir(self):
        return self._repos_dir

    def add_repo(self, name, url):
        self._config.read(self._repos_cfg)
        if not self._config.has_section(name):
            self._config.add_section(name)
            self._config.set(name, 'type', 'git')
            self._config.set(name, 'url', url)
            with open(self._repos_cfg, 'w') as index_file:
                self._config.write(index_file)
        else:
            raise Exception("Repository '%s' already exists" % (name))

    def del_repo(self, name):
        self._config.read(self._repos_cfg)
        if not self._config.has_section(name):
            raise Exception("Repository '%s' does not exist" % (name))
        else:
            self._config.remove_section(name)
            with open(self._repos_cfg, 'w') as index_file:
                self._config.write(index_file)

    def get_key(self, name):
        self._config.read(self._keys_cfg)
        if not self._config.has_section(name):
            raise Exception("Key '%s' does not exist" % (name))
        else:
            file_path = os.path.join(os.path.abspath(os.path.dirname(self._keys_cfg)), 'keys')
            return name, os.path.join(file_path, self._config.get(name, 'file'))

    def list_keys(self):
        self._config.read(self._keys_cfg)
        file_path = os.path.join(os.path.abspath(os.path.dirname(self._keys_cfg)), 'keys')
        return [(name, os.path.join(file_path, self._config.get(name, 'file'))) for name in self._config.sections()]

    def add_env(self, env):
        self._config.read(self._environments_cfg)
        name = env['name']
        if self._config.has_section(name):
            raise Exception("Environment '%s' already exist" % name)
        else:
            self._config.add_section(name)
            for key in env.keys():
                if key is not 'name':
                    self._config.set(name, key, env[key])

            with open(self._environments_cfg, 'w') as index_file:
                self._config.write(index_file)

    def del_env(self, name):
        self._config.read(self._environments_cfg)
        if not self._config.has_section(name):
            raise Exception("Environment '%s' does not exist" % (name))
        else:
            self._config.remove_section(name)
            with open(self._environments_cfg, 'w') as index_file:
                self._config.write(index_file)

    def get_env(self, name):
        self._config.read(self._environments_cfg)
        if not self._config.has_section(name):
            raise Exception("Environment '%s' does not exist" % (name))
        else:
            env = {'name': name}
            for item in self._config.items(name):
                env[item[0]] = item[1]
            return env

    def list_envs(self):
        self._config.read(self._environments_cfg)
        list_environments = []
        for section in self._config.sections():
            env = { 'name': section }
            for item in self._config.items(section):
                env[item[0]] = item[1]
            list_environments.append(env)
        return list_environments
