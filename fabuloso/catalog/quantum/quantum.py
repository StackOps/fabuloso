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
from fabric.api import settings, sudo
from cuisine import package_clean, package_ensure

import fabuloso.utils as utils

QUANTUM_API_PASTE_CONF = '/etc/quantum/api-paste.ini'

OVS_PLUGIN_CONF = '/etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini'


def quantum_server_stop():
    with settings(warn_only=True):
        sudo("service quantum-server stop")


def quantum_server_start():
    quantum_server_stop()
    sudo("service quantum-server start")


def stop():
    quantum_server_stop()


def start():
    quantum_server_start()


def uninstall_ubuntu_packages():
    """Uninstall openvswitch and quantum packages"""
    package_clean('quantum-server')
    package_clean('quantum-plugin-openvswitch')
    package_clean('python-pyparsing')
    package_clean('python-mysqldb')


def install(cluster=False):
    """Generate quantum configuration. Execute on both servers"""
    """Configure openvwsitch and quantum packages"""
    package_ensure('quantum-server')
    package_ensure('quantum-plugin-openvswitch')
    package_ensure('python-pyparsing')
    package_ensure('python-mysqldb')
    if cluster:
        stop()


def set_config_file(user, password, auth_host,
                    auth_port, auth_protocol, tenant='service'):
    utils.set_option(QUANTUM_API_PASTE_CONF, 'admin_tenant_name',
                     tenant, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'admin_user',
                     user, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'admin_password',
                     password, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'auth_host', auth_host,
                     section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'auth_port',
                     auth_port, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'auth_protocol',
                     auth_protocol, section='filter:authtoken')


def configure_ovs_plugin_vlan(vlan_start='1', vlan_end='4094',
                              mysql_username='quantum',
                              mysql_password='stackops',
                              mysql_host='127.0.0.1',
                              mysql_port='3306', mysql_schema='quantum'):

    utils.set_option(OVS_PLUGIN_CONF, 'sql_connection',
                     utils.sql_connect_string(mysql_host, mysql_password,
                                              mysql_port, mysql_schema,
                                              mysql_username),
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'reconnect_interval', '2',
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'tenant_network_type', 'vlan',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'network_vlan_ranges', 'physnet1:%s:%s'
                     % (vlan_start, vlan_end), section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'root_helper',
                     'sudo /usr/bin/quantum-rootwrap '
                     '/etc/quantum/rootwrap.conf',
                     section='AGENT')
