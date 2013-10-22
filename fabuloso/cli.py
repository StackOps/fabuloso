# -*- coding: utf-8 -*-

"""FABuloso: OpenStack deployments

Usage:
    fabuloso [--debug] list_repositories
    fabuloso [--debug] show_repository <name>
    fabuloso [--debug] add_repository <name> <url> [<key>]
    fabuloso [--debug] del_repository <name>
    fabuloso [--debug] list_components [<name>]
    fabuloso [--debug] list_services [--environment=<name>]
                                     <component>
    fabuloso [--debug] execute_service [--environment=<name>]
                                       [--properties=<file>]...
                                       <component> <service>
    fabuloso [--debug] get_template <component>
    fabuloso [--debug] list_environments
    fabuloso [--debug] show_environment <name>
    fabuloso [--debug] add_environment <name> <username> <host> <port> <key>
    fabuloso [--debug] del_environment <name>
    fabuloso [--debug] list_keys
    fabuloso [--debug] show_key <name>
    fabuloso [--debug] add_key <name> <key_path> <pub_path>
    fabuloso [--debug] gen_key <name>
    fabuloso [--debug] del_key <name>

    Options:
        -h --help                   Show this screen
        --debug                     Show debug info
        --environment=<name>        Environment [default: localhost]
        --properties=<file>         Properties file in yaml format
"""

import sys
import json
import logging

import yaml
from docopt import docopt

import fabuloso
from fabuloso import utils


def main():
    args = __parse_args()

    log = __get_logger(args)

    log.debug('Command-line arguments: {}'.format(dict(args)))

    FAB = fabuloso.Fabuloso()

    if args['list_repositories']:
        utils.print_list(FAB.list_repositories(), ['Name', 'Type', 'URL'])

    elif args['show_repository']:
        utils.print_dict(FAB.get_repository(args['<name>']))

    elif args['add_repository']:
        if args['<key>']:
            utils.print_dict(FAB.add_repository(args['<name>'],
                                                args['<url>'],
                                                args['<key>']))
        else:
            utils.print_dict(FAB.add_repository(args['<name>'], args['<url>']))

    elif args['del_repository']:
        FAB.delete_repository(args['<name>'])

    elif args['list_components']:
        # TODO(jaimegildesagredo): Components aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [comp.to_dict() for comp in FAB.list_components(args['<name>'])],
            ['Name'])

    elif args['list_services']:
        environment = FAB.get_environment(args['--environment'])

        # Initialize component without properties
        component = FAB.init_component(args['<component>'], {}, environment)

        # TODO(jaimegildesagredo): Services aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [{'name': service} for service in component._services],
            ['Name'])

    elif args['execute_service']:
        environment = FAB.get_environment(args['--environment'])

        properties = __load_properties(args)

        log.debug('Properties: {}'.format(properties))

        component = FAB.init_component(
            args['<component>'], properties, environment)

        component.execute_service(args['<service>'])

    elif args['get_template']:
        print json.dumps(FAB.get_template(args['<component>']), indent=4)

    elif args['list_environments']:
        utils.print_list(FAB.list_environments(),
                         ['Name', 'Username', 'Host', 'Port', 'Key Name'])

    elif args['show_environment']:
        utils.print_dict(FAB.get_environment(args['<name>']))

    elif args['add_environment']:
        utils.print_dict(FAB.add_environment(
            args['<name>'], args['<username>'],
            args['<host>'], args['<port>'],
            args['<key>']))

    elif args['del_environment']:
        FAB.delete_environment(args['<name>'])

    elif args['list_keys']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [key.to_dict() for key in FAB.list_keys()],
            ['Name', 'Key file', 'Pub file'])

    elif args['show_key']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(FAB.get_key(args['<name>']).to_dict())

    elif args['add_key']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(FAB.add_key(
            args['<name>'], args['<key_path>'], args['<pub_path>']).to_dict())

    elif args['gen_key']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(FAB.gen_key(args['<name>']).to_dict())

    elif args['del_key']:
        FAB.delete_key(args['<name>'])

    else:
        sys.exit(1)


def __parse_args():
    return docopt(__doc__)


def __get_logger(args):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args['--debug'] else logging.INFO)
    logger.addHandler(logging.StreamHandler())

    return logger


def __load_properties(args):
    results = {}

    for path in args['--properties']:
        with open(path) as f:
            results.update(yaml.load(f.read()))

    return results
