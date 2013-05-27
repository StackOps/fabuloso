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


class FabulosoCmd(cmd.Cmd):
    """Override the Cmd class.

    This class offers the command-line shell for fabuloso.
    All the 'do_*' methods are injected dynamically according
    and that's the reason so few methods are exposed.
    """
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'
    FAIL = '\033[91m'
    prompt = OKGREEN + "fabuloso" + ENDC + " > "

    def __init__(self):
        cmd.Cmd.__init__(self)

    def default(self, line):
        print("Component %s%s%s not loaded" %
              (self.FAIL, line.split()[0], self.ENDC))

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
            print("Available components are:\n")
            for doc in cmds_doc:
                if doc not in ['help', 'quit']:
                    print "* %s%s%s" % (HEADER, doc, ENDC)
