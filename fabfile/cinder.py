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

from fabric.api import *
from cuisine import *

import utils

CINDER_CONF = '/etc/cinder/cinder.conf'
CINDER_API_PASTE_CONF = '/etc/cinder/api-paste.ini'

@task
def stop():
    with settings(warn_only=True):
        sudo("nohup service cinder-api stop")
        sudo("nohup service cinder-scheduler stop")
        sudo("nohup service cinder-volume stop")

@task
def start():
    stop()
    sudo("nohup service cinder-api start")
    sudo("nohup service cinder-scheduler start")
    sudo("nohup service cinder-volume start")

@task
def iscsi_stop():
    with settings(warn_only=True):
        sudo("nohup service tgt stop")

@task
def iscsi_start():
    iscsi_stop()
    sudo("nohup service tgt start")

@task
def configure_ubuntu_packages():
    """Configure cinder packages"""
    package_ensure('cinder-api')
    package_ensure('cinder-scheduler')
    package_ensure('cinder-volume')
    package_ensure('tgt')
    package_ensure('python-cinderclient')
    package_ensure('python-mysqldb')


@task
def uninstall_ubuntu_packages():
    """Uninstall cinder packages"""
    package_clean('cinder-api')
    package_clean('cinder-scheduler')
    package_clean('cinder-volume')
    package_clean('tgt')
    package_clean('python-cinderclient')
    package_clean('python-mysqldb')

@task
def configure(cluster=False):
    """Generate cinder configuration. Execute on both servers"""
    configure_ubuntu_packages()
    if cluster:
        stop()
    sudo("echo 'include /var/lib/cinder/volumes/*' > /etc/tgt/conf.d/cinder.conf")
    sudo("echo 'include /etc/tgt/conf.d/cinder.conf' > /etc/tgt/targets.conf")

@task
def configure_files(rabbit_password='guest',rabbit_host='localhost',mysql_username='cinder',
                      mysql_password='stackops', mysql_host='127.0.0.1', mysql_port='3306', mysql_schema='cinder', service_user='cinder', service_tenant_name='service', service_pass='stackops',auth_host='127.0.0.1',
                      auth_port='35357', auth_protocol='http'):
    utils.set_option(CINDER_CONF,'rootwrap_config','/etc/cinder/rootwrap.conf')
    utils.set_option(CINDER_CONF,'auth_strategy','keystone')
    utils.set_option(CINDER_CONF,'iscsi_helper','tgtadm')
    utils.set_option(CINDER_CONF,'rabbit_password',rabbit_password)
    utils.set_option(CINDER_CONF,'rabbit_host',rabbit_host)
    utils.set_option(CINDER_CONF,'sql_connection',utils.sql_connect_string(mysql_host, mysql_password, mysql_port, mysql_schema, mysql_username))
    utils.set_option(CINDER_CONF,'verbose','true')
    utils.set_option(CINDER_CONF,'volume_group','cinder-volumes')
    utils.set_option(CINDER_CONF,'log_dir','/var/log/cinder')
    utils.set_option(CINDER_CONF,'notification_driver', 'nova.openstack.common.notifier.rabbit_notifier')
    utils.set_option(CINDER_CONF,'notification_topics', 'notifications,monitor')
    utils.set_option(CINDER_CONF,'default_notification_level', 'INFO')
    utils.set_option(CINDER_API_PASTE_CONF,'admin_tenant_name',service_tenant_name,section='filter:authtoken')
    utils.set_option(CINDER_API_PASTE_CONF,'admin_user',service_user,section='filter:authtoken')
    utils.set_option(CINDER_API_PASTE_CONF,'admin_password',service_pass,section='filter:authtoken')
    utils.set_option(CINDER_API_PASTE_CONF,'auth_host',auth_host,section='filter:authtoken')
    utils.set_option(CINDER_API_PASTE_CONF,'auth_port',auth_port,section='filter:authtoken')
    utils.set_option(CINDER_API_PASTE_CONF,'auth_protocol',auth_protocol,section='filter:authtoken')
    sudo('cinder-manage db sync')
    iscsi_start()
    start()

@task
def create_volume(partition):
    sudo('pvcreate %s' % partition)
    sudo('vgcreate cinder-volumes %s' % partition)
    iscsi_start()
    start()
