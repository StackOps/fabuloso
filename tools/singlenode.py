#!/usr/bin/env python
import fabuloso

HOSTNAME = 'controller'
DATABASE_ADMIN_PASSWORD = 'stackops'
ADMIN_TOKEN = 'stackops_token'
ADMIN_PASSWORD = 'stackops'
KEYSTONE_PROTOCOL = 'http'
KEYSTONE_HOST = 'localhost'
KEYSTONE_AUTH_PORT = '35357'
KEYSTONE_ENDPOINT = (KEYSTONE_PROTOCOL + '://' + KEYSTONE_HOST + ':'
                     + KEYSTONE_AUTH_PORT + '/v2.0')
SERVICE_TENANT_NAME = 'service'

env_dict = {
    'host': 'localhost',
    'port': 2223,
    'username': 'stackops',
    'ssh_key_file': '~/.ssh/nonsecureid_rsa',
    'catalog': ['catalog']
}

env = fabuloso.RemoteEnvironment(env_dict)
# Configure MySQL y RabbitMQ
fab = fabuloso.Fabuloso(env)

os = fab.get_component("os")
mysql = fab.get_component("mysql")
rabbit = fab.get_component("rabbitmq")
keystone = fab.get_component("keystone")
glance = fab.get_component("glance")
nova = fab.get_component("nova")
quantum_plugins = fab.get_component("quantum_plugins")
quantum = fab.get_component("quantum")
cinder = fab.get_component("cinder")
compute = fab.get_component("compute")
apache = fab.get_component("apache")

# Setup basic components
os.setup_singlenode(new_hostname=HOSTNAME)
mysql.setup(root_pass=DATABASE_ADMIN_PASSWORD)
rabbit.configure()

# ---------------------------------------------------
# Set keystone
# ---------------------------------------------------
KEYSTONE_SCHEMA_NAME = 'keystone'
KEYSTONE_MYSQL_USERNAME = 'keystone'
KEYSTONE_MYSQL_PASSWORD = 'stackops'
KEYSTONE_PUBLIC_URI = 'http://localhost/keystone/v2.0'
KEYSTONE_INTERNAL_URI = 'http://localhost:5000/v2.0'
keys_db = {
    'root_pass': DATABASE_ADMIN_PASSWORD,
    'schema_name': KEYSTONE_SCHEMA_NAME,
    'username': KEYSTONE_MYSQL_USERNAME,
    'password': KEYSTONE_MYSQL_PASSWORD
}
keys_config = {
    'admin_token': ADMIN_TOKEN,
    'admin_pass': ADMIN_PASSWORD,
    'mysql_username': KEYSTONE_MYSQL_USERNAME,
    'mysql_password': KEYSTONE_MYSQL_PASSWORD,
    'mysql_schema': KEYSTONE_SCHEMA_NAME,
    'endpoint': KEYSTONE_ENDPOINT,
    'tenant_name': SERVICE_TENANT_NAME
}
keys_serv = {
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN,
    'service_name': 'keystone',
    'service_type': 'identity',
    'description': 'Keystone Identity Service',
    'region': 'RegionOne',
    'public_url': KEYSTONE_PUBLIC_URI,
    'admin_url': KEYSTONE_ENDPOINT,
    'internal_url': KEYSTONE_INTERNAL_URI
}
mysql.set_schema(**keys_db)
keystone.install_and_configure(**keys_config)
keystone.register_service(**keys_serv)

# -----------------------------------------------------
# Set Glance
# -----------------------------------------------------
GLANCE_SCHEMA_NAME = 'glance'
GLANCE_MYSQL_USERNAME = 'glance'
GLANCE_MYSQL_PASSWORD = 'stackops'
GLANCE_PUBLIC_URI = 'http://localhost/glance/v1'
GLANCE_PORT = '9292'
GLANCE_HOST = 'localhost'
GLANCE_INTERNAL_URI = 'http://' + GLANCE_HOST + ':' + GLANCE_PORT + '/v1'
GLANCE_USER = 'glance'
GLANCE_PASSWORD = 'stackops'

glance_db = {
    'root_pass': DATABASE_ADMIN_PASSWORD,
    'schema_name': GLANCE_SCHEMA_NAME,
    'username': GLANCE_MYSQL_USERNAME,
    'password': GLANCE_MYSQL_PASSWORD
}
glance_service = {
    'user': GLANCE_USER,
    'tenant': SERVICE_TENANT_NAME,
    'password': GLANCE_PASSWORD,
    'mysql_username': GLANCE_MYSQL_USERNAME,
    'mysql_password': GLANCE_MYSQL_PASSWORD,
    'mysql_schema': GLANCE_SCHEMA_NAME,
    'auth_port': KEYSTONE_AUTH_PORT,
    'auth_protocol': KEYSTONE_PROTOCOL,
    'auth_host': KEYSTONE_HOST
}
glance_register = {
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN,
    'service_name': 'glance',
    'service_type': 'image',
    'description': 'Glance Image Service',
    'region': 'RegionOne',
    'public_url': GLANCE_PUBLIC_URI,
    'admin_url': GLANCE_INTERNAL_URI,
    'internal_url': GLANCE_INTERNAL_URI
}
glance_user = {
    'tenant': SERVICE_TENANT_NAME,
    'service_user_name': GLANCE_USER,
    'service_user_pass': GLANCE_PASSWORD,
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN
}
mysql.set_schema(**glance_db)
glance.install_and_configure(**glance_service)
keystone.register_service(**glance_register)
keystone.register_service_user(**glance_user)
glance.prepare_image(auth_uri=KEYSTONE_INTERNAL_URI)

# -----------------------------------------------------
# Set NOVA
# -----------------------------------------------------
NOVA_SCHEMA_NAME = 'nova'
NOVA_MYSQL_USERNAME = 'nova'
NOVA_MYSQL_PASSWORD = 'stackops'
NOVA_PUBLIC_URI = 'http://localhost/compute/v1.1/\$\(tenant_id\)s'
NOVA_INTERNAL_URI = 'http://localhost:8774/v1'
NOVA_USER = 'nova'
NOVA_PASSWORD = 'stackops'
EC2_PUBLIC_URL = 'http://localhost/services/Cloud'
EC2_ADMIN_URL = 'http://localhost:8773/services/Admin'
EC2_INTERNAL_URL = 'http://localhost:8773/services/Cloud'
EC2_PROXY_URL = 'http://localhost:8773/services'

nova_db = {
    'root_pass': DATABASE_ADMIN_PASSWORD,
    'schema_name': NOVA_SCHEMA_NAME,
    'username': NOVA_MYSQL_USERNAME,
    'password': NOVA_MYSQL_PASSWORD
}
nova_register = {
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN,
    'service_name': 'nova',
    'service_type': 'compute',
    'description': 'OpenStack Computer Service',
    'region': 'RegionOne',
    'public_url': NOVA_PUBLIC_URI,
    'admin_url': NOVA_INTERNAL_URI,
    'internal_url': NOVA_INTERNAL_URI
}
ec2_register = {
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN,
    'service_name': 'ec2',
    'service_type': 'ec2',
    'description': 'EC2 Compatibility Service',
    'region': 'RegionOne',
    'public_url': EC2_PUBLIC_URL,
    'admin_url': EC2_ADMIN_URL,
    'internal_url': EC2_INTERNAL_URL
}
nova_user = {
    'tenant': SERVICE_TENANT_NAME,
    'service_user_name': NOVA_USER,
    'service_user_pass': NOVA_PASSWORD,
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN
}
nova_service = {
    'user': NOVA_USER,
    'tenant': SERVICE_TENANT_NAME,
    'password': NOVA_PASSWORD,
    'mysql_username': NOVA_MYSQL_USERNAME,
    'mysql_password': NOVA_MYSQL_PASSWORD,
    'mysql_schema': NOVA_SCHEMA_NAME,
    'auth_port': KEYSTONE_AUTH_PORT,
    'auth_protocol': KEYSTONE_PROTOCOL,
    'auth_host': KEYSTONE_HOST,
    'management_ip': 'localhost'
}

NOVNCPROXY_URL = 'http://localhost:6080/vnc_auto.html'

nova_properties = {
    'rabbit_host': 'localhost',
    's3_host': 'localhost',
    'ec2_host': 'localhost',
    'ec2_dmz_host': 'localhost',
    'metadata_host': 'localhost',
    'nova_url': NOVA_INTERNAL_URI,
    'ec2_url': EC2_INTERNAL_URL,
    'keystone_ec2_url': KEYSTONE_INTERNAL_URI + '/ec2tokens',
    'quantum_url': 'http://localhost:9696',
    'quantum_admin_auth_url': KEYSTONE_ENDPOINT,
    'glance_api_servers': GLANCE_INTERNAL_URI,
    'novncproxy_base_url': NOVNCPROXY_URL,
    'vncserver_proxyclient_address': 'localhost'
}
mysql.set_schema(**nova_db)
keystone.register_service(**nova_register)
keystone.register_service(**ec2_register)
keystone.register_service_user(**nova_user)
nova.install_and_configure(**nova_service)
nova.start()

# -----------------------------------------------------
# Set QUANTUM
# -----------------------------------------------------
QUANTUM_SCHEMA_NAME = 'quantum'
QUANTUM_MYSQL_USERNAME = 'quantum'
QUANTUM_MYSQL_PASSWORD = 'stackops'
QUANTUM_PUBLIC_URI = 'http://localhost/network'
QUANTUM_INTERNAL_URI = 'http://localhost:9696'
QUANTUM_USER = 'quantum'
QUANTUM_PASSWORD = 'stackops'

quantum_db = {
    'root_pass': DATABASE_ADMIN_PASSWORD,
    'schema_name': QUANTUM_SCHEMA_NAME,
    'username': QUANTUM_MYSQL_USERNAME,
    'password': QUANTUM_MYSQL_PASSWORD
}
quantum_register = {
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN,
    'service_name': 'quantum',
    'service_type': 'network',
    'description': 'OpenStack Network Service',
    'region': 'RegionOne',
    'public_url': QUANTUM_PUBLIC_URI,
    'admin_url': QUANTUM_INTERNAL_URI,
    'internal_url': QUANTUM_INTERNAL_URI
}
quantum_user = {
    'tenant': SERVICE_TENANT_NAME,
    'service_user_name': QUANTUM_USER,
    'service_user_pass': QUANTUM_PASSWORD,
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN
}
quantum_service = {
    'iface_ex': 'eth2',
    'iface_bridge': 'eth1',
    'br_postfix': 'eth1',
    'vlan_start': 1,
    'user': QUANTUM_USER,
    'tenant': SERVICE_TENANT_NAME,
    'password': QUANTUM_PASSWORD,
    'mysql_username': QUANTUM_MYSQL_USERNAME,
    'mysql_password': QUANTUM_MYSQL_PASSWORD,
    'mysql_schema': QUANTUM_SCHEMA_NAME,
    'auth_port': KEYSTONE_AUTH_PORT,
    'auth_protocol': KEYSTONE_PROTOCOL,
    'auth_host': KEYSTONE_HOST,
    'management_ip': 'localhost',
    'auth_url': KEYSTONE_ENDPOINT,
    'region': 'RegionOne'
}
mysql.set_schema(**quantum_db)
keystone.register_service(**quantum_register)
keystone.register_service_user(**quantum_user)
quantum_plugins.install_and_configure(**quantum_service)
quantum_plugins.start()
quantum.install_and_configure(**quantum_service)
quantum.start()

# -----------------------------------------------------
# Set CINDER
# -----------------------------------------------------
CINDER_SCHEMA_NAME = 'cinder'
CINDER_MYSQL_USERNAME = 'cinder'
CINDER_MYSQL_PASSWORD = 'stackops'
CINDER_PUBLIC_URI = 'http://localhost/volume/v1/\$\(tenant_id\)s'
CINDER_INTERNAL_URI = 'http://localhost:8776/v1/\$\(tenant_id\)s'
CINDER_USER = 'cinder'
CINDER_PASSWORD = 'stackops'

cinder_db = {
    'root_pass': DATABASE_ADMIN_PASSWORD,
    'schema_name': CINDER_SCHEMA_NAME,
    'username': CINDER_MYSQL_USERNAME,
    'password': CINDER_MYSQL_PASSWORD
}
cinder_register = {
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN,
    'service_name': 'cinder',
    'service_type': 'network',
    'description': 'OpenStack Network Service',
    'region': 'RegionOne',
    'public_url': CINDER_PUBLIC_URI,
    'admin_url': CINDER_INTERNAL_URI,
    'internal_url': CINDER_INTERNAL_URI
}
cinder_user = {
    'tenant': SERVICE_TENANT_NAME,
    'service_user_name': CINDER_USER,
    'service_user_pass': CINDER_PASSWORD,
    'endpoint': KEYSTONE_ENDPOINT,
    'admin_token': ADMIN_TOKEN
}
cinder_service = {
    'user': CINDER_USER,
    'tenant': SERVICE_TENANT_NAME,
    'password': CINDER_PASSWORD,
    'mysql_username': CINDER_MYSQL_USERNAME,
    'mysql_password': CINDER_MYSQL_PASSWORD,
    'mysql_schema': CINDER_SCHEMA_NAME,
    'auth_port': KEYSTONE_AUTH_PORT,
    'auth_protocol': KEYSTONE_PROTOCOL,
    'auth_host': KEYSTONE_HOST,
}
mysql.set_schema(**cinder_db)
keystone.register_service(**cinder_register)
keystone.register_service_user(**cinder_user)
cinder.install_and_configure(**cinder_service)
# os.parted()
# cinder.create_volume()
cinder.start()

# -----------------------------------------------------
# Set Compute
# -----------------------------------------------------
compute_service = {
    'user': NOVA_USER,
    'tenant': SERVICE_TENANT_NAME,
    'password': NOVA_PASSWORD,
    'mysql_username': NOVA_MYSQL_USERNAME,
    'mysql_password': NOVA_MYSQL_PASSWORD,
    'mysql_schema': NOVA_SCHEMA_NAME,
    'auth_port': KEYSTONE_AUTH_PORT,
    'auth_protocol': KEYSTONE_PROTOCOL,
    'auth_host': KEYSTONE_HOST,
    'management_ip': 'localhost',
    'hostname': 'localhost',
    'admin_auth_url': KEYSTONE_ENDPOINT,
    'quantum_url': QUANTUM_INTERNAL_URI,
    'glance_host': GLANCE_HOST,
    'glance_port': GLANCE_PORT
}
compute.install_and_configure(**compute_service)
compute.start()


# -----------------------------------------------
# Set APACHE
# -----------------------------------------------
apache_config = {
    'keystone_host': KEYSTONE_HOST,
    'ec2_internal_url': EC2_INTERNAL_URL,
    'compute_internal_url': NOVA_INTERNAL_URI,
    'keystone_internal_url': KEYSTONE_INTERNAL_URI,
    'glance_internal_url': GLANCE_INTERNAL_URI,
    'cinder_internal_url': CINDER_INTERNAL_URI,
    'quantum_internal_url': QUANTUM_INTERNAL_URI
}
apache.install(**apache_config)
apache.start()
