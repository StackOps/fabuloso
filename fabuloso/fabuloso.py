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
# import argparse
import ConfigParser
import imp
import itertools
import pkgutil
import os

import environment
import fabulosocmd
import providers


def main():
    """ Execute the script remotely.

    Those are the input parameters:
    """
    def load_environment(config_module):
        environments = getattr(config_module, 'environments')
        return environment.RemoteEnvironment(environments['default'])

    def print_doc(module):
        def delegate_print():
            print module.__doc__
        return delegate_print

    config_module = Utils.load_config_module()
    env = load_environment(config_module)
    catalog = Utils.load_catalog(config_module)
    cmd = fabulosocmd.FabulosoCmd()
    for key, value in catalog.items():
        services, module = value
        setattr(cmd, 'do_' + key, Utils.delegate_method(env, services, module))
        setattr(cmd, 'help_' + key, print_doc(module))
    cmd.cmdloop()


class Fabuloso(object):
    """ Unique entry point via API of this package"""
    def __init__(self, env):
        """ Init with environment"""
        self.env = env
        config_module = Utils.load_config_module()
        self.catalog = Utils.load_catalog(config_module)

    def execute(self, command, service, **kwargs):
        service_empty, module = self.catalog.get(command)
        method = Utils.delegate_method(self.env, service, module)
        method(service, **kwargs)


class Utils(object):

    @staticmethod
    def load_config_module():
        config_file = os.path.join(os.path.expanduser('~'), '.config',
                                   'fabuloso', 'config.py')
        return imp.load_source('config', config_file)

    @staticmethod
    def load_catalog(config_module):
        """Returns a dict that maps the component name with the module."""
        catalogues = getattr(config_module, 'catalogues')
        catalog_dict = {}
        for catalogue in catalogues:
            cat_dir = os.path.join(os.path.dirname(__file__), catalogue)

            # Walk through all the catalog components
            for dirname, subdirnames, filenames in os.walk(cat_dir):
                for subdirname in subdirnames:
                    comp_dir = os.path.join(cat_dir, subdirname)
                    config_path = os.path.join(comp_dir, 'component.cfg')
                    comp_name, comp_file, methods = \
                        Utils.load_component_config_info(config_path)

                    comp_module = imp.load_source(comp_name,
                                                  os.path.join(comp_dir,
                                                               comp_file))
                    module_methods = []
                    for obj in dir(comp_module):
                        if obj in methods:
                            a = getattr(comp_module, obj)
                            module_methods.append(a)
                    catalog_dict[comp_name] = (methods, comp_module)

        return catalog_dict

    @staticmethod
    def load_component_config_info(config_path):
        component_config = ConfigParser.ConfigParser()
        component_config.read(config_path)

        comp_name = component_config.get('component', 'name')
        comp_file = component_config.get('component', 'file')
        methods = component_config.get('component', 'methods').split()
        return comp_name, comp_file, methods

    @staticmethod
    def delegate_method(env, available_services, module):
        def delegator(args):
            list_args = args.split()
            service = list_args[0]
            parameters = {}
            if len(list_args) > 1:
                parameters = Utils.__parse_parameters_into_dict(list_args[1:])

            fabric = providers.FabricProvider(env)
            module_function = getattr(module, service)
            method = fabric.execute_method(module_function)
            method(**parameters)

        return delegator

    def __parse_parameters_into_dict(parameters):
        """ Parse service parameters into dictionary.

        Parameters must be informed in the way: parameter_name:parameter_value
        and it can be as many parameters as the user need. This funtions turns
        it into a dictionary in the way: dict['parameter_name']:
        'parameter_value'
        """

        # Split each parameter_name:parameter_value in the list and flat
        # the list
        flat = list(itertools.chain(*map(lambda x: x.split(':'), parameters)))

        # Zip the list into two: the even values are the 'keys' and the odds
        # are the 'values'
        return dict(zip(flat[0::2], flat[1::2]))


def ee():
    print(pkgutil.get_data('fabuloso', 'data/easter_egg.txt'))
    print("This is the way we deploy OpenStack in StackOps!")
