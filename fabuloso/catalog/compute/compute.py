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
from fabric.api import settings, sudo, puts
from cuisine import package_ensure, package_clean, dir_exists, dir_remove

import fabuloso.utils as utils

PAGE_SIZE = 2 * 1024 * 1024
BONUS_PAGES = 40

NOVA_COMPUTE_CONF = '/etc/nova/nova-compute.conf'

DEFAULT_LIBVIRT_BIN_CONF = '/etc/default/libvirt-bin'

LIBVIRT_BIN_CONF = '/etc/init/libvirt-bin.conf'

LIBVIRTD_CONF = '/etc/libvirt/libvirtd.conf'

LIBVIRT_QEMU_CONF = '/etc/libvirt/qemu.conf'

COMPUTE_API_PASTE_CONF = '/etc/nova/api-paste.ini'

QUANTUM_API_PASTE_CONF = '/etc/quantum/api-paste.ini'

OVS_PLUGIN_CONF = '/etc/quantum/plugins/openvswitch/ovs_quantum_plugin.ini'

QUANTUM_CONF = '/etc/quantum/quantum.conf'

NOVA_INSTANCES = '/var/lib/nova/instances'


def stop():
    with settings(warn_only=True):
        openvswitch_stop()
        quantum_plugin_openvswitch_agent_stop()
        ntp_stop()
        compute_stop()
        iscsi_initiator_stop()


def start():
    stop()
    ntp_start()
    iscsi_initiator_start()
    openvswitch_start()
    quantum_plugin_openvswitch_agent_start()
    compute_start()


def openvswitch_stop():
    with settings(warn_only=True):
        sudo("/etc/init.d/openvswitch-switch stop")


def openvswitch_start():
    openvswitch_stop()
    sudo("/etc/init.d/openvswitch-switch start")


def quantum_plugin_openvswitch_agent_stop():
    with settings(warn_only=True):
        sudo("service quantum-plugin-openvswitch-agent stop")


def quantum_plugin_openvswitch_agent_start():
    quantum_plugin_openvswitch_agent_stop()
    sudo("service quantum-plugin-openvswitch-agent start")


def ntp_stop():
    with settings(warn_only=True):
        sudo("service ntp stop")


def ntp_start():
    ntp_stop()
    sudo("service ntp start")


def iscsi_initiator_stop():
    with settings(warn_only=True):
        sudo("nohup service open-iscsi stop")


def iscsi_initiator_start():
    iscsi_initiator_stop()
    sudo("nohup service open-iscsi start")


def compute_stop():
    with settings(warn_only=True):
        sudo("nohup service libvirt-bin stop")
    with settings(warn_only=True):
        sudo("nohup service nova-api-metadata stop")
    with settings(warn_only=True):
        sudo("nohup service nova-compute stop")


def compute_start():
    compute_stop()
    with settings(warn_only=True):
        sudo("nohup service nova-api-metadata start")
    sudo("nohup service libvirt-bin start")
    sudo("nohup service nova-compute start")


def configure_ubuntu_packages():
    """Configure compute packages"""
    package_ensure('python-software-properties')
    package_ensure('ntp')
    package_ensure('kvm')
    package_ensure('libvirt-bin')
    package_ensure('pm-utils')
    package_ensure('nova-compute-kvm')
    package_ensure('quantum-plugin-openvswitch-agent')
    package_ensure('open-iscsi')


def uninstall_ubuntu_packages():
    """Uninstall compute packages"""
    package_clean('python-software-properties')
    package_clean('ntp')
    package_clean('kvm')
    package_clean('libvirt-bin')
    package_clean('pm-utils')
    package_clean('nova-compute-kvm')
    package_clean('quantum-plugin-openvswitch-agent')
    package_clean('open-iscsi')


def install(cluster=False):
    """Generate compute configuration. Execute on both servers"""
    configure_ubuntu_packages()
    if cluster:
        stop()
    sudo('update-rc.d quantum-plugin-openvswitch-agent defaults 98 02')
    sudo('update-rc.d nova-compute defaults 98 02')


def configure_network():
    sudo("sed -i -r 's/^\s*#(net\.ipv4\.ip_forward=1.*)/\\1/' "
         "/etc/sysctl.conf")
    sudo("echo 1 > /proc/sys/net/ipv4/ip_forward")


def configure_ntp(host='ntp.ubuntu.com'):
    sudo('echo "server %s" > /etc/ntp.conf' % host)


def configure_vhost_net():
    sudo('modprobe vhost-net')
    sudo("sed -i '/modprobe vhost-net/d' /etc/rc.local")
    sudo("sed -i '/exit 0/d' /etc/rc.local")
    sudo("echo 'modprobe vhost-net' >> /etc/rc.local")
    sudo("echo 'exit 0' >> /etc/rc.local")


def configure_libvirt(hostname, shared_storage=False,
                      instances_path='/var/lib/nova/instances'):
    utils.uncomment_property(LIBVIRT_QEMU_CONF, 'cgroup_device_acl')
    utils.modify_property(LIBVIRT_QEMU_CONF,
                          'cgroup_device_acl',
                          '["/dev/null", "/dev/full", "/dev/zero", '
                          '"/dev/random", "/dev/urandom", "/dev/ptmx", '
                          '"/dev/kvm", "/dev/kqemu", "/dev/rtc", "/dev/hpet"'
                          ',"/dev/net/tun"]')
    utils.uncomment_property(LIBVIRTD_CONF, 'listen_tls')
    utils.uncomment_property(LIBVIRTD_CONF, 'listen_tcp')
    utils.uncomment_property(LIBVIRTD_CONF, 'auth_tcp')
    utils.modify_property(LIBVIRTD_CONF, 'listen_tls', '0')
    utils.modify_property(LIBVIRTD_CONF, 'listen_tcp', '1')
    utils.modify_property(LIBVIRTD_CONF, 'auth_tcp', '"none"')
    utils.modify_property(LIBVIRT_BIN_CONF, 'env libvirtd_opts', '"-d -l"')
    utils.modify_property(DEFAULT_LIBVIRT_BIN_CONF, 'libvirtd_opts', '"-d -l"')
    with settings(warn_only=True):
        sudo('virsh net-destroy default')
        sudo('virsh net-undefine default')

    compute_stop()
    # share libvirt configuration to restore compute nodes
    if shared_storage:
        path = '%s/libvirt/%s' % (instances_path, hostname)
        if not dir_exists(path):
            sudo('mkdir -p %s' % path)
            sudo('cp -fR /etc/libvirt/* %s/' % path)
        dir_remove('/etc/libvirt')
        sudo('ln -s %s /etc/libvirt' % path)
    compute_start()


def set_config_file(user,  password, auth_host, auth_port,
                    auth_protocol, admin_auth_url, quantum_url,
                    mysql_username, mysql_password, glance_host,
                    management_ip, glance_port, rabbit_host,
                    libvirt_type, vncproxy_host,
                    mysql_schema='nova',
                    mysql_host='127.0.0.1', tenant='service',
                    mysql_port='3306',
                    rabbit_password='guest',
                    vncproxy_port='6080'):

    if management_ip is None:
        puts("{error:'Management IP of the node needed as argument'}")
        exit(0)

    utils.set_option(COMPUTE_API_PASTE_CONF, 'admin_tenant_name',
                     tenant, section='filter:authtoken')
    utils.set_option(COMPUTE_API_PASTE_CONF, 'admin_user',
                     user, section='filter:authtoken')
    utils.set_option(COMPUTE_API_PASTE_CONF, 'admin_password',
                     password, section='filter:authtoken')
    utils.set_option(COMPUTE_API_PASTE_CONF, 'auth_host', auth_host,
                     section='filter:authtoken')
    utils.set_option(COMPUTE_API_PASTE_CONF, 'auth_port', auth_port,
                     section='filter:authtoken')
    utils.set_option(COMPUTE_API_PASTE_CONF, 'auth_protocol',
                     auth_protocol, section='filter:authtoken')

    utils.set_option(NOVA_COMPUTE_CONF, 'sql_connection',
                     utils.sql_connect_string(mysql_host, mysql_password,
                                              mysql_port, mysql_schema,
                                              mysql_username))

    utils.set_option(NOVA_COMPUTE_CONF, 'verbose', 'true')
    utils.set_option(NOVA_COMPUTE_CONF, 'auth_strategy', 'keystone')
    utils.set_option(NOVA_COMPUTE_CONF, 'use_deprecated_auth', 'false')
    utils.set_option(NOVA_COMPUTE_CONF, 'logdir', '/var/log/nova')
    utils.set_option(NOVA_COMPUTE_CONF, 'state_path', '/var/lib/nova')
    utils.set_option(NOVA_COMPUTE_CONF, 'lock_path', '/var/lock/nova')
    utils.set_option(NOVA_COMPUTE_CONF, 'root_helper',
                     'sudo nova-rootwrap /etc/nova/rootwrap.conf')
    utils.set_option(NOVA_COMPUTE_CONF, 'verbose', 'true')
    utils.set_option(NOVA_COMPUTE_CONF, 'notification_driver',
                     'nova.openstack.common.notifier.rabbit_notifier')
    utils.set_option(NOVA_COMPUTE_CONF, 'notification_topics',
                     'notifications,monitor')
    utils.set_option(NOVA_COMPUTE_CONF, 'default_notification_level', 'INFO')
    utils.set_option(NOVA_COMPUTE_CONF, 'my_ip', management_ip)

    utils.set_option(NOVA_COMPUTE_CONF, 'connection_type', 'libvirt')
    utils.set_option(NOVA_COMPUTE_CONF, 'libvirt_type', libvirt_type)
    utils.set_option(NOVA_COMPUTE_CONF, 'libvirt_ovs_bridge', 'br-int')
    utils.set_option(NOVA_COMPUTE_CONF, 'libvirt_vif_type', 'ethernet')
    utils.set_option(NOVA_COMPUTE_CONF, 'libvirt_vif_driver',
                     'nova.virt.libvirt.vif.LibvirtHybridOVSBridgeDriver')
    utils.set_option(NOVA_COMPUTE_CONF, 'libvirt_use_virtio_for_bridges',
                     'true')
    utils.set_option(NOVA_COMPUTE_CONF, 'start_guests_on_host_boot',
                     'false')
    utils.set_option(NOVA_COMPUTE_CONF, 'resume_guests_state_on_host_boot',
                     'false')

    utils.set_option(NOVA_COMPUTE_CONF, 'quantum_auth_strategy',
                     'keystone')
    utils.set_option(NOVA_COMPUTE_CONF, 'quantum_admin_username',
                     'quantum')
    utils.set_option(NOVA_COMPUTE_CONF, 'quantum_admin_password',
                     'stackops')
    utils.set_option(NOVA_COMPUTE_CONF, 'quantum_admin_tenant_name',
                     'service')

    utils.set_option(NOVA_COMPUTE_CONF, 'quantum_admin_auth_url',
                     admin_auth_url)
    utils.set_option(NOVA_COMPUTE_CONF, 'quantum_url',
                     quantum_url)

    utils.set_option(NOVA_COMPUTE_CONF, 'novncproxy_base_url',
                     'http://%s:%s/vnc_auto.html'
                     % (vncproxy_host, vncproxy_port))
    utils.set_option(NOVA_COMPUTE_CONF, 'vncserver_listen', '0.0.0.0')
    utils.set_option(NOVA_COMPUTE_CONF, 'novnc_enable', 'true')
    utils.set_option(NOVA_COMPUTE_CONF, 'vncserver_proxyclient_address',
                     management_ip)

    utils.set_option(NOVA_COMPUTE_CONF, 'compute_driver',
                     'libvirt.LibvirtDriver')

    utils.set_option(NOVA_COMPUTE_CONF, 'image_service',
                     'nova.image.glance.GlanceImageService')
    utils.set_option(NOVA_COMPUTE_CONF, 'glance_api_servers',
                     '%s:%s' % (glance_host, glance_port))

    utils.set_option(NOVA_COMPUTE_CONF, 'rabbit_host', rabbit_host)
    utils.set_option(NOVA_COMPUTE_CONF, 'rabbit_password', rabbit_password)

    utils.set_option(NOVA_COMPUTE_CONF, 'ec2_private_dns_show_ip', 'True')
    utils.set_option(NOVA_COMPUTE_CONF, 'enabled_apis',
                     'ec2,osapi_compute,metadata')
    utils.set_option(NOVA_COMPUTE_CONF, 'network_api_class',
                     'nova.network.quantumv2.api.API')
    utils.set_option(NOVA_COMPUTE_CONF, 'dmz_cidr', '169.254.169.254/32')
    utils.set_option(NOVA_COMPUTE_CONF, 'metadata_listen', '0.0.0.0')
    utils.set_option(NOVA_COMPUTE_CONF, 'volume_api_class',
                     'nova.volume.cinder.API')
    utils.set_option(NOVA_COMPUTE_CONF, 'cinder_catalog_info',
                     'volume:cinder:internalURL')

    utils.set_option(NOVA_COMPUTE_CONF, 'allow_same_net_traffic',
                     'True')

    start()


def configure_quantum(rabbit_password='guest', rabbit_host='127.0.0.1'):
    utils.set_option(QUANTUM_CONF, 'core_plugin',
                     'quantum.plugins.openvswitch.ovs_quantum_plugin.'
                     'OVSQuantumPluginV2')
    utils.set_option(QUANTUM_CONF, 'auth_strategy', 'keystone')
    utils.set_option(QUANTUM_CONF, 'fake_rabbit', 'False')
    utils.set_option(QUANTUM_CONF, 'rabbit_password', rabbit_password)
    utils.set_option(QUANTUM_CONF, 'rabbit_host', rabbit_host)
    utils.set_option(QUANTUM_CONF, 'notification_driver',
                     'nova.openstack.common.notifier.rabbit_notifier')
    utils.set_option(QUANTUM_CONF, 'notification_topics',
                     'notifications,monitor')
    utils.set_option(QUANTUM_CONF, 'default_notification_level', 'INFO')
    quantum_plugin_openvswitch_agent_start()


def configure_ovs_plugin_gre(mysql_username='quantum',
                             mysql_password='stackops',
                             mysql_host='127.0.0.1', mysql_port='3306',
                             mysql_schema='quantum'):
    utils.set_option(OVS_PLUGIN_CONF, 'sql_connection',
                     utils.sql_connect_string(mysql_host, mysql_password,
                                              mysql_port, mysql_schema,
                                              mysql_username),
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'reconnect_interval', '2',
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'tenant_network_type', 'gre',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'tunnel_id_ranges', '1:1000',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'integration_bridge', 'br-int',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'tunnel_bridge', 'br-tun',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'enable_tunneling', 'True',
                     section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'root_helper',
                     'sudo /usr/bin/quantum-rootwrap '
                     '/etc/quantum/rootwrap.conf', section='AGENT')
    with settings(warn_only=True):
        sudo('ovs-vsctl del-br br-int')
    sudo('ovs-vsctl add-br br-int')
    openvswitch_start()
    quantum_plugin_openvswitch_agent_start()


def configure_ovs_plugin_vlan(iface_bridge='eth1', br_postfix='eth1',
                              vlan_start='2',
                              vlan_end='4094', mysql_quantum_username='quantum',
                              mysql_quantum_password='stackops',
                              mysql_host='127.0.0.1',
                              mysql_port='3306', mysql_schema='quantum'):
    utils.set_option(OVS_PLUGIN_CONF, 'sql_connection',
                     utils.sql_connect_string(mysql_host,
                                              mysql_quantum_password,
                                              mysql_port, mysql_schema,
                                              mysql_quantum_username),
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'reconnect_interval', '2',
                     section='DATABASE')
    utils.set_option(OVS_PLUGIN_CONF, 'tenant_network_type',
                     'vlan', section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'network_vlan_ranges', 'physnet1:%s:%s'
                     % (vlan_start, vlan_end), section='OVS')
    utils.set_option(OVS_PLUGIN_CONF, 'bridge_mappings', 'physnet1:br-%s'
                     % iface_bridge, section='OVS')
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


def get_memory_available():
    return 1024 * int(sudo("cat /proc/meminfo | grep 'MemTotal' | "
                           "sed 's/[^0-9\.]//g'"))


def configure_hugepages(is_enabled=True, percentage='70'):
    ''' enable/disable huge pages in the system'''
    sudo("sed -i '/hugepages/d' /etc/apparmor.d/abstractions/libvirt-qemu")
    sudo('sed -i /hugetlbfs/d /etc/fstab')
    sudo("sed -i '/hugepages/d' "
         "/usr/share/pyshared/nova/virt/libvirt.xml.template")
    with settings(warn_only=True):
        sudo('rm etc/sysctl.d/60-hugepages.conf')
        sudo('umount /dev/hugepages')
    if is_enabled:
        pages = int(0.01 * int(percentage) *
                    int(get_memory_available() / PAGE_SIZE)) + BONUS_PAGES
        sudo("echo '  owner /dev/hugepages/libvirt/qemu/* rw,' >> "
             "/etc/apparmor.d/abstractions/libvirt-qemu")
        sudo('mkdir /dev/hugepages')
        sudo('echo "hugetlbfs       /dev/hugepages  hugetlbfs     '
             'defaults        0 0\n" >> /etc/fstab')
        sudo('mount -t hugetlbfs hugetlbfs /dev/hugepages')
        sudo('echo "vm.nr_hugepages = %s" > /etc/sysctl.d/60-hugepages.conf'
             % pages)
        sudo('sysctl vm.nr_hugepages=%s' % pages)
        sudo("sysctl -p /etc/sysctl.conf")

        # modify libvirt template to enable hugepages
        sudo("sed -i 's#</domain>#\\t<memoryBacking><hugepages/>"
             "</memoryBacking>\\n</domain>#g' "
             "/usr/share/pyshared/nova/virt/libvirt.xml.template")


def configure_nfs_storage(endpoint, delete_content=False, set_nova_owner=True,
                          endpoint_params='defaults'):
    package_ensure('nfs-common')
    if delete_content:
        sudo('rm -fr %s' % NOVA_INSTANCES)
    stop()
    sudo('mkdir -p %s' % NOVA_INSTANCES)
    mpoint = '%s %s nfs %s 0 0' % (endpoint, NOVA_INSTANCES, endpoint_params)
    sudo('sed -i "#%s#d" /etc/fstab' % NOVA_INSTANCES)
    sudo('echo "\n%s" >> /etc/fstab' % mpoint)
    sudo('mount -a')
    if set_nova_owner:
        sudo('chown nova:nova -R %s' % NOVA_INSTANCES)
    start()


def configure_local_storage(delete_content=False, set_nova_owner=True):
    if delete_content:
        sudo('rm -fr %s' % NOVA_INSTANCES)
    stop()
    sudo('sed -i "#%s#d" /etc/fstab' % NOVA_INSTANCES)
    sudo('mkdir -p %s' % NOVA_INSTANCES)
    if set_nova_owner:
        sudo('chown nova:nova -R %s' % NOVA_INSTANCES)
    start()
