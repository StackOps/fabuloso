# Component properties
#########################################
## DEPLOYTIME VALUES
########################################
singlenode = {
    'host': '127.0.0.1'
}

##########################################
# COMPONENT VALUES
#########################################
os = {
    'hostname': 'controller'
}

mysql = {
    'root_pass': 'stackops',
    'keystone_user': 'keystone',
    'keystone_password': 'stackops',
    'nova_user': 'nova',
    'nova_password': 'stackops',
    'glance_user': 'glance',
    'glance_password': 'stackops',
    'cinder_user': 'cinder',
    'cinder_password': 'stackops',
    'quantum_user': 'quantum',
    'quantum_password': 'stackops'
}

rabbit = {
    'password': 'guest'
}

keystone = {
    'admin_token': 'stackops_admin',
    'admin_pass': mysql['root_pass'],
    'mysql_username': mysql['keystone_user'],
    'mysql_password': mysql['keystone_password'],
    'mysql_schema': 'keystone',
    'protocol': 'http',
    'auth_port': '35357',
    'host': singlenode['host'],
    'tenant_name': 'service',
    'region': 'RegionOne',
    'endpoint': 'http://' + singlenode['host'] + ':35357/v2.0',
    'ks_public_url': 'http://' + singlenode['host'] + ':35357/v2.0',
    'ks_admin_url': 'http://' + singlenode['host'] + '/keystone/v2.0',
    'ks_internal_url': 'http://' + singlenode['host'] + ':5000/v2.0',
    'ks_user': 'keystone',
    'ks_password': 'stackops',
    'nova_public_url': 'http://' + singlenode['host'] +
                       '/compute/v1.1/$(tenant_id)s',
    'nova_admin_url': 'http://' + singlenode['host']
                      + ':8774/v1.1/$(tenant_id)s',
    'nova_internal_config': 'http://' + singlenode['host'] + ':8774/v1.1',
    'nova_internal_url': 'http://' + singlenode['host']
                         + ':8774/v1.1/$(tenant_id)s',
    'nova_user': 'nova',
    'nova_password': 'stackops',
    'ec2_public_url': 'http://' + singlenode['host'] + '/services/Cloud',
    'ec2_admin_url': 'http://' + singlenode['host'] + '/services/Admin',
    'ec2_internal_url': 'http://' + singlenode['host'] + '/services/Cloud',
    'glance_port': '9292',
    'glance_public_url': 'http://' + singlenode['host'] + '/glance/v1',
    'glance_admin_url': 'http://' + singlenode['host'] + ':9292/v1',
    'glance_internal_url': 'http://' + singlenode['host'] + ':9292/v1',
    'glance_user': 'glance',
    'glance_password': 'stackops',
    'quantum_public_url': 'http://' + singlenode['host'] + '/network',
    'quantum_admin_url': 'http://' + singlenode['host'] + ':9696',
    'quantum_internal_url': 'http://' + singlenode['host'] + ':9696',
    'quantum_user': 'quantum',
    'quantum_password': 'stackops',
    'cinder_public_url': 'http://' + singlenode['host'] +
                         '/volume/v1/$(tenant_id)s',
    'cinder_admin_url': 'http://' + singlenode['host'] +
                        ':8776/v1/$(tenant_id)s',
    'cinder_internal_config': 'http://' + singlenode['host'] + ':8776/v1',
    'cinder_internal_url': 'http://' + singlenode['host'] +
                           ':8776/v1/$(tenant_id)s',
    'cinder_user': 'cinder',
    'cinder_password': 'stackops'
}

glance = {
    'auth_uri': keystone['endpoint'],
    'user': keystone['glance_user'],
    'password': keystone['glance_password'],
    'mysql_username': mysql['glance_user'],
    'mysql_password': mysql['glance_password'],
    'auth_port': keystone['auth_port'],
    'auth_protocol': keystone['protocol'],
    'auth_host': singlenode['host']
}

nova = {
    'user': keystone['nova_user'],
    'password': keystone['nova_password'],
    'mysql_username': mysql['nova_user'],
    'mysql_password': mysql['nova_password'],
    'auth_port': keystone['auth_port'],
    'auth_protocol': keystone['protocol'],
    'auth_host': singlenode['host'],
    'management_ip': singlenode['host'],
    'props': {
        'rabbit_host': singlenode['host'],
        's3_host': singlenode['host'],
        'ec2_host': singlenode['host'],
        'ec2_dmz_host': singlenode['host'],
        'metadata_host': singlenode['host'],
        'nova_url': keystone['nova_internal_url'],
        'ec2_url': keystone['ec2_internal_url'],
        'keystone_ec2_url': keystone['ks_internal_url'] + '/ec2tokens',
        'quantum_url': keystone['quantum_internal_url'],
        'quantum_admin_auth_url': keystone['endpoint'],
        'glance_api_servers': keystone['glance_internal_url'],
        'novncproxy_base_url': 'http://' + singlenode['host']
                               + ':6080/vnc_auto.html',
        'vncserver_proxyclient_address': singlenode['host']
    }
}

quantum = {
    'iface_ex': 'eth2',
    'iface_bridge': 'eth1',
    'br_postfix': 'eth1',
    'vlan_start': 1,
    'user': keystone['quantum_user'],
    'password': keystone['quantum_password'],
    'mysql_username': mysql['quantum_user'],
    'mysql_password': mysql['quantum_password'],
    'auth_port': keystone['auth_port'],
    'auth_protocol': keystone['protocol'],
    'auth_host': singlenode['host'],
    'management_ip': singlenode['host'],
    'region': keystone['region'],
    'auth_url': keystone['endpoint']
}

cinder = {
    'user': keystone['cinder_user'],
    'password': keystone['cinder_password'],
    'mysql_username': mysql['cinder_user'],
    'mysql_password': mysql['cinder_password'],
    'auth_port': keystone['auth_port'],
    'auth_protocol': keystone['protocol'],
    'auth_host': singlenode['host']
}

compute = {
    'user': keystone['nova_user'],
    'password': keystone['nova_password'],
    'mysql_username': mysql['nova_user'],
    'mysql_password': mysql['nova_password'],
    'auth_port': keystone['auth_port'],
    'auth_protocol': keystone['protocol'],
    'auth_host': singlenode['host'],
    'management_ip': singlenode['host'],
    'hostname': singlenode['host'],
    'admin_auth_url': keystone['endpoint'],
    'quantum_url': keystone['quantum_internal_url'],
    'glance_host': singlenode['host'],
    'glance_port': keystone['glance_port']
}

apache = {
    'keystone_host': singlenode['host'],
    'ec2_internal_url': keystone['ec2_internal_url'],
    'compute_internal_url': keystone['nova_internal_config'],
    'keystone_internal_url': keystone['ks_internal_url'],
    'glance_internal_url': keystone['glance_internal_url'],
    'cinder_internal_url': keystone['cinder_internal_config'],
    'quantum_internal_url': keystone['quantum_internal_url']
}
