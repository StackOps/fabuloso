#!/usr/bin/env python
import fabuloso
import properties  # Alert! relative import!

env_dict = {
    'host': '127.0.0.1',
    'port': 2223,
    'username': 'stackops',
    'ssh_key_file': '~/.ssh/nonsecureid_rsa',
    'catalog': ['catalog']
}

env = fabuloso.RemoteEnvironment(env_dict)
fab = fabuloso.Fabuloso(env)

# Prepare OS
os = fab.get_component("os", properties.os)
# os.setup_node()

# Prepare mysql
mysql = fab.get_component("mysql", properties.mysql)
# mysql.setup()
# mysql.set_keystone()
# mysql.set_nova()
# mysql.set_glance()
# mysql.set_cinder()
# mysql.set_quantum()

# Prepare Rabbit
rabbit = fab.get_component("rabbitmq", properties.rabbit)
# rabbit.configure()

# Prepare Keystone and register services
keystone = fab.get_component("keystone", properties.keystone)
# keystone.install_and_configure()
# keystone.register_services_and_endpoints()

# Install glance
glance = fab.get_component("glance", properties.glance)
# glance.install_and_configure()
# glance.prepare_image()

# nova = fab.get_component("nova")
# quantum_plugins = fab.get_component("quantum_plugins")
# quantum = fab.get_component("quantum")
# cinder = fab.get_component("cinder")
# compute = fab.get_component("compute")
# apache = fab.get_component("apache")

# Setup basic components

# # # -----------------------------------------------------
# # # Set NOVA
# # # -----------------------------------------------------
# NOVA_SCHEMA_NAME = 'nova'
# NOVA_MYSQL_USERNAME = 'nova'
# NOVA_MYSQL_PASSWORD = 'stackops'
# NOVA_PUBLIC_CONFIG = 'http://127.0.0.1/compute/v1.1'
# NOVA_PUBLIC_URI = NOVA_PUBLIC_CONFIG + '/$(tenant_id)s'
# NOVA_INTERNAL_CONFIG = 'http://127.0.0.1:8774/v1.1'
# NOVA_INTERNAL_URI = NOVA_INTERNAL_CONFIG + '/$(tenant_id)s'
# NOVA_USER = 'nova'
# NOVA_PASSWORD = 'stackops'
# EC2_PUBLIC_URL = 'http://127.0.0.1/services/Cloud'
# EC2_ADMIN_URL = 'http://127.0.0.1:8773/services/Admin'
# EC2_INTERNAL_URL = 'http://127.0.0.1:8773/services/Cloud'
# EC2_PROXY_URL = 'http://127.0.0.1:8773/services'
#
# nova_user = {
#     'tenant': SERVICE_TENANT_NAME,
#     'service_user_name': NOVA_USER,
#     'service_user_pass': NOVA_PASSWORD,
#     'endpoint': KEYSTONE_ENDPOINT,
#     'admin_token': ADMIN_TOKEN
# }
# nova_service = {
#     'user': NOVA_USER,
#     'tenant': SERVICE_TENANT_NAME,
#     'password': NOVA_PASSWORD,
#     'mysql_username': NOVA_MYSQL_USERNAME,
#     'mysql_password': NOVA_MYSQL_PASSWORD,
#     'mysql_schema': NOVA_SCHEMA_NAME,
#     'auth_port': KEYSTONE_AUTH_PORT,
#     'auth_protocol': KEYSTONE_PROTOCOL,
#     'auth_host': KEYSTONE_HOST,
#     'management_ip': '127.0.0.1'
# }
#
# NOVNCPROXY_URL = 'http://127.0.0.1:6080/vnc_auto.html'
#
# nova_properties = {
#     'props': {
#         'rabbit_host': '127.0.0.1',
#         's3_host': '127.0.0.1',
#         'ec2_host': '127.0.0.1',
#         'ec2_dmz_host': '127.0.0.1',
#         'metadata_host': '127.0.0.1',
#         'nova_url': NOVA_INTERNAL_URI,
#         'ec2_url': EC2_INTERNAL_URL,
#         'keystone_ec2_url': KEYSTONE_INTERNAL_URI + '/ec2tokens',
#         'quantum_url': 'http://127.0.0.1:9696',
#         'quantum_admin_auth_url': KEYSTONE_ENDPOINT,
#         'glance_api_servers': GLANCE_INTERNAL_URI,
#         'novncproxy_base_url': NOVNCPROXY_URL,
#         'vncserver_proxyclient_address': '127.0.0.1'
#     }
# }
# mysql.set_schema(**nova_db)
# keystone.register_service(**nova_register)
# keystone.register_service(**ec2_register)
# keystone.register_service_user(**nova_user)
# nova.install_and_configure(**nova_service)
# nova.set_properties(**nova_properties)
# nova.start()
#
# # -----------------------------------------------------
# # Set QUANTUM
# # -----------------------------------------------------
# QUANTUM_SCHEMA_NAME = 'quantum'
# QUANTUM_MYSQL_USERNAME = 'quantum'
# QUANTUM_MYSQL_PASSWORD = 'stackops'
# QUANTUM_PUBLIC_URI = 'http://127.0.0.1/network'
# QUANTUM_INTERNAL_URI = 'http://127.0.0.1:9696'
# QUANTUM_USER = 'quantum'
# QUANTUM_PASSWORD = 'stackops'
#
# quantum_db = {
#     'root_pass': DATABASE_ADMIN_PASSWORD,
#     'schema_name': QUANTUM_SCHEMA_NAME,
#     'username': QUANTUM_MYSQL_USERNAME,
#     'password': QUANTUM_MYSQL_PASSWORD
# }
# quantum_user = {
#     'tenant': SERVICE_TENANT_NAME,
#     'service_user_name': QUANTUM_USER,
#     'service_user_pass': QUANTUM_PASSWORD,
#     'endpoint': KEYSTONE_ENDPOINT,
#     'admin_token': ADMIN_TOKEN
# }
# quantum_service = {
#     'iface_ex': 'eth2',
#     'iface_bridge': 'eth1',
#     'br_postfix': 'eth1',
#     'vlan_start': 1,
#     'user': QUANTUM_USER,
#     'tenant': SERVICE_TENANT_NAME,
#     'password': QUANTUM_PASSWORD,
#     'mysql_username': QUANTUM_MYSQL_USERNAME,
#     'mysql_password': QUANTUM_MYSQL_PASSWORD,
#     'mysql_schema': QUANTUM_SCHEMA_NAME,
#     'auth_port': KEYSTONE_AUTH_PORT,
#     'auth_protocol': KEYSTONE_PROTOCOL,
#     'auth_host': KEYSTONE_HOST,
#     'management_ip': '127.0.0.1',
#     'auth_url': KEYSTONE_ENDPOINT,
#     'region': 'RegionOne'
# }
# mysql.set_schema(**quantum_db)
# keystone.register_service(**quantum_register)
# keystone.register_service_user(**quantum_user)
# quantum_plugins.install_and_configure(**quantum_service)
# quantum_plugins.start()
# quantum.install_and_configure(**quantum_service)
# quantum.start()
#
# # -----------------------------------------------------
# # Set CINDER
# # -----------------------------------------------------
# CINDER_SCHEMA_NAME = 'cinder'
# CINDER_MYSQL_USERNAME = 'cinder'
# CINDER_MYSQL_PASSWORD = 'stackops'
# CINDER_PUBLIC_URI = 'http://127.0.0.1/volume/v1/$(tenant_id)s'
# CINDER_INTERNAL_CONFIG = 'http://127.0.0.1:8776/v1'
# CINDER_INTERNAL_URI = CINDER_INTERNAL_CONFIG + '/$(tenant_id)s'
# CINDER_USER = 'cinder'
# CINDER_PASSWORD = 'stackops'
#
# cinder_user = {
#     'tenant': SERVICE_TENANT_NAME,
#     'service_user_name': CINDER_USER,
#     'service_user_pass': CINDER_PASSWORD,
#     'endpoint': KEYSTONE_ENDPOINT,
#     'admin_token': ADMIN_TOKEN
# }
# cinder_service = {
#     'user': CINDER_USER,
#     'tenant': SERVICE_TENANT_NAME,
#     'password': CINDER_PASSWORD,
#     'mysql_username': CINDER_MYSQL_USERNAME,
#     'mysql_password': CINDER_MYSQL_PASSWORD,
#     'mysql_schema': CINDER_SCHEMA_NAME,
#     'auth_port': KEYSTONE_AUTH_PORT,
#     'auth_protocol': KEYSTONE_PROTOCOL,
#     'auth_host': KEYSTONE_HOST,
# }
# mysql.set_schema(**cinder_db)
# keystone.register_service(**cinder_register)
# keystone.register_service_user(**cinder_user)
# cinder.install_and_configure(**cinder_service)
# # os.parted()
# # cinder.create_volume()
# cinder.start()
#
# # -----------------------------------------------------
# # Set Compute
# # -----------------------------------------------------
# compute_service = {
#     'user': NOVA_USER,
#     'tenant': SERVICE_TENANT_NAME,
#     'password': NOVA_PASSWORD,
#     'mysql_username': NOVA_MYSQL_USERNAME,
#     'mysql_password': NOVA_MYSQL_PASSWORD,
#     'mysql_schema': NOVA_SCHEMA_NAME,
#     'auth_port': KEYSTONE_AUTH_PORT,
#     'auth_protocol': KEYSTONE_PROTOCOL,
#     'auth_host': KEYSTONE_HOST,
#     'management_ip': '127.0.0.1',
#     'hostname': '127.0.0.1',
#     'admin_auth_url': KEYSTONE_ENDPOINT,
#     'quantum_url': QUANTUM_INTERNAL_URI,
#     'glance_host': GLANCE_HOST,
#     'glance_port': GLANCE_PORT
# }
# compute.install_and_configure(**compute_service)
# compute.start()
#
#
# # -----------------------------------------------
# # Set APACHE
# # -----------------------------------------------
# apache_config = {
#     'keystone_host': KEYSTONE_HOST,
#     'ec2_internal_url': EC2_INTERNAL_URL,
#     'compute_internal_url': NOVA_INTERNAL_CONFIG,
#     'keystone_internal_url': KEYSTONE_INTERNAL_URI,
#     'glance_internal_url': GLANCE_INTERNAL_URI,
#     'cinder_internal_url': CINDER_INTERNAL_CONFIG,
#     'quantum_internal_url': QUANTUM_INTERNAL_URI
# }
# apache.install(**apache_config)
# apache.start()
