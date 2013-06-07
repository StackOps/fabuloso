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
os.setup_node()

# Prepare mysql
mysql = fab.get_component("mysql", properties.mysql)
mysql.setup()
mysql.set_keystone()
mysql.set_nova()
mysql.set_glance()
mysql.set_cinder()
mysql.set_quantum()

# Prepare Rabbit
rabbit = fab.get_component("rabbitmq", properties.rabbit)
rabbit.configure()

# Prepare Keystone and register services
keystone = fab.get_component("keystone", properties.keystone)
keystone.install_and_configure()
keystone.register_services_and_endpoints()

# Install glance
glance = fab.get_component("glance", properties.glance)
glance.install_and_configure()
glance.prepare_image()

nova = fab.get_component("nova", properties.nova)
nova.install_and_configure()
nova.nova_properties()
nova.start()

quantum_plugins = fab.get_component("quantum_plugins", properties.quantum)
quantum_plugins.install_and_configure()
quantum_plugins.start()

quantum = fab.get_component("quantum", properties.quantum)
quantum.install_and_configure()
quantum.start()

cinder = fab.get_component("cinder", properties.cinder)
cinder.install_and_configure()
cinder.start()

compute = fab.get_component("compute", properties.compute)
compute.install_and_configure()
compute.start()

apache = fab.get_component("apache", properties.apache)
apache.install()
apache.start()
