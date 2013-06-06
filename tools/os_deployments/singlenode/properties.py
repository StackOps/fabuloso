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
    'nova_admin_url': 'http://' + singlenode['host'] + ':8774/v1.1',
    'nova_internal_url': 'http://' + singlenode['host'] + ':8774/v1.1',
    'nova_user': 'nova',
    'nova_password': 'stackops',
    'ec2_public_url': 'http://' + singlenode['host'] + '/services/Cloud',
    'ec2_admin_url': 'http://' + singlenode['host'] + '/services/Admin',
    'ec2_internal_url': 'http://' + singlenode['host'] + '/services/Cloud',
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
