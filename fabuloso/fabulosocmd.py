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
        print "\nAvailable components are:"
        for component in self.fabuloso.list_components():
            print " * %s%s%s" % (self.HEADER, component._name, self.ENDC)

    def do_init(self, args):
        """Initialize a component. """
        if not args in self.fabuloso._catalog:
            print "Component '%s' not available" % args 
            return

        properties = self.fabuloso.get_template(args)
        tmp_prompt = "%s-(initializing %s)%s" % (self.OKBLUE, args, self.ENDC)
        for key, value in properties.items():
            curr_prompt = tmp_prompt + " Insert value for property '%s' [%s]: "
            input_user = raw_input(curr_prompt % (key, value))
            if input_user:
                properties[key] = input_user

        tmp_prompt = "%s-(connection data %s)%s" % (self.MAGENTA, args, self.ENDC)
        host = raw_input(tmp_prompt + " Insert remote host IP: ")
        port = raw_input(tmp_prompt + " Insert remote host port: ")
        username = raw_input(tmp_prompt + " Insert username: ")
        key_file = raw_input(tmp_prompt + " Insert key file path: ")
        environment = {'host': host,
                       'port': port,
                       'ssh_key_file': key_file,
                       'username': username}

        self.current_comp = self.fabuloso.init_component(args, properties, environment)
        self.prompt = self.OKGREEN + "fabuloso [" + args + "]" + self.ENDC + " > "

    def do_finalize(self, args):
        self.current_comp = None
        self.prompt = self.OKGREEN + "fabuloso" + self.ENDC + " > "

    def do_list_services(self, args):
        if not self.current_comp:
            print "No component initialized. Can not list services"
            return
        print "\nAvailable services are:"
        for key, value in self.current_comp._services.iteritems():
            print " * %s%s%s" % (self.HEADER, key, self.ENDC)

    def do_execute(self, args):
        if not self.current_comp:
            print "No component initialized. Can not execute any service"
            return
        if not args in self.current_comp._services:
            print ("Service '%s' not available in current "
                   "component '%s'") % (args, self.current_comp._name)
            return
        self.current_comp.execute_service(args)

    def do_add_repo(self, args):
        """ Add repository catalog"""
        self.fabuloso.add_repository(args[0], args[1]) 


    def help_init(self):
        print ("Initialize a fabuloso component")

    def help_finalize(self):
        print ("Finalize a fabuloso component")

    def help_list_components(self):
        print ("List the available fabuloso components")

    def help_list_services(self):
        print ("List services by loaded component")

    def help_execute(self):
        print ("Execute a service from a loaded component")

    def help_quit(self):
        print ("Exit shell")

    def do_quit(self, args):
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
