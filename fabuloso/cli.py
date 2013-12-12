# -*- coding: utf-8 -*-

"""FABuloso: OpenStack deployments

Usage:
    fabuloso [--debug] list_repositories [--catalog-path=<dir>]
    fabuloso [--debug] show_repository [--catalog-path=<dir>]
                                       <name>
    fabuloso [--debug] add_repository [--key=<key>]
                                      [--branch=<branch>]
                                      [--catalog-path=<dir>]
                                      <name> <url>
    fabuloso [--debug] pull_repository [--key=<key>]
                                       [--catalog-path=<dir>]
                                       <name>
    fabuloso [--debug] del_repository [--catalog-path=<dir>]
                                      <name>
    fabuloso [--debug] list_components [--catalog-path=<dir>]
                                       [<name>]
    fabuloso [--debug] list_services [--environment=<name>]
                                     [--catalog-path=<dir>]
                                     <component>
    fabuloso [--debug] execute_service [--environment=<name>]
                                       [--set-env=<key>=<value>]...
                                       [--properties=<file>]...
                                       [--set-prop=<key>=<value>]...
                                       [--catalog-path=<dir>]
                                       <component> <service>
    fabuloso [--debug] get_template [--extended]
                                    [--catalog-path=<dir>]
                                    <component>
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
        --key=<key>                 Private key [default: nonsecure]
        --branch=<branch>           The git branch name [default: master]
        --environment=<name>        Environment [default: localhost]
        --set-env=<key>=<value>     Override an environment key value
        --properties=<file>         Properties file in yaml format
        --set-prop=<key>=<value>    Override a property value
        --extended                  Used to get a template in extended format
        --catalog-path=<dir>        The catalog root directory
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

    fabuloso_instance = fabuloso.Fabuloso(args['--catalog-path'])

    if args['list_repositories']:
        utils.print_list(fabuloso_instance.list_repositories(),
                         ['Name', 'Type', 'URL', 'Branch'])

    elif args['show_repository']:
        utils.print_dict(fabuloso_instance.get_repository(args['<name>']))

    elif args['add_repository']:
        utils.print_dict(fabuloso_instance.add_repository(
            args['<name>'], args['<url>'], args['--branch'],
            args['--key']))

    elif args['del_repository']:
        fabuloso_instance.delete_repository(args['<name>'])

    elif args['pull_repository']:
        utils.print_dict(fabuloso_instance.pull_repository(
            args['<name>'], args['--key']))

    elif args['list_components']:
        utils.print_list(
            # Components aren't dicts so we need to convert them first
            [comp.to_dict() for comp in
                fabuloso_instance.list_components(args['<name>'])],
            ['Name'])

    elif args['list_services']:
        environment = fabuloso_instance.get_environment(args['--environment'])

        # Initialize component without properties
        component = fabuloso_instance.init_component(
            args['<component>'], {}, environment)

        utils.print_list(
            # Services aren't dicts so we need to convert them first
            [{'name': service} for service in component._services],
            ['Name'])

    elif args['execute_service']:
        environment = __get_environment(fabuloso_instance, args)

        log.debug('Environment: {}'.format(environment))

        properties = __get_properties(args)

        log.debug('Properties: {}'.format(properties))

        component = fabuloso_instance.init_component(
            args['<component>'], properties, environment)

        component.execute_service(args['<service>'])

    elif args['get_template']:
        if args['--extended']:
            result = fabuloso_instance.get_template_extended_data(
                args['<component>'])
        else:
            result = fabuloso_instance.get_template(args['<component>'])

        print json.dumps(result, indent=4)

    elif args['list_environments']:
        utils.print_list(fabuloso_instance.list_environments(),
                         ['Name', 'Username', 'Host', 'Port', 'Key Name'])

    elif args['show_environment']:
        utils.print_dict(fabuloso_instance.get_environment(args['<name>']))

    elif args['add_environment']:
        utils.print_dict(fabuloso_instance.add_environment(
            args['<name>'], args['<username>'],
            args['<host>'], args['<port>'],
            args['<key>']))

    elif args['del_environment']:
        fabuloso_instance.delete_environment(args['<name>'])

    elif args['list_keys']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [key.to_dict() for key in fabuloso_instance.list_keys()],
            ['Name', 'Key file', 'Pub file'])

    elif args['show_key']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(fabuloso_instance.get_key(args['<name>']).to_dict())

    elif args['add_key']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(fabuloso_instance.add_key(
            args['<name>'], args['<key_path>'], args['<pub_path>']).to_dict())

    elif args['gen_key']:
        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(fabuloso_instance.gen_key(args['<name>']).to_dict())

    elif args['del_key']:
        fabuloso_instance.delete_key(args['<name>'])

    else:
        sys.exit(1)


def __parse_args():
    return docopt(__doc__)


def __get_logger(args):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if args['--debug'] else logging.INFO)
    logger.addHandler(logging.StreamHandler())

    return logger


def __get_properties(args):
    result = {}

    for path in args['--properties']:
        with open(path) as f:
            result.update(yaml.load(f.read()))

    for override in args['--set-prop']:
        key, value = override.split('=')
        result[key] = value

    return result


def __get_environment(fab, args):
    result = fab.get_environment(args['--environment'])

    for override in args['--set-env']:
        key, value = override.split('=')
        result[key] = value

    return result
