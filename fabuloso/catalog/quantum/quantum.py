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

from cuisine import *
from fabric.api import *

import utils

QUANTUM_API_PASTE_CONF = '/etc/quantum/api-paste.ini'

OVS_PLUGIN_CONF = '/etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini'

@task
def quantum_server_stop():
    with settings(warn_only=True):
        sudo("service quantum-server stop")

@task
def quantum_server_start():
    quantum_server_stop()
    sudo("service quantum-server start")

@task
def stop():
    quantum_server_stop()

@task
def start():
    quantum_server_start()

@task
def configure_ubuntu_packages():
    """Configure openvwsitch and quantum packages"""
    package_ensure('quantum-server')
    package_ensure('quantum-plugin-openvswitch')
    package_ensure('python-pyparsing')
    package_ensure('python-mysqldb')

@task
def uninstall_ubuntu_packages():
    """Uninstall openvswitch and quantum packages"""
    package_clean('quantum-server')
    package_clean('quantum-plugin-openvswitch')
    package_clean('python-pyparsing')
    package_clean('python-mysqldb')

@task
def configure(cluster=False):
    """Generate quantum configuration. Execute on both servers"""
    configure_ubuntu_packages()
    if cluster:
        stop()

@task
def configure_ovs_plugin_gre(mysql_username='quantum',
                             mysql_password='stackops', mysql_host='127.0.0.1', mysql_port='3306', mysql_schema='quantum'):
    utils.set_option(OVS_PLUGIN_CONF,'sql_connection',utils.sql_connect_string(mysql_host, mysql_password, mysql_port, mysql_schema, mysql_username),section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF,'reconnect_interval','2',section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF,'tenant_network_type','gre',section='OVS')
    utils.set_option(OVS_PLUGIN_CONF,'tunnel_id_ranges','%s:%s' % (tunnel_start,tunnel_end),section='OVS')
    utils.set_option(OVS_PLUGIN_CONF,'root_helper','sudo /usr/bin/quantum-rootwrap /etc/quantum/rootwrap.conf',section='AGENT')

@task
def configure_ovs_plugin_vlan(vlan_start='1',vlan_end='4094',mysql_username='quantum',
                              mysql_password='stackops', mysql_host='127.0.0.1', mysql_port='3306', mysql_schema='quantum'):
    utils.set_option(OVS_PLUGIN_CONF,'sql_connection',utils.sql_connect_string(mysql_host, mysql_password, mysql_port, mysql_schema, mysql_username),section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF,'reconnect_interval','2',section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF,'tenant_network_type','vlan',section='OVS')
    utils.set_option(OVS_PLUGIN_CONF,'network_vlan_ranges','physnet1:%s:%s' % (vlan_start, vlan_end),section='OVS')
    utils.set_option(OVS_PLUGIN_CONF,'root_helper','sudo /usr/bin/quantum-rootwrap /etc/quantum/rootwrap.conf',section='AGENT')

@task
def configure_files(service_user='quantum', service_tenant_name='service', service_pass='stackops',auth_host='127.0.0.1',
                        auth_port='35357', auth_protocol='http'):
    utils.set_option(QUANTUM_API_PASTE_CONF,'admin_tenant_name',service_tenant_name,section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF,'admin_user',service_user,section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF,'admin_password',service_pass,section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF,'auth_host',auth_host,section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF,'auth_port',auth_port,section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF,'auth_protocol',auth_protocol,section='filter:authtoken')