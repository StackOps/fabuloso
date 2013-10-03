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
import imp
import shutil
import UserDict

import yaml
from sh import git

from . import component, providers, utils, config


class Fabuloso(object):

    def __init__(self):
        self._config_editor = config.ConfigureEditor()

        """ Init with catalog dir"""
        self._load_catalog()

    def add_repository(self, repo_name, repo_url, auth_keys=None):
        self._config_editor.add_repo(repo_name, repo_url)
        self._clone_repo(repo_name, repo_url)
        self._load_catalog()

    def add_environment(self, name, username, host, port, key_name):
        self.get_key(key_name)

        env = {'name': name,
               'username': username,
               'host': host,
               'port': port,
               'key_name': key_name}
        self._config_editor.add_env(env)
        return Environment(env)

    def add_key(self, name, key_path, pub_path):
        key_file, pub_file = self.__store_keypair(name, key_path, pub_path)

        keypair = {
            'name': name,
            'key_file': key_file,
            'pub_file': pub_file
        }

        self._config_editor.add_key(keypair)

    def __store_keypair(self, name, key_path, pub_path):
        keys_path = os.path.join(os.path.dirname(
            self._config_editor._keys_cfg), 'keys')

        key_file = os.path.join(keys_path, name)
        pub_file = os.path.join(keys_path, name + '.pub')

        utils.copy(key_path, key_file)
        utils.copy(pub_path, pub_file)

        return key_file, pub_file

    def delete_key(self, name):
        keypair = self.get_key(name)

        os.remove(keypair.key_file)
        os.remove(keypair.pub_file)

        self._config_editor.del_key(name)

    def delete_environment(self, name):
        self._config_editor.del_env(name)

    def delete_repository(self, repo_name):
        self._config_editor.del_repo(repo_name)
        path = os.path.join(self._config_editor.get_catalog_dir(), repo_name)
        shutil.rmtree(path)
        self._load_catalog()

    def init_component(self, component_name, properties, environment):
        if not isinstance(environment, Environment):
            raise Exception("'environment' parameter must be an instance "
                            " of Environment class")
        comp = self._catalog[component_name]
        comp.set_properties(properties)
        environment.data['ssh_key_file'] = self.get_key(
            environment.data['key_name']).key_file

        comp.set_environment(environment)
        return comp

    def init_component_extended_data(self, component_name,
                                     ext_properties, environment):
        properties = {}
        map(properties.update, ext_properties.values())
        return self.init_component(component_name, properties, environment)

    def get_template(self, component_name):
        """ Retrieves the list of needed properties"""
        comp = self._catalog[component_name]
        props = {}
        for service, service_def in comp._services.items():
            description, methods = service_def
            for method in methods:
                params = comp._get_method_params(method)
                for param in params:
                    if not param in props:
                        props[param] = comp._get_param_default(param, method)
        return props

    def get_template_extended_data(self, component_name):
        """ Retrieves the list of needed properties"""
        comp = self._catalog[component_name]
        props = {}
        for service, service_def in comp._services.items():
            service_props = {}
            description, methods = service_def
            for method in methods:
                params = comp._get_method_params(method)
                for param in params:
                    if not param in service_props:
                        service_props[param] = comp._get_param_default(
                            param, method)

            props[service] = service_props
        return props

    def list_components(self, repo_name=None):
        """ Return the catalog in a string/json way."""

        if repo_name is None:
            return self._catalog.values()

        # Ensure the repo exists
        repo = self.get_repo(repo_name)

        return [comp for name, comp in self._catalog.items()
                if name.startswith('{}.'.format(repo['name']))]

    def get_repo(self, name):
        return Repository.import_repo(name)

    def list_keys(self):
        return [SshKey(**key) for key in self._config_editor.list_keys()]

    def get_key(self, name):
        return SshKey.import_key(name)

    def list_environments(self):
        envs = self._config_editor.list_envs()
        ret_data = []
        for env in envs:
            ret_data.append(Environment(env))
        return ret_data

    def list_repositories(self):
        repos = self._config_editor.list_repos()
        ret_data = []
        for repo in repos:
            ret_data.append(Repository(repo))
        return ret_data

    def _load_catalog(self):
        """Returns a dict that maps the component name with the module."""
        catalog_dir = self._config_editor.get_catalog_dir()
        self._catalog = {}
        repos = self._get_subdirectories(catalog_dir)
        for repo in repos:
            # Walk through all the catalog components
            repo_dir = os.path.join(catalog_dir, repo)
            for dirname, subdirnames, filenames in os.walk(repo_dir):
                for subdirname in subdirnames:
                    comp_dir = os.path.join(repo_dir, subdirname)
                    try:
                        comp = self._load_component(repo, comp_dir)
                        self._catalog[comp._name] = comp
                    except IOError:
                        # Skip the failing components
                        continue

    def _get_subdirectories(self, dir):
        return [name for name in os.listdir(dir)
                if os.path.isdir(os.path.join(dir, name))]

    def _load_component(self, repo, comp_dir):
        """ Based on the definition file, build the component.
        """
        definition_path = os.path.join(comp_dir, 'component.yml')
        with open(definition_path) as f:
            definition = yaml.load(f.read())

        # load the module that belongs to this component
        component_name = repo + '.' + definition['name']
        module_path = os.path.join(comp_dir, definition['file'])
        module = imp.load_source(definition['name'], module_path)

        # TODO: read also from the configuration file, now we have
        # only a provider, so we hard core it
        provider = providers.FabricProvider()

        comp_services = {}
        for service in definition['Services']:
            name = service['name']
            list_methods = []
            description = service['description']
            for method in service['methods']:
                list_methods.append(method)
            comp_services[name] = (description, list_methods)

        comp = component.Component(component_name, module, comp_services,
                                   provider)
        return comp

    def validate_credentials(self, user, password, tenant, endpoint,
                             admin_token):
        utils.validate_credentials(user, password, tenant, endpoint,
                                   admin_token)

    def validate_database(self, database_type, username, password, host, port,
                          schema, drop_schema=None, install_database=None):
        utils.validate_database(database_type, username, password, host, port,
                                schema, drop_schema, install_database)

    def send_rabbitMQ(self, service_type, host, port=None, user=None,
                      password=None, virtual_host=None):
        utils.send_rabbitMQ(service_type, host, port, user, password,
                            virtual_host)

    def _clone_repo(self, name, url, auth_tuple=None):
        path = os.path.join(self._config_editor.get_catalog_dir(), name)
        if not auth_tuple:
            git.clone(url, path)
        else:
            # TODO: implement for private repos
            git.clone(url, path)


class Environment(UserDict.UserDict):

    def __repr__(self):
        return ("<Environment '%(name)s': user=%(username)s, host=%(host)s, "
                "port=%(port)s, key=%(key_name)s>" % self.data)

    @classmethod
    def import_environment(cls, name):
        config_editor = config.ConfigureEditor()
        return cls(config_editor.get_env(name))


class Repository(UserDict.UserDict):

    def __repr__(self):
        return ("<Repository '%(name)s': type=%(type)s, url=%(url)s " %
                self.data)

    @classmethod
    def import_repo(cls, name):
        config_editor = config.ConfigureEditor()
        return cls(config_editor.get_repo(name))


class SshKey(object):
    """ Manage a ssh key"""

    def __init__(self, name, key_file, pub_file):
        self.name = name
        self.key_file = key_file
        self.pub_file = pub_file

    @classmethod
    def import_key(cls, name):
        """ Import a ssh key by name"""
        config_editor = config.ConfigureEditor()

        return cls(**config_editor.get_key(name))

    def __repr__(self):
        return '<SshKey: {}, {}, {}>'.format(self.name, self.key_file,
                                             self.pub_file)
