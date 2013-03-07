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
#   limitations under the License.from fabric.api import *

from fabric.api import *
from cuisine import *

@task
def stop():
    with settings(warn_only=True):
        sudo("nohup service mysql stop")

@task
def start():
    stop()
    sudo("nohup service mysql start")

@task
def configure_ubuntu_packages(root_pass):
    """Configure mysql ubuntu packages"""
    sudo('echo mysql-server-5.5 mysql-server/root_password password %s | debconf-set-selections' % root_pass)
    sudo('echo mysql-server-5.5 mysql-server/root_password_again password %s | debconf-set-selections' % root_pass)
    sudo('echo mysql-server-5.5 mysql-server/start_on_boot boolean true | debconf-set-selections')
    package_ensure('mysql-server')
    package_ensure('python-mysqldb')

@task
def configure(root_pass='stackops', cluster=False):
    """Generate mysql configuration. Execute on both servers"""
    configure_ubuntu_packages(root_pass)
    if cluster:
        stop()
        sudo('echo "manual" >> /etc/init/mysql.override')
        sudo('chmod -R og=rxw /var/lib/mysql')
        sudo('chown -R mysql:mysql /var/lib/mysql')
    sudo("sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf")
    sudo('''mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%%' IDENTIFIED BY '%s' WITH GRANT OPTION;"''' % (root_pass, root_pass))

def setup_schema(drop_schema, password, root_pass, schema, username, mysql_host):
    if drop_schema:
        sudo('mysql -uroot -p%s -e "DROP DATABASE IF EXISTS %s;"' % (root_pass, schema))
    sudo('mysql -uroot -p%s -e "CREATE DATABASE %s;"' % (root_pass, schema))
    sudo(
        '''mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'localhost' IDENTIFIED BY '%s';"''' % (
            root_pass, schema, username, password))
    sudo('''mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%%' IDENTIFIED BY '%s';"''' % (
        root_pass, schema, username, password))
    if mysql_host is not None:
        sudo(
            '''mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%s' IDENTIFIED BY '%s';"''' % (
                root_pass, schema, username, mysql_host, password))

@task
def configure_nova(root_pass, drop_schema=False, schema='nova', username='nova', password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_glance(root_pass,drop_schema=False,schema='glance',username='glance',password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_keystone(root_pass,drop_schema=False,schema='keystone',username='keystone',password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_portal(root_pass,drop_schema=False,schema='portal',username='portal',password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_quantum(root_pass,drop_schema=False,schema='quantum',username='quantum',password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_cinder(root_pass,drop_schema=False,schema='cinder',username='cinder',password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_accounting(root_pass,drop_schema=False,schema='accounting',username='accounting',password='stackops', mysql_host=None):
    setup_schema(drop_schema, password, root_pass, schema, username, mysql_host)

@task
def configure_all_schemas(root_pass,drop_schema=False, mysql_host=None):
    configure_portal(root_pass,drop_schema,mysql_host)
    configure_keystone(root_pass,drop_schema,mysql_host)
    configure_glance(root_pass,drop_schema,mysql_host)
    configure_nova(root_pass,drop_schema,mysql_host)
    configure_quantum(root_pass,drop_schema,mysql_host)
    configure_cinder(root_pass,drop_schema,mysql_host)
    configure_accounting(root_pass,drop_schema,mysql_host)
