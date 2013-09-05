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
import imp
import os

import yaml

import component
import providers
import utils


class Fabuloso(object):

    def __init__(self, catalog_dir=None):
        if catalog_dir is None:
            config_file = os.path.expanduser('~/.config/fabuloso/config.py')
            module = imp.load_source('config', config_file)
            catalog_dir = getattr(module, 'catalog_dir')

        """ Init with catalog dir"""
        self.catalog = self._load_catalog(catalog_dir)

    def init_component(self, component_name, properties, environment):
        comp = self.catalog[component_name]
        comp.set_properties(properties)
        comp.set_environment(environment)
        return comp

    def init_component_extended_data(self, component_name,
                                     ext_properties, environment):
        properties = {}
        map(properties.update, ext_properties.values())
        return self.init_component(component_name, properties, environment)

    def get_template(self, component_name):
        """ Retrieves the list of needed properties"""
        comp = self.catalog[component_name]
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
        comp = self.catalog[component_name]
        props = {}
        for service, service_def in comp._services.items():
            service_props = {}
            description, methods = service_def
            for method in methods:
                params = comp._get_method_params(method)
                for param in params:
                    if not param in service_props:
                        service_props[param] = comp._get_param_default(param, method)
            props[service] = service_props
        return props

    def list_components(self):
        """ Return the catalog in a string/json way."""
        return self.catalog.values()

    def _load_catalog(self, catalog_dir):
        """Returns a dict that maps the component name with the module."""
        catalog_dict = {}
        for catalogue in catalog_dir:
            cat_dir = os.path.join(os.path.dirname(__file__), catalogue)

            # Walk through all the catalog components
            for dirname, subdirnames, filenames in os.walk(cat_dir):
                for subdirname in subdirnames:
                    comp_dir = os.path.join(cat_dir, subdirname)
                    try:
                        comp = self._load_component(comp_dir)
                        catalog_dict[comp._name] = comp
                    except IOError:
                        # Skip the failing components
                        continue

        return catalog_dict

    def _load_component(self, comp_dir):
        """ Based on the definition file, build the component.
        """
        definition_path = os.path.join(comp_dir, 'component.yml')
        with open(definition_path) as f:
            definition = yaml.load(f.read())

        # load the module that belongs to this component
        component_name = definition['name']
        module_path = os.path.join(comp_dir, definition['file'])
        module = imp.load_source(component_name, module_path)

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
