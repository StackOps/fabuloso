# -*- coding: utf-8 -*-
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

import cmd

import fabuloso
from . import exceptions, utils


class FabulosoShell(cmd.Cmd, object):
    """Override the Cmd class.

    This class offers the command-line shell for fabuloso.
    All the 'do_*' methods are injected dynamically according
    and that's the reason so few methods are exposed.
    """
    OKGREEN = '\033[92m'
    OKBLUE = '\033[94m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'
    FAIL = '\033[91m'
    HEADER = '\033[95m'
    prompt = OKGREEN + 'fabuloso' + ENDC + ' > '

    def __init__(self, *args, **kwargs):
        super(FabulosoShell, self).__init__(*args, **kwargs)

        self.fabuloso = fabuloso.Fabuloso()
        self.current_comp = None

    def default(self, line):
        print("Unknow command")

    def emptyline(self):
        pass

    def get_names(self):
        """Overriden function to return all the methods.

        The base class (cmd.Cmd) only return the names defined
        by the __class__ and hence, does not return the dinamically
        inserted.
        """
        return dir(self)

    def do_list_components(self, args):
        """Return the list of available components. An optional
        `repo_name` argument can be passed to list only the components
        of the given repo if any.

        Usage: list_components [repo_name]
        """

        if args:
            args = args.split()

            if len(args) != 1:
                print "'list_components' takes at most 1 argument"
                return

            repo = args[0]
        else:
            repo = None

        try:
            components = self.fabuloso.list_components(repo)
        except exceptions.RepositoryNotFound as error:
            print error.msg
            return

        # TODO(jaimegildesagredo): Components aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [comp.to_dict() for comp in components],
            ['Name'])

    def do_list_keys(self, args):
        """ Return the list of available ssh keys"""

        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [key.to_dict() for key in self.fabuloso.list_keys()],
            ['Name', 'Key file', 'Pub file'])

    def do_show_key(self, args):
        """ Prints the details of a key.

        Usage:
        $ show_key {key_name}
        """

        msg_error = ("'show_key' command needs just one parameter to run. "
                     "Type 'help show_key' for more info")
        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())
            if len(arg_split) != 1:
                print msg_error
                return
            key_name = arg_split[0]
        except ValueError:
            print msg_error
            return

        try:
            key = self.fabuloso.get_key(key_name)
        except exceptions.KeyNotFound as e:
            print e.msg + " Use 'list_keys' to see available ssh keys."
        else:
            # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
            #                          convert them first

            utils.print_dict(key.to_dict())

    def do_add_key(self, args):
        """Add a new ssh key pair"""

        if args:
            print "No input arguments needed. Ignored"

        tmp_prompt = "%s-(Adding new keypair)-%s" % (self.OKBLUE, self.ENDC)

        name = raw_input(tmp_prompt + 'Name: ')
        key_path = raw_input(tmp_prompt + 'Key path: ')
        pub_path = raw_input(tmp_prompt + 'Pub path: ')

        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(
            self.fabuloso.add_key(name, key_path, pub_path).to_dict())

    def do_gen_key(self, args):
        """Generates a new key pair"""

        msg_error = ("'gen_key' command needs just one parameter to run. "
                     "Type 'help gen_key' for more info")

        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())

            if len(arg_split) != 1:
                print msg_error
                return

            name = arg_split[0]
        except ValueError:
            print msg_error
            return

        # TODO(jaimegildesagredo): SshKeys aren't dicts so we need to
        #                          convert them first

        utils.print_dict(self.fabuloso.gen_key(name).to_dict())

    def do_del_key(self, args):
        """Deletes a keypair"""

        msg_error = ("'del_key' command needs just one parameter to run. "
                     "Type 'help del_key' for more info")

        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())
            if len(arg_split) != 1:
                print msg_error
                return

            name = arg_split[0]
        except ValueError:
            print msg_error
            return

        try:
            self.fabuloso.delete_key(name)
        except exceptions.KeyNotFound as error:
            print error.msg

    def do_list_environments(self, args):
        """ Return the list of available environments. """

        utils.print_list(self.fabuloso.list_environments(),
                         ['Name', 'Username', 'Host', 'Port', 'Key Name'])

    def do_show_environment(self, args):
        """ Prints the details of an environment.

        Usage:
        $ show_environment {environment_name}
        """

        msg_error = ("'show_environment' command needs just one parameter "
                     "to run. Type 'help show_environment' for more info")

        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())
            if len(arg_split) != 1:
                print msg_error
                return
            env_name = arg_split[0]
        except ValueError:
            print msg_error
            return

        try:
            env = fabuloso.Environment.import_environment(env_name)
        except exceptions.EnvironmentNotFound as e:
            print(e.msg + " Use 'list_environments' to see available "
                  "environments.")
        else:
            utils.print_dict(env)

    def do_add_environment(self, args):
        """Add an enviroment."""

        if args:
            print "No input arguments needed. Ignored"

        tmp_prompt = "%s-(Adding new environment)-%s" % (self.OKBLUE,
                                                         self.ENDC)

        env_name = raw_input(tmp_prompt + " Name: ")
        username = raw_input(tmp_prompt + " Remote username: ")
        host = raw_input(tmp_prompt + " Remote host: ")
        port = raw_input(tmp_prompt + " Remote port: ")
        key_name = raw_input(tmp_prompt + " Ssh Key name: ")

        try:
            env = self.fabuloso.add_environment(env_name, username, host,
                                                port, key_name)

        except exceptions.KeyNotFound as e:
            print e.msg + " Use 'list_keys' to see available ssh keys."
        except exceptions.EnvironmentAlreadyExists as e:
            print e.msg
        else:
            utils.print_dict(env)

    def do_del_environment(self, args):
        """Deletes an environment.

        Usage
        $ del_environment {env_name}
        """

        msg_error = ("'del_environment' command needs just one parameter "
                     " to run. Type 'help del_environment' for more info")

        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())
            if len(arg_split) != 1:
                print msg_error
                return
            env_name = arg_split[0]
        except ValueError:
            print msg_error
            return

        try:
            self.fabuloso.delete_environment(env_name)
        except exceptions.EnvironmentNotFound as e:
            print e.msg

    def do_list_repositories(self, args):
        """ Return the list of available repositories. """

        utils.print_list(self.fabuloso.list_repositories(),
                         ['Name', 'Type', 'URL'])

    def do_show_repository(self, args):
        """ Prints the details of a repo.

        Usage:
        $ show_repo {repo_name}
        """

        msg_error = ("'show_repo' command needs just one parameter to run. "
                     "Type 'help show_repo' for more info")
        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())
            if len(arg_split) != 1:
                print msg_error
                return
            repo_name = arg_split[0]
        except ValueError:
            print msg_error
            return

        try:
            repo = self.fabuloso.get_repository(repo_name)
        except exceptions.RepositoryNotFound as e:
            print(e.msg + " Use 'list_repositories' to see available "
                  "repositories.")
        else:
            utils.print_dict(repo)

    def do_add_repository(self, args):
        """ Add repository catalog.
            Usage:
                $ add_repository {repo_name} {repo_url} {ssh_key:optional}

        """
        list_args = args.split()
        if len(list_args) == 2:
            # If there are only two arguments, insert the default key
            list_args.append('nonsecure')
        elif len(list_args) == 3:
            pass
        else:
            print("'add_repository' command needs two or three "
                  "parameters to run. "
                  "Type 'help add_repository' for more info")

            return

        try:
            repo = self.fabuloso.add_repository(*tuple(list_args))
        except exceptions.FabulosoError as e:
            print e.msg
        else:
            utils.print_dict(repo)

    def do_del_repository(self, args):
        """ Deletes a repository.

        Usage:
        $ del_repository {repo_name}
        """

        msg_error = ("'del_repository' command needs just one parameter "
                     "to run. Type 'help del_repository' for more info")

        if not args:
            print msg_error
            return

        try:
            arg_split = tuple(args.split())
            if len(arg_split) != 1:
                print msg_error
                return
            repo_name = arg_split[0]
        except ValueError:
            print msg_error
            return

        try:
            self.fabuloso.delete_repository(repo_name)
        except exceptions.RepositoryNotFound as e:
            print e.msg

    def do_init_component(self, args):
        """Initialize a fabuloso component.

        Usage:
        $ init_component {component_name} {environment_name}

        Fabuloso will prompt to ask for properties to initialize the
        component
        """

        try:
            comp_name, env_name = tuple(args.split())
        except ValueError:
            print("'init_component' command needs two parameters to run. "
                  "Type 'help init_component' for more info")

            return

        """Initialize a component. """
        if not comp_name in self.fabuloso._catalog:
            print "Component '%s' not available" % args
            return

        try:
            environment = fabuloso.Environment.import_environment(env_name)
        except exceptions.EnvironmentNotFound as e:
            print e.msg
            return

        properties = self.fabuloso.get_template(comp_name)

        tmp_prompt = "%s-(initializing %s in environment %s)%s" % (
            self.OKBLUE, comp_name, env_name, self.ENDC)

        for key, value in properties.items():
            curr_prompt = tmp_prompt + " Insert value for property '%s' [%s]: "
            input_user = raw_input(curr_prompt % (key, value))
            if input_user:
                properties[key] = input_user

        self.current_comp = self.fabuloso.init_component(comp_name, properties,
                                                         environment)

        self.prompt = (self.OKGREEN + "fabuloso [" + comp_name + "/"
                       + env_name + "]" + self.ENDC + " > ")

    def do_finalize_component(self, args):
        """ Finalize a component.

        That means the initialized component will be dropped and
        'list_services' and 'execute_service' will not be
        available as actions.
        """
        self.current_comp = None
        self.prompt = self.OKGREEN + "fabuloso" + self.ENDC + " > "

    def do_list_services(self, args):
        """ List the available services.

        A component must be initialized to see the correct output.
        """

        if not self.current_comp:
            print "No component initialized. Can not list services"
            return

        # TODO(jaimegildesagredo): Services aren't dicts so we need to
        #                          convert them first

        utils.print_list(
            [{'name': service} for service in self.current_comp._services],
            ['Name'])

    def do_execute_service(self, args):
        """Execute a service from a loaded component.

        Usage:
        $ execute {service_name}

        run 'list_services' to know the available services.
        """

        if not self.current_comp:
            print "No component initialized. Can not execute any service"
            return

        if not args in self.current_comp._services:
            print ("Service '%s' not available in current "
                   "component '%s'") % (args, self.current_comp._name)
            return

        self.current_comp.execute_service(args)

    def do_quit(self, args):
        """ Exit shell"""
        return -1

    def do_help(self, arg):
        """Override the help in a prettier way"""
        HEADER = '\033[95m'
        ENDC = '\033[0m'
        if arg:
            try:
                func = getattr(self, 'help_' + arg)
            except AttributeError:
                try:
                    doc = getattr(self, 'do_' + arg).__doc__
                    if doc:
                        self.stdout.write("%s\n" % str(doc))
                        return
                except AttributeError:
                    pass
                self.stdout.write("%s\n" % str(self.nohelp % (arg,)))
                return
            func()
        else:
            names = self.get_names()
            cmds_doc = []
            cmds_undoc = []
            help = {}
            for name in names:
                if name[:5] == 'help_':
                    help[name[5:]] = 1
            names.sort()
            # There can be duplicates if routines overridden
            prevname = ''
            for name in names:
                if name[:3] == 'do_':
                    if name == prevname:
                        continue
                    prevname = name
                    cmd = name[3:]
                    if cmd in help:
                        cmds_doc.append(cmd)
                        del help[cmd]
                    elif getattr(self, name).__doc__:
                        cmds_doc.append(cmd)
                    else:
                        cmds_undoc.append(cmd)
            print("Available methods are:\n")
            for doc in cmds_doc:
                if doc not in ['help', 'quit']:
                    print "* %s%s%s" % (HEADER, doc, ENDC)


def main():
    FabulosoShell().cmdloop()
