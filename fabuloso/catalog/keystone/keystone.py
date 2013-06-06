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

from fabric.api import settings, sudo, put, local, puts
from cuisine import package_ensure, package_clean


def stop():
    with settings(warn_only=True):
        sudo("service keystone stop")


def start():
    stop()
    sudo("service keystone start")


def uninstall():
    """Uninstall keystone packages"""
    package_clean('keystone')
    package_clean('python-keystone')
    package_clean('python-keystoneclient')


def install(cluster=False):
    """Generate keystone configuration. Execute on both servers"""
    package_ensure('keystone')
    package_ensure('python-keystone')
    package_ensure('python-keystoneclient')
    package_ensure('python-mysqldb')
    if cluster:
        stop()
        sudo('echo "manual" >> /etc/init/keystone.override')
        sudo('mkdir -p /usr/lib/ocf/resource.d/openstack')
        put('./ocf/keystone', '/usr/lib/ocf/resource.d/openstack/keystone',
            use_sudo=True)
        sudo('chmod +x /usr/lib/ocf/resource.d/openstack/keystone')


def _get_id(str):
    stdout = local("echo '%s' | awk '/ id / { print $4 }'" % str, capture=True)
    puts(stdout)
    return stdout.replace('\n', '')


def _sql_connect_string(host, password, port, schema, username):
    sql_connection = 'mysql://%s:%s@%s:%s/%s' % (username, password, host,
                                                 port, schema)
    return sql_connection


def set_config_file(admin_token, mysql_schema, mysql_username,
                    mysql_password, mysql_host='127.0.0.1',
                    mysql_port='3306'):
    """Configure keystone to use the database and set the default
    admin token password"""
    bind_host = '0.0.0.0'
    public_port = '5000'
    admin_port = '35357'
    sudo("sed -i 's/^.*admin_token =.*$/admin_token = %s/g' "
         "/etc/keystone/keystone.conf" % admin_token)
    sudo("sed -i 's/^# bind_host =.*$/bind_host = %s/g' "
         "/etc/keystone/keystone.conf" % bind_host)
    sudo("sed -i 's/^# public_port =.*$/public_port = %s/g' "
         "/etc/keystone/keystone.conf" % public_port)
    sudo("sed -i 's/^# admin_port =.*$/admin_port = %s/g' "
         "/etc/keystone/keystone.conf" % admin_port)
    sudo("sed -i 's#connection.*$#connection = %s#g' "
         "/etc/keystone/keystone.conf" %
         _sql_connect_string(mysql_host, mysql_password, mysql_port,
                             mysql_schema, mysql_username))
    sudo("service keystone restart")
    sudo("keystone-manage db_sync")


def _link_user_role(endpoint, admin_token, quantum_user, admin_role,
                    service_tenant):
    sudo('keystone --endpoint %s --token %s user-role-add --user-id %s '
         '--role-id %s --tenant-id %s' % (endpoint, admin_token, quantum_user,
                                          admin_role, service_tenant))


def _create_role(endpoint, admin_token, role):
    stdout = sudo('keystone --endpoint %s --token %s role-create --name=%s'
                  % (endpoint, admin_token, role))
    return _get_id(stdout)


def _create_user(endpoint, admin_token, name, password, tenant):
    stdout = sudo(
        'keystone --endpoint %s --token %s user-create --name=%s --pass=%s '
        '--tenant-id %s --email=%s@domain.com' % (endpoint, admin_token, name,
                                                  password, tenant, name))
    return _get_id(stdout)


def _create_tenant(endpoint, admin_token, name):
    stdout = sudo('keystone --endpoint %s --token %s tenant-create --name=%s'
                  % (endpoint, admin_token, name))
    return _get_id(stdout)


def _get_tenant_id(endpoint, admin_token, name):
    stdout = sudo("keystone --endpoint %s --token %s tenant-list | grep '%s' |"
                  " awk '/ | / { print $2 }'" % (endpoint, admin_token, name))
    puts(stdout)
    return stdout.replace('\n', '')


def _get_role_id(endpoint, admin_token, name):
    stdout = sudo("keystone --endpoint %s --token %s role-list | grep '%s' |"
                  " awk '/ | / { print $2 }'" % (endpoint, admin_token, name))
    puts(stdout)
    return stdout.replace('\n', '')


def create_user_for_service(endpoint, service_user_name, admin_token,
                            service_user_pass, tenant):
    """Configure component user and service"""
    service_tenant = _get_tenant_id(endpoint, admin_token, tenant)
    print "Service tenant is" + service_tenant
    admin_role = _get_role_id(endpoint, admin_token, 'admin')
    service_user = _create_user(endpoint, admin_token, service_user_name,
                                service_user_pass, service_tenant)
    _link_user_role(endpoint, admin_token, service_user, admin_role,
                    service_tenant)


def configure_users(endpoint, admin_token, admin_pass, tenant_name):
    """Configure basic service users/roles"""
    admin_tenant = _create_tenant(endpoint, admin_token, 'admin')
    _create_tenant(endpoint, admin_token, tenant_name)
    head_tenant = _create_tenant(endpoint, admin_token, 'head')
    admin_role = _create_role(endpoint, admin_token, 'admin')
    member_role = _create_role(endpoint, admin_token, 'Member')
    keystone_admin_role = _create_role(endpoint, admin_token, 'KeystoneAdmin')
    keystone_service_admin_role = _create_role(endpoint, admin_token,
                                               'KeystoneServiceAdmin')
    portal_admin_role = _create_role(endpoint, admin_token,
                                     'ROLE_PORTAL_ADMIN')
    portal_user_role = _create_role(endpoint, admin_token, 'ROLE_PORTAL_USER')
    activity_admin_role = _create_role(endpoint, admin_token,
                                       'ROLE_ACTIVITY_ADMIN')
    activity_user_role = _create_role(endpoint, admin_token,
                                      'ROLE_ACTIVITY_USER')
    chargeback_admin_role = _create_role(endpoint, admin_token,
                                         'ROLE_CHARGEBACK_ADMIN')
    chargeback_user_role = _create_role(endpoint, admin_token,
                                        'ROLE_CHARGEBACK_USER')
    accounting_user_role = _create_role(endpoint, admin_token,
                                        'ROLE_ACCOUNTING')
    automation_user_role = _create_role(endpoint, admin_token,
                                        'ROLE_HEAD_ADMIN')
    admin_user = _create_user(endpoint, admin_token, 'admin', admin_pass,
                              admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, keystone_admin_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user,
                    keystone_service_admin_role, admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, admin_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, member_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, portal_admin_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, portal_user_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, activity_admin_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, activity_user_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, chargeback_admin_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, chargeback_user_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, accounting_user_role,
                    admin_tenant)
    _link_user_role(endpoint, admin_token, admin_user, automation_user_role,
                    head_tenant)


def create_service(admin_token, service_name, service_type, description,
                   region, endpoint, public_url, internal_url, admin_url):
    """Create a new service"""
    stdout = sudo("keystone --endpoint %s --token %s service-create --name=%s"
                  " --type=%s --description='%s' " % (endpoint, admin_token,
                                                      service_name,
                                                      service_type,
                                                      description))
    service_id = _get_id(stdout)
    sudo("keystone --endpoint %s --token %s endpoint-create --region %s "
         "--service-id %s --publicurl '%s' --adminurl '%s' --internalurl '%s' "
         % (endpoint, admin_token, region, service_id, public_url, admin_url,
            internal_url))


def configure_services(admin_token="password", public_ip='127.0.0.1',
                       public_port='80', internal_ip='127.0.0.1',
                       region='RegionOne'):
    """Configure services and endpoints"""
    endpoint = "'http://localhost:35357/v2.0'"
    create_service(endpoint, admin_token, 'keystone', 'identity',
                   'Keystone Identity Service', region,
                   'http://%s:%s/keystone/v2.0' % (public_ip, public_port),
                   'http://%s:$(admin_port)s/v2.0' % internal_ip,
                   'http://%s:$(public_port)s/v2.0' % internal_ip)
    create_service(endpoint, admin_token, 'nova', 'compute',
                   'Openstack Compute Service', region,
                   'http://%s:%s/compute/v1.1/$(tenant_id)s' % (public_ip,
                                                                public_port),
                   'http://%s:$(compute_port)s/v1.1/$(tenant_id)s'
                   % internal_ip,
                   'http://%s:$(compute_port)s/v1.1/$(tenant_id)s'
                   % internal_ip)
    create_service(endpoint, admin_token, 'ec2', 'ec2',
                   'EC2 Compatibility Layer', region,
                   'http://%s:%s/services/Cloud' % (public_ip, public_port),
                   'http://%s:8773/services/Admin' % internal_ip,
                   'http://%s:8773/services/Cloud' % internal_ip)
    create_service(endpoint, admin_token, 'glance', 'image',
                   'Glance Image Service', region,
                   'http://%s:9292/v1' % public_ip,
                   'http://%s:9292/v1' % internal_ip,
                   'http://%s:9292/v1' % internal_ip)
    create_service(endpoint, admin_token, 'cinder', 'volume',
                   'Openstack Volume Service', region,
                   'http://%s:%s/volume/v1/$(tenant_id)s' % (public_ip,
                                                             public_port),
                   'http://%s:8776/v1/$(tenant_id)s' % internal_ip,
                   'http://%s:8776/v1/$(tenant_id)s' % internal_ip)
    create_service(endpoint, admin_token, 'quantum', 'network',
                   'Quantum Service', region,
                   'http://%s:%s/network' % (public_ip, public_port),
                   'http://%s:9696' % internal_ip,
                   'http://%s:9696' % internal_ip)
