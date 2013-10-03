# -*- coding: utf-8 -*-

"""FABuloso: OpenStack deployments

Usage:
    fabuloso list_repositories
    fabuloso show_repository <name>
    fabuloso add_repository <name> <url>
    fabuloso del_repository <name>
    fabuloso list_components [<name>]
    fabuloso list_services [--environment=<name>]
                           <component>

    fabuloso execute_service [--environment=<name>]
                             [--properties=<file>]...
                             <component> <service>

    fabuloso list_environments
    fabuloso show_environment <name>
    fabuloso add_environment <name> <username> <host> <port> <key>
    fabuloso del_environment <name>
    fabuloso list_keys
    fabuloso show_key <name>
    fabuloso add_key <name> <key_path> <pub_path>
    fabuloso del_key <name>

    Options:
        --environment=<name>        Environment [default: localhost]
        --properties=<file>         Properties file in yaml format
"""

import sys
import logging

import yaml
from docopt import docopt

import fabuloso


def main():
    args = __parse_args()

    log = __get_logger()

    log.debug('Command-line arguments: {}'.format(dict(args)))

    FAB = fabuloso.Fabuloso()

    if args['list_repositories']:
        for repo in FAB.list_repositories():
            print repo
    elif args['show_repository']:
        print FAB.get_repository(args['<name>'])
    elif args['add_repository']:
        print FAB.add_repository(args['<name>'], args['<url>'])
    elif args['del_repository']:
        FAB.delete_repository(args['<name>'])
    elif args['list_components']:
        for component in FAB.list_components(args['<name>']):
            print component
    elif args['list_services']:
        environment = FAB.get_environment(args['--environment'])

        # Initialize component without properties
        component = FAB.init_component(args['<component>'], {}, environment)

        for service in component._services:
            print service
    elif args['execute_service']:
        environment = FAB.get_environment(args['--environment'])
        properties = __load_properties(args)

        log.debug('Properties: {}'.format(properties))

        component = FAB.init_component(args['<component>'], properties,
                                       environment)
        getattr(component, args['<service>'])()
    elif args['list_environments']:
        for environment in FAB.list_environments():
            print environment
    elif args['show_environment']:
        print FAB.get_environment(args['<name>'])
    elif args['add_environment']:
        print FAB.add_environment(args['<name>'], args['<username>'],
                                  args['<host>'], args['<port>'],
                                  args['<key>'])
    elif args['del_environment']:
        FAB.delete_environment(args['<name>'])
    elif args['list_keys']:
        for key in FAB.list_keys():
            print key
    elif args['show_key']:
        print FAB.get_key(args['<name>'])
    elif args['add_key']:
        print FAB.add_key(args['<name>'], args['<key_path>'],
                          args['<pub_path>'])
    elif args['del_key']:
        FAB.delete_key(args['<name>'])
    else:
        sys.exit(1)


def __parse_args():
    return docopt(__doc__)


def __get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    return logger


def __load_properties(args):
    results = {}

    for path in args['--properties']:
        with open(path) as f:
            results.update(yaml.load(f.read()))

    return results
