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
import itertools
import os
import pkgutil

import fabulosocmd


def main():
    """ Execute the script remotely.

    Those are the input parameters:
    """
    def print_doc(comp):
        def delegate_print():
            RED = '\033[91m'
            BLUE = '\033[94m'
            HEADER = '\033[95m'
            ENDC = '\033[0m'
            print "Available services for this component are:\n"
            for name_s, tup in comp._services.items():
                print "* %s%s%s: %s" % (HEADER, name_s, ENDC, tup[0])

        return delegate_print

    def delegate_execution(fab, comp_name):
        def fabuloso_wrapper(args):
            args_list = args.split()
            service = args_list[0]
            params = _parse_parameters_into_dict(args_list[1:])
            fab.execute_service(comp_name, service, **params)

        return fabuloso_wrapper

    cmd = fabulosocmd.FabulosoCmd()
    # for comp_name, comp in fab._catalog.items():
    #     setattr(cmd, 'do_' + comp_name, delegate_execution(fab, comp_name))
    #     setattr(cmd, 'help_' + comp_name, print_doc(comp))
    cmd.cmdloop()


def _parse_parameters_into_dict(parameters):
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
