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
from fabric.api import task, settings, sudo, puts, local
from cuisine import package_ensure, package_clean

import fabuloso.utils as utils

QUANTUM_API_PASTE_CONF = '/etc/quantum/api-paste.ini'

DHCP_AGENT_CONF = '/etc/quantum/dhcp_agent.ini'

L3_AGENT_CONF = '/etc/quantum/l3_agent.ini'

OVS_PLUGIN_CONF = '/etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini'

QUANTUM_CONF = '/etc/quantum/quantum.conf'


@task
def openvswitch_stop():
    with settings(warn_only=True):
        sudo("/etc/init.d/openvswitch-switch stop")


@task
def openvswitch_start():
    openvswitch_stop()
    sudo("/etc/init.d/openvswitch-switch start")


@task
def quantum_plugin_openvswitch_agent_stop():
    with settings(warn_only=True):
        sudo("service quantum-plugin-openvswitch-agent stop")


@task
def quantum_plugin_openvswitch_agent_start():
    quantum_plugin_openvswitch_agent_stop()
    sudo("service quantum-plugin-openvswitch-agent start")


@task
def quantum_dhcp_agent_stop():
    with settings(warn_only=True):
        sudo("service quantum-dhcp-agent stop")


@task
def quantum_dhcp_agent_start():
    quantum_dhcp_agent_stop()
    sudo("service quantum-dhcp-agent start")


@task
def quantum_l3_agent_stop():
    with settings(warn_only=True):
        sudo("service quantum-l3-agent stop")


@task
def quantum_l3_agent_start():
    quantum_l3_agent_stop()
    sudo("service quantum-l3-agent start")


@task
def stop():
    openvswitch_stop()
    quantum_plugin_openvswitch_agent_stop()
    quantum_dhcp_agent_stop()
    quantum_l3_agent_stop()


@task
def start():
    openvswitch_start()
    quantum_plugin_openvswitch_agent_start()
    quantum_dhcp_agent_start()
    quantum_l3_agent_start()


@task
def compile_datapath():
    package_ensure('openvswitch-datapath-source')
    sudo('DEBIAN_FRONTEND=noninteractive module-assistant -fi '
         'auto-install openvswitch-datapath')


@task
def configure_ubuntu_packages():
    """Configure openvwsitch and quantum packages"""
    package_ensure('vlan')
    package_ensure('bridge-utils')
    package_ensure('python-cliff')
    package_ensure('openvswitch-datapath-dkms')
    package_ensure('openvswitch-switch')
    package_ensure('quantum-plugin-openvswitch-agent')
    package_ensure('quantum-l3-agent')
    package_ensure('quantum-dhcp-agent')
    package_ensure('python-pyparsing')
    package_ensure('python-mysqldb')


@task
def uninstall_ubuntu_packages():
    """Uninstall openvswitch and quantum packages"""
    package_clean('openvswitch-datapath-dkms')
    package_clean('openvswitch-switch')
    package_clean('python-cliff')
    package_clean('quantum-plugin-openvswitch-agent')
    package_clean('quantum-l3-agent')
    package_clean('quantum-dhcp-agent')
    package_clean('python-pyparsing')
    package_clean('python-mysqldb')
    package_clean('vlan')
    package_clean('bridge-utils')


@task
def configure_network():
    sudo("sed -i -r 's/^\s*#(net\.ipv4\.ip_forward=1.*)/\\1/' "
         "/etc/sysctl.conf")
    sudo("echo 1 > /proc/sys/net/ipv4/ip_forward")


@task
def install(cluster=False, iface_ex=None):
    """Generate quantum configuration. Execute on both servers"""
    if iface_ex is None:
        puts("{'error':'You need to pass the physical interface as argument "
             "of the external bridge'}")
        return
    configure_ubuntu_packages()
    if cluster:
        stop()
    configure_network()
    openvswitch_start()
    with settings(warn_only=True):
        sudo('ovs-vsctl del-br br-ex')
    sudo('ovs-vsctl add-br br-ex')
    sudo('ovs-vsctl add-port br-ex %s' % iface_ex)
    sudo('update-rc.d quantum-dhcp-agent defaults 98 02')
    sudo('update-rc.d quantum-l3-agent defaults 98 02')
    sudo('update-rc.d quantum-plugin-openvswitch-agent defaults 98 02')


@task
def configure_ovs_plugin_gre(ip_tunnel='127.0.0.1', tunnel_start='1',
                             tunnel_end='1000', mysql_username='quantum',
                             mysql_password='stackops', mysql_host='127.0.0.1',
                             mysql_port='3306', mysql_schema='quantum'):
    utils.set_option(OVS_PLUGIN_CONF, 'sql_connection',
                     utils.sql_connect_string(mysql_host, mysql_password,
                                              mysql_port, mysql_schema,
                                              mysql_username),
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'reconnect_interval', '2',
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'tenant_network_type', 'gre',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'tunnel_id_ranges',
                     '%s:%s' % (tunnel_start, tunnel_end), section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'local_ip', ip_tunnel)
    utils.set_option(OVS_PLUGIN_CONF, 'integration_bridge', 'br-int',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'tunnel_bridge', 'br-tun', section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'enable_tunneling', 'True',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'root_helper',
                     'sudo /usr/bin/quantum-rootwrap '
                     '/etc/quantum/rootwrap.conf',
                     section='AGENT')
    with settings(warn_only=True):
        sudo('ovs-vsctl del-br br-int')
    sudo('ovs-vsctl add-br br-int')
    openvswitch_start()
    quantum_plugin_openvswitch_agent_start()


@task
def configure_ovs_plugin_vlan(iface_bridge='eth1', br_postfix='eth1',
                              vlan_start='1', vlan_end='4094',
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
    utils.set_option(OVS_PLUGIN_CONF, 'tenant_network_type',
                     'vlan', section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'network_vlan_ranges', 'physnet1:%s:%s'
                     % (vlan_start, vlan_end), section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'bridge_mappings',
                     'physnet1:br-%s' % iface_bridge, section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'root_helper',
                     'sudo /usr/bin/quantum-rootwrap '
                     '/etc/quantum/rootwrap.conf', section='AGENT')
    with settings(warn_only=True):
        sudo('ovs-vsctl del-br br-int')
    sudo('ovs-vsctl add-br br-int')
    with settings(warn_only=True):
        sudo('ovs-vsctl del-br br-%s' % br_postfix)
    sudo('ovs-vsctl add-br br-%s' % br_postfix)
    sudo('ovs-vsctl add-port br-%s %s' % (br_postfix, iface_bridge))
    openvswitch_start()
    quantum_plugin_openvswitch_agent_start()


@task
def configure_l3_agent(user, password, auth_url, management_ip,
                       region, tenant='service'):
    utils.set_option(L3_AGENT_CONF, 'debug', 'True')
    utils.set_option(L3_AGENT_CONF, 'interface_driver',
                     'quantum.agent.linux.interface.OVSInterfaceDriver')
    utils.set_option(L3_AGENT_CONF, 'auth_url', auth_url)
    utils.set_option(L3_AGENT_CONF, 'auth_region', region)
    utils.set_option(L3_AGENT_CONF, 'admin_tenant_name', tenant)
    utils.set_option(L3_AGENT_CONF, 'admin_user', user)
    utils.set_option(L3_AGENT_CONF, 'admin_password', password)
    utils.set_option(L3_AGENT_CONF, 'root_helper',
                     'sudo quantum-rootwrap /etc/quantum/rootwrap.conf')
    utils.set_option(L3_AGENT_CONF, 'metadata_ip', management_ip)
    utils.set_option(L3_AGENT_CONF, 'use_namespaces', 'False')


@task
def configure_dhcp_agent(name_server='8.8.8.8'):
    utils.set_option(DHCP_AGENT_CONF, 'use_namespaces', 'False')
    utils.set_option(DHCP_AGENT_CONF, 'dnsmasq_dns_server', name_server)


@task
def set_config_file(user, password, auth_host,
                    auth_port, auth_protocol, tenant='service',
                    rabbit_password='guest',
                    rabbit_host='127.0.0.1'):

    utils.set_option(QUANTUM_API_PASTE_CONF, 'admin_tenant_name',
                     tenant, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'admin_user',
                     user, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'admin_password',
                     password, section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'auth_host', auth_host,
                     section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'auth_port', auth_port,
                     section='filter:authtoken')
    utils.set_option(QUANTUM_API_PASTE_CONF, 'auth_protocol', auth_protocol,
                     section='filter:authtoken')
    cp = 'quantum.plugins.openvswitch.ovs_quantum_plugin.OVSQuantumPluginV2'
    utils.set_option(QUANTUM_CONF, 'core_plugin', cp)
    utils.set_option(QUANTUM_CONF, 'auth_strategy', 'keystone')
    utils.set_option(QUANTUM_CONF, 'fake_rabbit', 'False')
    utils.set_option(QUANTUM_CONF, 'rabbit_password', rabbit_password)
    utils.set_option(QUANTUM_CONF, 'rabbit_host', rabbit_host)
    utils.set_option(QUANTUM_CONF, 'notification_driver',
                     'nova.openstack.common.notifier.rabbit_notifier')
    utils.set_option(QUANTUM_CONF, 'notification_topics',
                     'notifications,monitor')
    utils.set_option(QUANTUM_CONF, 'default_notification_level', 'INFO')


def get_net_id(str):
    stdout = local("echo '%s' | awk '/ id / { print $4 }'" % (str,),
                   capture=True)
    puts(stdout)
    return stdout.replace('\n', '')


@task
def configure_external_network(floating_start, floating_end, floating_gw,
                               floating_range, admin_user, admin_tenant_name,
                               admin_pass, auth_url):

    stdout = sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
                  '--os-tenant-name %s net-create ext_net '
                  '--provider:network_type local  --router:external=True'
                  % (auth_url, admin_user, admin_pass, admin_tenant_name))
    external_network_id = get_net_id(stdout)
    sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
         '--os-tenant-name %s subnet-create --ip_version 4 --allocation-pool '
         'start=%s,end=%s --gateway %s %s %s -- --enable_dhcp=False'
         % (auth_url, admin_user, admin_pass, admin_tenant_name,
            floating_start, floating_end, floating_gw,
            external_network_id, floating_range))


@task
def configure_external_bridge(floating_range):
    sudo('ip addr flush dev br-ex')
    sudo('ip addr add %s dev br-ex' % floating_range)
    sudo('ip link set br-ex up')


@task
def configure_private_network(tenant_id, network_name, private_range,
                              private_gw, external_network_id,
                              admin_user='admin', admin_tenant_name='admin',
                              admin_pass='stackops',
                              auth_url='http://localhost:5000/v2.0'):
    stdout = sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
                  '--os-tenant-name %s net-create --tenant_id %s %s'
                  % (auth_url, admin_user, admin_pass, admin_tenant_name,
                     tenant_id, network_name))
    private_network_id = get_net_id(stdout)
    stdout = sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
                  '--os-tenant-name %s subnet-create --tenant_id %s '
                  '--ip_version 4 %s %s --gateway %s'
                  % (auth_url, admin_user, admin_pass, admin_tenant_name,
                     tenant_id, private_network_id, private_range, private_gw))
    private_subnet_id = get_net_id(stdout)
    stdout = sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
                  '--os-tenant-name %s router-create --tenant_id %s '
                  'provider-router'
                  % (auth_url, admin_user, admin_pass, admin_tenant_name,
                     tenant_id))
    router_id = get_net_id(stdout)
    sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
         '--os-tenant-name %s router-interface-add %s %s'
         % (auth_url, admin_user, admin_pass, admin_tenant_name, router_id,
            private_subnet_id))
    sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
         '--os-tenant-name %s router-gateway-set %s %s'
         % (auth_url, admin_user, admin_pass, admin_tenant_name, router_id,
            external_network_id))


@task
def delete_network(network_id, admin_user='admin', admin_tenant_name='admin',
                   admin_pass='stackops',
                   auth_url='http://localhost:5000/v2.0'):
    sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
         '--os-tenant-name %s net-delete %s'
         % (auth_url, admin_user, admin_pass, admin_tenant_name, network_id))


@task
def delete_router(router_id, admin_user='admin', admin_tenant_name='admin',
                  admin_pass='stackops',
                  auth_url='http://localhost:5000/v2.0'):
    sudo('quantum --os-auth-url %s --os-username %s --os-password %s '
         '--os-tenant-name %s router-delete %s'
         % (auth_url, admin_user, admin_pass, admin_tenant_name, router_id))
