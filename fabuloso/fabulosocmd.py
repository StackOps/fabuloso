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
import cmd
import fabuloso
import exceptions


class FabulosoCmd(cmd.Cmd):
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

    def __init__(self):
        self.fabuloso = fabuloso.Fabuloso()
        self.current_comp = None
        cmd.Cmd.__init__(self)

    def default(self, line):
        print("Unknow command")

    def do_list_components(self, args):
        """ Return the list of available components. """
        print "\nAvailable components are:"
        for component in self.fabuloso.list_components():
            print " * %s%s%s" % (self.HEADER, component._name, self.ENDC)

    def do_list_keys(self, args):
        """ Return the list of available ssh keys"""

        for key in self.fabuloso.list_keys():
            print " * %s%s%s" % (self.HEADER, key.name, self.ENDC)

    def do_list_environments(self, args):
        """ Return the list of available environments. """
        for env in self.fabuloso.list_environments():
            data = env.data
            print " * %s%s%s" % (self.HEADER, data['name'], self.ENDC)

    def do_list_repositories(self, args):
        """ Return the list of available repositories. """
        for env in self.fabuloso.list_repositories():
            data = env.data
            print " * %s%s%s" % (self.HEADER, data['name'], self.ENDC)

    def do_init_component(self, args):
        """Initialize a fabuloso component. 

        Usage:
        $ init {component_name} {environment_name}

        Fabuloso will prompt to ask for properties to initialize the 
        component
        """

        try:
            comp_name, env_name = tuple(args.split())
        except ValueError:
            print "'init' command needs two parameters to run. Type 'help init' for more info"
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
        tmp_prompt = "%s-(initializing %s in environment %s)%s" % (self.OKBLUE, comp_name, env_name, self.ENDC)
        for key, value in properties.items():
            curr_prompt = tmp_prompt + " Insert value for property '%s' [%s]: "
            input_user = raw_input(curr_prompt % (key, value))
            if input_user:
                properties[key] = input_user

        self.current_comp = self.fabuloso.init_component(comp_name, properties, environment)
        self.prompt = self.OKGREEN + "fabuloso [" + comp_name + "/" + env_name + "]" + self.ENDC + " > "

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
        print "\nAvailable services are:"
        for key, value in self.current_comp._services.iteritems():
            print " * %s%s%s" % (self.HEADER, key, self.ENDC)

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

    def do_add_repo(self, args):
        """ Add repository catalog.
            Usage:
                $ add_repo {repo_name} {repo_url} {ssh_key:optional}
        
            Currently ssh_key does not work
        """
        try:
            repo_name, repo_url = tuple(args.split())
        except ValueError:
            print "'add_repo' command needs two parameters to run. Type 'help add_repo' for more info"
            return

        try:
            self.fabuloso.add_repository(repo_name, repo_url) 
        except exceptions.RepositoryAlreadyExists as e:
            print e.msg

    def do_del_repo(self, args):
        """ Deletes a repository. 

        Usage:
        $ del_repo {repo_name}
        """
        msg_error = "'del_repo' command needs just one parameter to run. Type 'help del_repo' for more info"
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


    def do_quit(self, args):
        """ Exit shell"""
        return -1

    def get_names(self):
        """Overriden function to return all the methods.

        The base class (cmd.Cmd) only return the names defined
        by the __class__ and hence, does not return the dinamically
        inserted.
        """
        return dir(self)

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
