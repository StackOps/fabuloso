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
import json
import os

import yaml


class Component(object):

    services = {}
    methods = {}
    module = None

    """Parses component files and extracts its data"""
    def __init__(self, comp_dir):
        self._comp_dir = comp_dir
        self._config_path = os.path.join(comp_dir, 'component.yml')
        with open(self._config_path) as f:
            self._config = yaml.load(f.read())

        self._check_component_coherency()
        self._load_services()
        self._load_methods()
        self._load_module()

    @property
    def name(self):
        return self._config['name']

    @property
    def path(self):
        return os.path.join(self._comp_dir, self._config['file'])

    def __repr__(self):
        return json.dumps(self._config, indent=4)

    def _load_methods(self):
        self.methods = {}
        for method in self._config['Methods']:
            method_name = method['name']
            list_params = []
            if 'params' in method:
                for param in method['params']:
                    list_params.append((param['name'], param['description']))

            self.methods[method_name] = list_params

    def _load_services(self):
        self.services = {}
        for service in self._config['Services']:
            name = service['name']
            list_methods = []
            for method in service['methods']:
                list_methods.append(method)
            description = service['description']
            self.services[name] = (description, list_methods)

    def _load_module(self):
        self.module = imp.load_source(self.name, self.path)

    def _check_component_coherency(self):
        """ Checks if the component has coherency.

        According with the fabuloso doc [todo link here], this method
        checks if the component has coherency.
        """
        pass
