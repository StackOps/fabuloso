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

import uuid
import shutil
import os.path
import ConfigParser

import pika
import MySQLdb
import prettytable
from fabric.api import puts, sudo, get, put, local
from keystoneclient.v2_0 import client


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


def validate_credentials(user, password, tenant, endpoint, admin_token):
    try:
        keystone = client.Client(token=admin_token, endpoint=endpoint)
        token = keystone.tokens.authenticate(username=user,
                                             tenant_name=tenant,
                                             password=password)
        if token is not None:
            print '\nValidation of credentials for %s user in ' \
                  'tenant %s was successful..\n' % (user, tenant)

    except Exception, e:
        #logging.error("Error at the moment to add a Service. %s" % e)
        raise Exception('Error at the moment to Validate Credentials '
                        'on Keystone for user %s. Please check log %s'
                        % (user, e))


def validate_database(database_type, username, password, host, port,
                      schema, drop_schema=None, install_database=None):
    if database_type == 'mysql':
        port = int(port)
        try:
            con_test = None
            con_test_user = None
            if schema == 'mysql':
                dbtest = MySQLdb.connect(host=host,
                                         user=username,
                                         passwd=password,
                                         port=port)
                #Test with root user, create schema, use it, create tables,
                # populate tables, select and drop schema
                curtest = dbtest.cursor()
                curtest.execute('CREATE DATABASE test_main_database')
                curtest.execute('USE test_main_database')
                curtest.execute('''CREATE TABLE test (
                  id_test int(3) unsigned NOT NULL AUTO_INCREMENT,
                  value_test VARCHAR(15),
                  PRIMARY KEY (id_test, value_test)
                  )
                  ''')
                curtest.execute(('INSERT INTO test (value_test) \n'
                                 'values (\'Data 1\')'))
                curtest.execute('SHOW TABLES')
                con_test = curtest.fetchall()
                dbtest.commit()
                curtest.execute('drop database test_main_database')

                #Test with test user, create schema, use it,
                #create tables, populate tables, select and drop schema
                curtest.execute("CREATE USER %s@%s IDENTIFIED BY %s",
                                ('test', 'localhost', 'test'))
                curtest.execute('GRANT ALL PRIVILEGES ON *.* to %s@%s '
                                'IDENTIFIED BY %s WITH GRANT OPTION',
                                ('test', '%', 'test'))
                dbtestuser = MySQLdb.connect(host=host,
                                             user='test',
                                             passwd='test',
                                             port=port)
                curtestuser = dbtestuser.cursor()
                curtestuser.execute('CREATE DATABASE test_user_database')
                curtestuser.execute('USE test_user_database')
                curtestuser.execute('''CREATE TABLE test_user (
                  id_test int(3) unsigned NOT NULL AUTO_INCREMENT,
                  value_test VARCHAR(15),
                  PRIMARY KEY (id_test, value_test)
                  )
                  ''')
                curtestuser.execute(('INSERT INTO test_user (value_test) \n'
                                     'values (\'Data user 1\')'))
                curtestuser.execute('SHOW TABLES')
                con_test_user = curtestuser.fetchall()
                dbtestuser.commit()
                curtest.execute('drop user test')
                curtest.execute('drop user test@localhost')
                curtest.execute('drop database test_user_database')
                curtestuser.close()
                dbtestuser.close()
                curtest.close()
                dbtest.close()
                db = MySQLdb.connect(host=host,
                                     user=username,
                                     passwd=password,
                                     db=schema,
                                     port=port)
                cur = db.cursor()
            else:
                db = MySQLdb.connect(host=host,
                                     user=username,
                                     passwd=password,
                                     db=schema,
                                     port=port)
                cur = db.cursor()
            cur.execute("SHOW TABLES")
            con = cur.fetchall()
            if con is not None:
                if len(con) > 0:
                    print '\nDatabase connection successfully and schema %s ' \
                          'has some tables...\n' % schema

                else:
                    raise Exception('\nDatabase connection successfully '
                                    'but schema %s seems empty...\n' % schema)

            cur.close()
            db.close()
            print con, con_test, con_test_user
        except Exception, e:
            #import traceback
            #logging.error(traceback.format_exc())
            #logging.error('Database Failed test...%s' % e)
            raise Exception('Database Failed test... %s' % e)


def send_rabbitMQ(service_type, host, port=None, user=None, password=None,
                  virtual_host=None):
    try:
        #Send the message
        if port is not None and user is not None and password is not None \
                and virtual_host is not None:
            credentials = pika.PlainCredentials(user, password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                          port=int(port),
                                          virtual_host=virtual_host,
                                          credentials=credentials))
        if port is not None and user is None and password is None \
                and virtual_host is None:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                          port=int(port)))
        if port is None and user is None and password is None \
                and virtual_host is None:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host))
        channel = connection.channel()
        channel.queue_declare(queue='test')
        channel.basic_publish(exchange='',
                              routing_key='test',
                              body='Test RabbitMQ to %s successfully'
                                   % service_type)
        print " [x] SENT: 'Message test to %s RabbitMQ successfully sent'""" \
              % service_type
        connection.close()
        _receive_rabbitMQ(service_type, host, port, user, password,
                          virtual_host)
    except Exception, e:
        #logging.error('RabbitMQ to %s Test Failed...%s' % (service_type, e))
        raise Exception('RabbitMQ to %s Test Failed...%s' % (service_type, e))


def _receive_rabbitMQ(service_type, host, port=None, user=None, password=None,
                      virtual_host=None):
    try:
        if port is not None and user is not None and password is not None \
                and virtual_host is not None:
            credentials = pika.PlainCredentials(user, password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                          port=int(port),
                                          virtual_host=virtual_host,
                                          credentials=credentials))
        if port is not None and user is None and password is None \
                and virtual_host is None:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host,
                                          port=int(port)))
        if port is None and user is None and password is None \
                and virtual_host is None:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=host))
        channel = connection.channel()
        channel.queue_declare(queue='test')
        print ' [*] Waiting for messages....'
        channel.basic_consume(_callback, queue='test', no_ack=True,
                              consumer_tag='consumer')
        connection.close()
    except Exception, e:
        #logging.error('RabbitMQ to %s Test Failed...%s' % (service_type, e))
        raise Exception('RabbitMQ to %s Test Failed...%s' % (service_type, e))


def _callback(ch, method, properties, body):
        print " [x] RECEIVED: %r" % (body)
        print ' [*] Message sent and received successfully....' \
              'Test completed...'


def copy(src, dest):
    return shutil.copy(os.path.expanduser(src), dest)


def print_dict(obj):
    table = prettytable.PrettyTable(['Property', 'Value'])

    for k, v in obj.items():
        table.add_row([k, v])

    print table


def print_list(objs, fields):
    table = prettytable.PrettyTable(fields)

    for obj in objs:
        row = []

        for field in fields:
            key_name = field.lower().replace(' ', '_')

            row.append(obj[key_name])

        table.add_row(row)

    print table
