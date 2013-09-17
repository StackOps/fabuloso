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

import exceptions

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
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._repos_cfg)
        if not config_parser.has_section(name):
            config_parser.add_section(name)
            config_parser.set(name, 'type', 'git')
            config_parser.set(name, 'url', url)
            with open(self._repos_cfg, 'w') as index_file:
                config_parser.write(index_file)
        else:
            excp_data = { 'repo_name': name }
            raise exceptions.RepositoryAlreadyExists(**excp_data)

    def del_repo(self, name):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._repos_cfg)
        if not config_parser.has_section(name):
            excp_data = { 'repo_name': name }
            raise exceptions.RepositoryNotFound(**excp_data)
        else:
            config_parser.remove_section(name)
            with open(self._repos_cfg, 'w') as index_file:
                config_parser.write(index_file)

    def get_key(self, name):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._keys_cfg)
        if not config_parser.has_section(name):
            excp_data = { 'key_name': name }
            raise exceptions.KeyNotFound(**excp_data)
        else:
            file_path = os.path.join(os.path.abspath(os.path.dirname(self._keys_cfg)), 'keys')
            return name, os.path.join(file_path, config_parser.get(name, 'file'))

    def list_keys(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._keys_cfg)
        file_path = os.path.join(os.path.abspath(os.path.dirname(self._keys_cfg)), 'keys')
        return [(name, os.path.join(file_path, config_parser.get(name, 'file'))) for name in config_parser.sections()]

    def add_env(self, env):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._environments_cfg)
        name = env['name']
        if config_parser.has_section(name):
            excp_data = { 'env_name': name }
            raise exceptions.EnvironmentAlreadyExists(**excp_data)
        else:
            config_parser.add_section(name)
            for key in env.keys():
                if key is not 'name':
                    config_parser.set(name, key, env[key])

            with open(self._environments_cfg, 'w') as index_file:
                config_parser.write(index_file)

    def del_env(self, name):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._environments_cfg)
        if not config_parser.has_section(name):
            excp_data = {'env_name': name}
            raise exceptions.EnvironmentNotFound(**excp_data)
        else:
            config_parser.remove_section(name)
            with open(self._environments_cfg, 'w') as index_file:
                config_parser.write(index_file)

    def get_env(self, name):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._environments_cfg)
        if not config_parser.has_section(name):
            excp_data = {'env_name': name}
            raise exceptions.EnvironmentNotFound(**excp_data)
        else:
            env = {'name': name}
            for item in config_parser.items(name):
                env[item[0]] = item[1]
            return env

    def get_repo(self, name):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._repos_cfg)
        if not config_parser.has_section(name):
            excp_data = {'repo_name': name}
            raise exceptions.RepositoryNotFound(**excp_data)
        else:
            repo = {'name': name}
            for item in config_parser.items(name):
                repo[item[0]] = item[1]
            return repo

    def list_envs(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._environments_cfg)
        list_environments = []
        for section in config_parser.sections():
            env = { 'name': section }
            for item in config_parser.items(section):
                env[item[0]] = item[1]
            list_environments.append(env)
        return list_environments


    def list_repos(self):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(self._repos_cfg)
        list_environments = []
        for section in config_parser.sections():
            env = { 'name': section }
            for item in config_parser.items(section):
                env[item[0]] = item[1]
            list_environments.append(env)
        return list_environments
