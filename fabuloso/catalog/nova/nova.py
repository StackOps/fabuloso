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
from fabric.api import settings, sudo, put, get, local, puts
from cuisine import package_clean, package_ensure


import uuid

CONFIG_FILE = '/etc/nova/nova.conf'


def api_stop():
    with settings(warn_only=True):
        sudo("nohup service nova-api stop")


def api_start():
    api_stop()
    sudo("nohup service nova-api start")


def scheduler_stop():
    with settings(warn_only=True):
        sudo("nohup service nova-scheduler stop")


def scheduler_start():
    scheduler_stop()
    sudo("nohup service nova-scheduler start")


def cert_stop():
    with settings(warn_only=True):
        sudo("nohup service nova-cert stop")


def cert_start():
    cert_stop()
    sudo("nohup service nova-cert start")


def novncproxy_stop():
    with settings(warn_only=True):
        sudo("nohup service nova-novncproxy stop")


def novncproxy_start():
    novncproxy_stop()
    sudo("nohup service nova-novncproxy start")


def console_stop():
    with settings(warn_only=True):
        sudo("nohup service nova-console stop")


def console_start():
    console_stop()
    sudo("nohup service nova-console start")


def consoleauth_stop():
    with settings(warn_only=True):
        sudo("nohup service nova-consoleauth stop")


def consoleauth_start():
    consoleauth_stop()
    sudo("nohup service nova-consoleauth start")


def stop():
    api_stop()
    scheduler_stop()
    novncproxy_stop()
    cert_stop()
    console_stop()
    consoleauth_stop()


def start():
    api_start()
    scheduler_start()
    novncproxy_start()
    cert_start()
    console_start()
    consoleauth_start()


def uninstall_ubuntu_packages():
    """Uninstall nova packages"""
    package_clean('nova-api')
    package_clean('nova-cert')
    package_clean('nova-common')
    package_clean('nova-scheduler')
    package_clean('nova-console')
    package_clean('python-nova')
    package_clean('python-novaclient')
    package_clean('nova-consoleauth')
    package_clean('novnc')
    package_clean('nova-novncproxy')


def install(cluster=False):
    """Generate nova configuration. Execute on both servers"""
    package_ensure('nova-api')
    package_ensure('nova-cert')
    package_ensure('nova-common')
    package_ensure('nova-scheduler')
    package_ensure('nova-console')
    package_ensure('python-nova')
    package_ensure('python-novaclient')
    package_ensure('nova-consoleauth')
    package_ensure('novnc')
    package_ensure('nova-novncproxy')
    if cluster:
        stop()
        sudo('echo "manual" >> /etc/init/nova-api.override')
        sudo('echo "manual" >> /etc/init/nova-novncproxy.override')
        sudo('echo "manual" >> /etc/init/nova-cert.override')
        sudo('echo "manual" >> /etc/init/nova-consoleauth.override')
        sudo('echo "manual" >> /etc/init/nova-scheduler.override')
        sudo('mkdir -p /usr/lib/ocf/resource.d/openstack')
        put('./ocf/nova-novnc', '/usr/lib/ocf/resource.d/openstack/nova-novnc',
            use_sudo=True)
        put('./ocf/nova-api', '/usr/lib/ocf/resource.d/openstack/nova-api',
            use_sudo=True)
        put('./ocf/nova-cert', '/usr/lib/ocf/resource.d/openstack/nova-cert',
            use_sudo=True)
        put('./ocf/nova-consoleauth',
            '/usr/lib/ocf/resource.d/openstack/nova-consoleauth',
            use_sudo=True)
        put('./ocf/nova-scheduler',
            '/usr/lib/ocf/resource.d/openstack/nova-scheduler',
            use_sudo=True)
        sudo('chmod +x /usr/lib/ocf/resource.d/openstack/nova-*')


def sql_connect_string(host, password, port, schema, username):
    sql_connection = 'mysql://%s:%s@%s:%s/%s' % (username, password, host,
                                                 port, schema)
    return sql_connection


def set_config_file(user, password, auth_host,
                    auth_port, auth_protocol, management_ip,
                    mysql_username, mysql_password,
                    mysql_schema='nova',
                    tenant='service', mysql_host='127.0.0.1',
                    mysql_port='3306'):

    f = '/etc/nova/api-paste.ini'
    sudo('sed -i "/volume/d" %s' % f)
    sudo("sed -i 's/admin_password.*$/admin_password = %s/g' %s"
         % (password, f))
    sudo("sed -i 's/admin_tenant_name.*$/admin_tenant_name = %s/g' %s"
         % (tenant, f))
    sudo("sed -i 's/admin_user.*$/admin_user = %s/g' %s"
         % (user, f))
    sudo("sed -i 's/auth_host.*$/auth_host = %s/g' %s"
         % (auth_host, f))
    sudo("sed -i 's/auth_port.*$/auth_port = %s/g' %s"
         % (auth_port, f))
    sudo("sed -i 's/auth_protocol.*$/auth_protocol = %s/g' %s"
         % (auth_protocol, f))

    if management_ip is None:
        puts("{error:'Management IP of the node needed as argument'}")
        exit(0)

    set_property('sql_connection', sql_connect_string(mysql_host,
                 mysql_password, mysql_port, mysql_schema, mysql_username))
    set_property('scheduler_driver', 'nova.scheduler.simple.SimpleScheduler')
    set_property('auth_strategy', 'keystone')
    set_property('allow_admin_api', 'true')
    set_property('use_deprecated_auth', 'false')
    set_property('ec2_private_dns_show_ip', 'True')
    set_property('api_paste_config', '/etc/nova/api-paste.ini')
    set_property('enabled_apis', 'ec2,osapi_compute,metadata')
    set_property('network_api_class', 'nova.network.quantumv2.api.API')
    set_property('dmz_cidr', '169.254.169.254/32')
    set_property('metadata_listen', '0.0.0.0')
    set_property('quantum_auth_strategy', 'keystone')
    set_property('quantum_admin_username', 'quantum')
    set_property('quantum_admin_password', 'stackops')
    set_property('quantum_admin_tenant_name', 'service')
    set_property('libvirt_vif_driver',
                 'nova.virt.libvirt.vif.LibvirtHybridOVSBridgeDriver')
    set_property('libvirt_volume_drivers',
                 '"iscsi=nova.virt.libvirt.volume.LibvirtISCSIVolumeDriver, '
                 'local=nova.virt.libvirt.volume.LibvirtVolumeDriver, '
                 'fake=nova.virt.libvirt.volume.LibvirtFakeVolumeDriver, '
                 'rbd=nova.virt.libvirt.volume.LibvirtNetVolumeDriver, '
                 'sheepdog=nova.virt.libvirt.volume.LibvirtNetVolumeDriver, '
                 'nfs=nova.virt.libvirt.volume_nfs.NfsVolumeDriver"')
    set_property('linuxnet_interface_driver',
                 'nova.network.linux_net.LinuxOVSInterfaceDriver')
    set_property('firewall_driver',
                 'nova.virt.libvirt.firewall.IptablesFirewallDriver')
    set_property('volume_api_class', 'nova.volume.cinder.API')
    set_property('cinder_catalog_info', 'volume:cinder:internalURL')
    set_property('image_service', 'nova.image.glance.GlanceImageService')
    set_property('novnc_enable', 'true')
    set_property('vncserver_listen', '0.0.0.0')
    set_property('logdir', '/var/log/nova')
    set_property('state_path', '/var/lib/nova')
    set_property('lock_path', '/var/lock/nova')
    set_property('root_helper', 'sudo nova-rootwrap /etc/nova/rootwrap.conf')
    set_property('verbose', 'true')
    set_property('notification_driver',
                 'nova.openstack.common.notifier.rabbit_notifier')
    set_property('notification_topics', 'notifications,monitor')
    set_property('default_notification_level', 'INFO')
    set_property('my_ip', management_ip)
    # Quotas
    set_property('quota_instances', '4096')
    set_property('quota_cores', '8192')
    set_property('quota_ram', str(1024 * 1024 * 20))
    set_property('quota_volumes', '8192')
    set_property('quota_gigabytes', str(1024 * 20))
    set_property('quota_floating_ips', '254')
    set_property('quota_metadata_items', '128')
    set_property('quota_max_injected_files', '5')
    set_property('quota_max_injected_file_content_bytes', str(10 * 1024))
    set_property('quota_max_injected_file_path_bytes', '255')
    set_property('quota_key_pairs,', '100')
    set_property('quota_security_group_rules', '20')
    set_property('quota_security_groups', '10')
    # NOVA-SCHEDULER configruration
    set_property('max_cores', '16')
    set_property('max_gigabytes', '2048')  # 2TB
    set_property('max_networks', '1000')
    sudo('nova-manage db sync')


def set_property(name, value, comment=None):
    delete_property(name)
    comm = ''
    if comment is not None:
        comm = '# %s' % comment
    sudo('echo "%s=%s       %s" >> %s' % (name, value, comm, CONFIG_FILE))


def nova_properties(props):
    for key, value in props.items():
        set_property(key, value)


def get_property(name):
    sudo('''sed '/^\#/d' %s | grep "%s"  | tail -n 1 | sed 's/^.*=//' '''
         % (name, CONFIG_FILE))


def get_properties():
    temp_file = "/tmp/%s" % uuid.uuid1()
    sudo("cp %s %s" % (CONFIG_FILE, temp_file))
    sudo("chmod 666 %s" % temp_file)
    local_file = "/tmp/%s" % uuid.uuid1()
    get(temp_file, local_file)
    sudo('rm -f %s' % temp_file)
    d = {}
    for line in open(local_file):
        try:
            x = line.strip().split('=')
            if len(x) > 1:
                tokens = line.split('=')
                d[tokens[0]] = '='.join(tokens[1:])
        except:
            pass
    local('rm -f %s' % local_file)
    puts(d)


def delete_property(name):
    sudo('sed -i "/^%s=/d" %s' % (name, CONFIG_FILE))
