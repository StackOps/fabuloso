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
"""MySQL Component.

This component exposes methods for mysql purposes.
The following are the services available:
    * configure root_pass:string -> configures the mysql admin with the
                                    'root_pass' parameter
    * start -> starts the mysql service
    * stop -> stops the mysql service
"""
from fabric.api import sudo, settings
from cuisine import package_ensure


def configure(root_pass):
    """Generate mysql configuration. Execute on both servers"""
    __configure_ubuntu_packages(root_pass)
    stop()

    sudo('echo "manual" >> /etc/init/mysql.override')
    sudo('chmod -R og=rxw /var/lib/mysql')
    sudo('chown -R mysql:mysql /var/lib/mysql')
    start()
    sudo("sed -i 's/127.0.0.1/0.0.0.0/g' /etc/mysql/my.cnf")
    sudo("""mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON *.* TO
            'root'@'%%' IDENTIFIED BY '%s' WITH GRANT OPTION;" """
         % (root_pass, root_pass))


def start():
    stop()
    sudo("nohup service mysql start")


def __configure_ubuntu_packages(root_pass):
    """Configure mysql ubuntu packages"""
    sudo('echo mysql-server-5.5 mysql-server/root_password password %s'
         ' | debconf-set-selections' % root_pass)
    sudo('echo mysql-server-5.5 mysql-server/root_password_again password %s'
         ' | debconf-set-selections' % root_pass)
    sudo('echo mysql-server-5.5 mysql-server/start_on_boot boolean true'
         ' | debconf-set-selections')
    package_ensure('mysql-server')
    package_ensure('python-mysqldb')


def stop():
    with settings(warn_only=True):
        sudo("nohup service mysql stop")


def setup_schema(root_pass, username, password, schema_name,
                 host=None, drop_previous=False):
    if drop_previous:
        sudo('mysql -uroot -p%s -e "DROP DATABASE IF EXISTS %s;"'
             % (root_pass, schema_name))
    sudo('mysql -uroot -p%s -e "CREATE DATABASE %s;"' % (root_pass,
                                                         schema_name))
    sudo("""mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO
            '%s'@'localhost' IDENTIFIED BY '%s';" """
         % (root_pass, schema_name, username, password))
    if host is not None:
        sudo("""mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO
                '%s'@'%s' IDENTIFIED BY '%s';" """
             % (root_pass, schema_name, username, host, password))
    else:
        sudo("""mysql -uroot -p%s -e "GRANT ALL PRIVILEGES ON %s.* TO '%s'@'%%'
                IDENTIFIED BY '%s';" """
             % (root_pass, schema_name, username, password))
