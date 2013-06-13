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
from fabric.api import puts, sudo, get, put, local

import uuid
import ConfigParser


def sql_connect_string(host, password, port, schema, username):
    sql_connection = 'mysql://%s:%s@%s:%s/%s' % (username, password, host,
                                                 port, schema)
    return sql_connection


def delete_option(config_file, name, section='DEFAULT'):

    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    temp_file = "/tmp/%s" % uuid.uuid1()
    sudo("cp %s %s" % (config_file, temp_file))
    sudo("chmod 666 %s" % temp_file)
    local_file = "/tmp/%s" % uuid.uuid1()
    get(temp_file, local_file)
    sudo('rm -f %s' % temp_file)
    cfg = ConfigParser.ConfigParser()
    cfg.read([local_file])
    cfg.remove_option(section, name)
    cfg.write(open(local_file, 'w'))
    put(local_file, config_file, use_sudo=True)
    local('rm -f %s' % local_file)


def set_option(config_file, name, value, comment=None, section='DEFAULT'):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
#    delete_property(name)
#    comm=''
#    if comment is not None:
#        comm = '# %s' % comment
#    sudo('echo "%s=%s       %s" >> %s' % (name,value,comm,config_file))
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    temp_file = "/tmp/%s" % uuid.uuid1()
    sudo("cp %s %s" % (config_file, temp_file))
    sudo("chmod 666 %s" % temp_file)
    local_file = "/tmp/%s" % uuid.uuid1()
    get(temp_file, local_file)
    sudo('rm -f %s' % temp_file)
    cfg = ConfigParser.ConfigParser()
    cfg.read([local_file])
    cfg.set(section, name, value)
    cfg.write(open(local_file, 'w'))
    put(local_file, config_file, use_sudo=True)
    local('rm -f %s' % local_file)


def get_option(config_file, name, section='DEFAULT'):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    d = get_options(config_file)
    result = ''
    try:
        result = d[section][name]
    except:
        pass
    return result


def get_options(config_file):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    temp_file = "/tmp/%s" % uuid.uuid1()
    sudo("cp %s %s" % (config_file, temp_file))
    sudo("chmod 666 %s" % temp_file)
    local_file = "/tmp/%s" % uuid.uuid1()
    get(temp_file, local_file)
    sudo('rm -f %s' % temp_file)
    cfg = ConfigParser.SafeConfigParser(allow_no_value=True)
    cfg.read([local_file])
    sec = cfg.sections()
    sec.append('DEFAULT')
    d = {}
    for section_name in sec:
        section = dict(cfg.items(section_name))
        d[section_name] = section
    local('rm -f %s' % local_file)
    return d


def uncomment_property(config_file, name):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    sudo('''sed -i 's&^#.*%s.*=\(.*\)$&%s =\\1&g' %s'''
         % (name, name, config_file))


def comment_property(config_file, name):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    sudo('''sed -i 's&^.*%s.*=\(.*\)$&# %s =\\1&g' %s'''
         % (name, name, config_file))


def modify_property(config_file, name, value):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    sudo('''sed -i 's&^%s.*=\(.*\)$&%s=%s&g' %s'''
         % (name, name, value, config_file))


def modify_property_with_semicolon(config_file, name, value):
    if config_file is None:
        puts("{'error':'No config file.'}")
        SystemExit()
    sudo('''sed -i 's&^\$%s.*=.*\"\(.*\)\";$&\$%s=\"%s\";&g' %s'''
         % (name, name, value, config_file))
