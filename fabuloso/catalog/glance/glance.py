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
from fabric.api import sudo, settings, put, cd, local, puts
from cuisine import package_ensure, package_clean

GLANCE_IMAGES = '/var/lib/glance/images'


def stop():
    with settings(warn_only=True):
        sudo("service glance-api stop")
        sudo("service glance-registry stop")


def start():
    stop()
    sudo("service glance-api start")
    sudo("service glance-registry start")


def uninstall_ubuntu_packages():
    """Uninstall glance packages"""
    package_clean('glance')
    package_clean('glance-api')
    package_clean('python-glanceclient')
    package_clean('glance-common')
    package_clean('glance-registry')
    package_clean('python-glance')
    package_clean('python-mysqldb')


def install(cluster=False):
    """Generate glance configuration. Execute on both servers"""
    package_ensure('glance')
    package_ensure('glance-api')
    package_ensure('python-glanceclient')
    package_ensure('glance-common')
    package_ensure('glance-registry')
    package_ensure('python-glance')
    package_ensure('python-mysqldb')
    if cluster:
        stop()
        sudo('echo "manual" >> /etc/init/glance-registry.override')
        sudo('echo "manual" >> /etc/init/glance-api.override')
        sudo('mkdir -p /usr/lib/ocf/resource.d/openstack')
        put('./ocf/glance-registry',
            '/usr/lib/ocf/resource.d/openstack/glance-registry', use_sudo=True)
        put('./ocf/glance-api',
            '/usr/lib/ocf/resource.d/openstack/glance-api', use_sudo=True)
        sudo('chmod +x /usr/lib/ocf/resource.d/openstack/glance-*')


def sql_connect_string(host, password, port, schema, username):
    sql_connection = 'mysql://%s:%s@%s:%s/%s' % (username, password, host,
                                                 port, schema)
    return sql_connection


def set_config_file(user, password,
                    mysql_username, mysql_password, mysql_schema='glance',
                    tenant='service', mysql_host='127.0.0.1',
                    mysql_port='3306', auth_port='35357', auth_protocol='http',
                    auth_host='127.0.0.1'):
    for f in ['/etc/glance/glance-api.conf',
              '/etc/glance/glance-registry.conf']:
        sudo("sed -i 's#sql_connection.*$#sql_connection = %s#g' %s"
             % (sql_connect_string(mysql_host, mysql_password, mysql_port,
                                   mysql_schema, mysql_username), f))
        sudo("sed -i 's/admin_password.*$/admin_password = %s/g' %s" %
             (password, f))
        sudo("sed -i 's/admin_tenant_name.*$/admin_tenant_name = %s/g' %s" %
             (tenant, f))
        sudo("sed -i 's/admin_user.*$/admin_user = %s/g' %s" %
             (user, f))
        sudo("sed -i 's/auth_host.*$/auth_host = %s/g' %s" % (auth_host, f))
        sudo("sed -i 's/auth_port.*$/auth_port = %s/g' %s" % (auth_port, f))
        sudo("sed -i 's/auth_protocol.*$/auth_protocol = %s/g' %s"
             % (auth_protocol, f))

    sudo("sed -i 's/^#flavor=.*$/flavor=keystone+cachemanagement/g' "
         "/etc/glance/glance-api.conf")
    sudo("sed -i 's/^#flavor=.*$/flavor=keystone/g' "
         "/etc/glance/glance-registry.conf")
    start()
    sudo("glance-manage version_control 0")
    sudo("glance-manage db_sync")


def configure_local_storage(delete_content=False, set_glance_owner=True):
    if delete_content:
        sudo('rm -fr %s' % GLANCE_IMAGES)
    stop()
    sudo('sed -i "#%s#d" /etc/fstab' % GLANCE_IMAGES)
    sudo('mkdir -p %s' % GLANCE_IMAGES)
    if set_glance_owner:
        sudo('chown glance:glance -R %s' % GLANCE_IMAGES)
    start()


def configure_nfs_storage(endpoint, delete_content=False,
                          set_glance_owner=True, endpoint_params='defaults'):
    package_ensure('nfs-common')
    if delete_content:
        sudo('rm -fr %s' % GLANCE_IMAGES)
    stop()
    sudo('mkdir -p %s' % GLANCE_IMAGES)
    mpoint = '%s %s nfs %s 0 0' % (endpoint, GLANCE_IMAGES, endpoint_params)
    sudo('sed -i "#%s#d" /etc/fstab' % GLANCE_IMAGES)
    sudo('echo "\n%s" >> /etc/fstab' % mpoint)
    sudo('mount -a')
    if set_glance_owner:
        sudo('chown glance:glance -R %s' % GLANCE_IMAGES)
    start()


def publish_ttylinux(auth_uri,
                     test_username='admin', test_password='stackops',
                     test_tenant_name='admin',
                     ):
    image_name = 'ttylinux-uec-amd64-12.1_2.6.35-22_1'
    with cd('/tmp'):
        sudo('wget http://stackops.s3.amazonaws.com/images/%s.tar.gz -O '
             '/tmp/%s.tar.gz' % (image_name, image_name))
        sudo('mkdir -p images')
        sudo('tar -zxf %s.tar.gz  -C images' % image_name)
        stdout = sudo('glance --os-username %s --os-password %s '
                      '--os-tenant-name %s --os-auth-url %s --os-endpoint-type'
                      ' internalURL image-create '
                      '--name="ttylinux-uec-amd64-kernel" '
                      '--is-public=true --container-format=aki '
                      '--disk-format=aki '
                      '< /tmp/images/%s-vmlinuz*' %
                      (test_username, test_password, test_tenant_name,
                       auth_uri, image_name))
        kernel_id = local('''echo "%s" | grep ' id ' ''' %
                          stdout, capture=True).split('|')
        puts(kernel_id)
        sudo('glance --os-username %s --os-password %s --os-tenant-name %s '
             '--os-auth-url %s --os-endpoint-type internalURL image-create '
             '--name="ttylinux-uec-amd64" --is-public=true '
             '--container-format=ami --disk-format=ami --property '
             'kernel_id=%s < /tmp/images/%s.img'
             % (test_username, test_password, test_tenant_name, auth_uri,
                kernel_id[2].strip(), image_name))
        sudo('rm -fR images')
        sudo('rm -f %s.tar.gz' % image_name)
