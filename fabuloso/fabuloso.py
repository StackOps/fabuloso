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
import argparse
import itertools
import pkgutil


def main():
    """ Execute the script remotely.

    Those are the input parameters:
    """
    # Initialize argument's parser
    description = 'Execute python fuctions remotely from a catalog list'
    parser = argparse.ArgumentParser(description=description,
                                     epilog="Run them far away!")
    parser.add_argument('component', type=str)
    parser.add_argument('service', type=str)
    parser.add_argument('parameters', type=str, nargs='*')
    args = parser.parse_args()
    parameters_dict = __parse_parameters_into_dict(args.parameters)
    print parameters_dict


def ee():
    print(pkgutil.get_data('fabuloso', 'data/easter_egg.txt'))
    print("This is the way we deploy OpenStack in StackOps!")


def execute(component, service, **kwargs):
    catalog = __load_catalog()
    module = __import__(catalog[component])
    function = getattr(module, service)
    function(**kwargs)


def __parse_parameters_into_dict(parameters):
    """ Parse service parameters into dictionary.

    Parameters must be informed in the way: parameter_name:parameter_value
    and it can be as many parameters as the user need. This funtions turns it
    into a dictionary in the way: dict['parameter_name']: 'parameter_value'
    """

    # Split each parameter_name:parameter_value in the list and flat
    # the list
    flat = list(itertools.chain(*map(lambda x: x.split(':'), parameters)))

    # Zip the list into two: the even values are the 'keys' and the odds are
    # the 'values'
    return dict(zip(flat[0::2], flat[1::2]))


def __load_catalog():
    """Returns a dict that maps the component name with the module."""
    pass
