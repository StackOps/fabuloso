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

import component
import providers


class Fabuloso(object):
    """ Unique entry point via API of this package"""
    def __init__(self, env):
        """ Init with environment"""
        self.env = env
        self.catalog = self._load_catalog(self.env)

    def list_components(self):
        """ Return the catalog in a string/json way."""
        return self.catalog.values()

    def execute_service(self, comp_name, service, **kwargs):
        comp = self.catalog.get(comp_name)
        self.provider = providers.FabricProvider(self.env)
        description, methods = comp.services[service]
        for method in methods:
            service_args = self.__build_args(comp, method, kwargs)
            self.provider.execute_method(getattr(comp.module, method),
                                         **service_args)

    def __build_args(self, comp, method, kwargs):
        """ Build appropiate args depending on the method

        The execute service receives a list of arguments that may be
        useful for one or more methods. This function filters only
        the ones that are needed for the current 'method'
        """
        method_args = {}
        parameters = comp.methods[method]
        for parameter in parameters:
            param_name, description = parameter
            method_args[param_name] = kwargs[param_name]
        return method_args

    def _load_catalog(self, env):
        """Returns a dict that maps the component name with the module."""
        catalogues = env['catalog']
        catalog_dict = {}
        for catalogue in catalogues:
            cat_dir = os.path.join(os.path.dirname(__file__), catalogue)

            # Walk through all the catalog components
            for dirname, subdirnames, filenames in os.walk(cat_dir):
                for subdirname in subdirnames:
                    comp_dir = os.path.join(cat_dir, subdirname)
                    try:
                        comp = component.Component(comp_dir)
                        catalog_dict[comp.name] = comp
                    except IOError:
                        # Skip the failing components
                        continue

        return catalog_dict
