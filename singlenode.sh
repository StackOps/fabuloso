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

#!/bin/bash

export MYSQL_ROOT_PASSWORD=stackops
export MYSQL_HOST=$CONTROLLER_HOST
export MYSQL_PORT=3306
export MYSQL_KEYSTONE_USERNAME=keystone export MYSQL_KEYSTONE_PASSWORD=stackops
export MYSQL_KEYSTONE_SCHEMA=keystone
export MYSQL_GLANCE_USERNAME=glance
export MYSQL_GLANCE_PASSWORD=stackops
export MYSQL_GLANCE_SCHEMA=glance
export MYSQL_NOVA_USERNAME=nova
export MYSQL_NOVA_PASSWORD=stackops
export MYSQL_NOVA_SCHEMA=nova
export MYSQL_QUANTUM_USERNAME=quantum
export MYSQL_QUANTUM_PASSWORD=stackops
export MYSQL_QUANTUM_SCHEMA=quantum
export MYSQL_CINDER_USERNAME=cinder
export MYSQL_CINDER_PASSWORD=stackops
export MYSQL_CINDER_SCHEMA=cinder

export ADMIN_USER_PASS=stackops
export SERVICE_TENANT_NAME=service
export SERVICE_GLANCE_USER=glance
export SERVICE_GLANCE_PASS=stackops
export SERVICE_NOVA_USER=nova
export SERVICE_NOVA_PASS=stackops
export SERVICE_QUANTUM_USER=quantum
export SERVICE_QUANTUM_PASS=stackops
export SERVICE_CINDER_USER=cinder
export SERVICE_CINDER_PASS=stackops

export TEST_USERNAME=admin
export TEST_PASSWORD=$ADMIN_USER_PASS
export TEST_TENANT_NAME=admin

export REGION=RegionOne
export AUTH_HOST=$KEYSTONE_HOST
export AUTH_PORT=35357
export AUTH_PROTOCOL=http
export AUTH_URI=http://$KEYSTONE_HOST:5000/v2.0
export ADMIN_AUTH_URL=http://$KEYSTONE_HOST:35357/v2.0
export ADMIN_TOKEN=stackops
export IFACE_EXT=eth2
export IFACE_BRIDGE=eth1
export VLAN_START=600
export VLAN_END=610
export LIBVIRT_TYPE=qemu
export KEYSTONE_PUBLIC_URL=http://$PUBLIC_IP/keystone/v2.0
export KEYSTONE_ADMIN_URL=http://$KEYSTONE_HOST:35357/v2.0
export KEYSTONE_INTERNAL_URL=http://$KEYSTONE_HOST:5000/v2.0
export KEYSTONE_PROXY_URL=http://$KEYSTONE_HOST:5000/v2.0
export GLANCE_PUBLIC_URL=http://$PUBLIC_IP/glance/v1
export GLANCE_ADMIN_URL=http://$GLANCE_HOST:9292/v1
export GLANCE_INTERNAL_URL=http://$GLANCE_HOST:9292/v1
export GLANCE_PROXY_URL=http://$GLANCE_HOST:9292/v1
export COMPUTE_PUBLIC_URL=http://$PUBLIC_IP/compute/v1.1/\$\(tenant_id\)s
export COMPUTE_ADMIN_URL=http://$CONTROLLER_HOST:\$\(compute_port\)s/v1.1/\$\(tenant_id\)s
export COMPUTE_INTERNAL_URL=http://$CONTROLLER_HOST:\$\(compute_port\)s/v1.1/\$\(tenant_id\)s
export COMPUTE_PROXY_URL=http://$CONTROLLER_HOST:8774/v1.1
export EC2_PUBLIC_URL=http://$PUBLIC_IP/services/Cloud
export EC2_ADMIN_URL=http://$CONTROLLER_HOST:8773/services/Admin
export EC2_INTERNAL_URL=http://$CONTROLLER_HOST:8773/services/Cloud
export EC2_PROXY_URL=http://$CONTROLLER_HOST:8773/services
export NOVNCPROXY_URL=http://$VNCPROXY_HOST:$VNCPROXY_PORT/vnc_auto.html
export CINDER_PUBLIC_URL=http://$PUBLIC_IP/volume/v1/\$\(tenant_id\)s
export CINDER_ADMIN_URL=http://$CINDER_HOST:8776/v1/\$\(tenant_id\)s
export CINDER_INTERNAL_URL=http://$CINDER_HOST:8776/v1/\$\(tenant_id\)s
export CINDER_PROXY_URL=http://$CINDER_HOST:8776/v1
export QUANTUM_PUBLIC_URL=http://$PUBLIC_IP/network
export QUANTUM_ADMIN_URL=http://$QUANTUMAPI_HOST:9696
export QUANTUM_INTERNAL_URL=http://$QUANTUMAPI_HOST:9696
export QUANTUM_PROXY_URL=http://$QUANTUMAPI_HOST:9696
export PORTAL_PROXY_URL=http://127.0.0.1
export ACTIVITY_PROXY_URL=http://127.0.0.1
export CHARGEBACK_PROXY_URL=http://127.0.0.1

HOST=127.0.0.1
PORT=${PORT:-2223}
HOSTNAME=controller

# Configure QUANTUM Server
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa mysql.configure_quantum:root_pass="$MYSQL_ROOT_PASSWORD",drop_schema=False,schema="$MYSQL_QUANTUM_SCHEMA",username="$MYSQL_QUANTUM_USERNAME",password="$MYSQL_QUANTUM_PASSWORD"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa  keystone.create_service:endpoint="$ADMIN_AUTH_URL",admin_token="$ADMIN_TOKEN",name="quantum",type="network",description="Openstack Quantum Services",region="$REGION",public_url=$QUANTUM_PUBLIC_URL,admin_url=$QUANTUM_ADMIN_URL,internal_url=$QUANTUM_INTERNAL_URL
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa keystone.configure_service_user:endpoint="$ADMIN_AUTH_URL",user_name="$SERVICE_QUANTUM_USER",admin_token="$ADMIN_TOKEN",user_pass="$SERVICE_QUANTUM_PASS"

fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.compile_datapath
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.configure:iface_ex=$IFACE_EXT
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.configure_files:service_user="$SERVICE_QUANTUM_USER",service_tenant_name="$SERVICE_TENANT_NAME",service_pass="$SERVICE_QUANTUM_PASS",auth_host="$AUTH_HOST",auth_port="$AUTH_PORT",auth_protocol="$AUTH_PROTOCOL"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.configure_quantum:rabbit_host="$RABBITMQ_HOST"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.configure_ovs_plugin_vlan:iface_bridge=$IFACE_BRIDGE,vlan_start=$VLAN_START,vlan_end=$VLAN_END,mysql_username="$MYSQL_QUANTUM_USERNAME",mysql_password="$MYSQL_QUANTUM_PASSWORD",mysql_host="$MYSQL_HOST",mysql_port="$MYSQL_PORT",mysql_schema="$MYSQL_QUANTUM_SCHEMA"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.configure_l3_agent:service_user="$SERVICE_QUANTUM_USER",service_tenant_name="$SERVICE_TENANT_NAME",service_pass="$SERVICE_QUANTUM_PASS",auth_url="$ADMIN_AUTH_URL",metadata_ip="$CONTROLLER_HOST",region="$REGION"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.configure_dhcp_agent
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum_plugins.start
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum.configure
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum.configure_files
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa quantum.start

# Configure CINDER
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa mysql.configure_cinder:root_pass="$MYSQL_ROOT_PASSWORD",drop_schema=False,schema="$MYSQL_CINDER_SCHEMA",username="$MYSQL_CINDER_USERNAME",password="$MYSQL_CINDER_PASSWORD"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa keystone.create_service:endpoint="$ADMIN_AUTH_URL",admin_token="$ADMIN_TOKEN",name="cinder",type="volume",description="Openstack Volume Services",region="$REGION",public_url=$CINDER_PUBLIC_URL,admin_url=$CINDER_ADMIN_URL,internal_url=$CINDER_INTERNAL_URL
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa keystone.configure_service_user:endpoint="$ADMIN_AUTH_URL",user_name="$SERVICE_CINDER_USER",admin_token="$ADMIN_TOKEN",user_pass="$SERVICE_CINDER_PASS"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa cinder.configure
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa cinder.configure_files:rabbit_host="$RABBITMQ_HOST",mysql_username="$MYSQL_CINDER_USERNAME",mysql_password="$MYSQL_CINDER_PASSWORD",mysql_host="$MYSQL_HOST",mysql_port="$MYSQL_PORT",mysql_schema="$MYSQL_CINDER_SCHEMA",service_user="$SERVICE_CINDER_USER",service_tenant_name="$SERVICE_TENANT_NAME",service_pass="$SERVICE_CINDER_PASS",auth_host="$AUTH_HOST",auth_port="$AUTH_PORT",auth_protocol="$AUTH_PROTOCOL"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa baseos.parted_mklabel:disk=/dev/sdb
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa baseos.parted:disk=/dev/sdb,start=0,end=100
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa cinder.create_volume:partition=/dev/sdb1
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa cinder.iscsi_start
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa cinder.start

# Configure Compute Node
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_network
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_ntp
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_vhost_net
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_libvirt:hostname=$HOSTNAME
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_hugepages:is_enabled=True,percentage='70'
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_files:management_ip="$HOST",quantum_url="$QUANTUM_INTERNAL_URL",admin_auth_url="$ADMIN_AUTH_URL",libvirt_type="$LIBVIRT_TYPE",rabbit_host="$RABBITMQ_HOST",mysql_username="$MYSQL_NOVA_USERNAME",mysql_password="$MYSQL_NOVA_PASSWORD",mysql_host="$MYSQL_HOST",mysql_port="$MYSQL_PORT",mysql_schema="$MYSQL_NOVA_SCHEMA",service_user="$SERVICE_NOVA_USER",service_tenant_name="$SERVICE_TENANT_NAME",service_pass="$SERVICE_NOVA_PASS",auth_host="$AUTH_HOST",auth_port="$AUTH_PORT",auth_protocol="$AUTH_PROTOCOL",vncproxy_host="$VNCPROXY_HOST",vncproxy_port="$VNCPROXY_PORT",glance_host="$GLANCE_HOST",glance_port="$GLANCE_PORT"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_quantum:rabbit_host="$RABBITMQ_HOST"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.configure_ovs_plugin_vlan:iface_bridge="$IFACE_BRIDGE",vlan_start="$VLAN_START",vlan_end="$VLAN_END",mysql_username="$MYSQL_QUANTUM_USERNAME",mysql_password="$MYSQL_QUANTUM_PASSWORD",mysql_host="$MYSQL_HOST",mysql_port="$MYSQL_PORT",mysql_schema="$MYSQL_QUANTUM_SCHEMA"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa compute.start

# Configure Apache
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa apache.configure:keystone_host="$AUTH_HOST",ec2_internal_url="$EC2_PROXY_URL",compute_internal_url="$COMPUTE_PROXY_URL",keystone_internal_url="$KEYSTONE_PROXY_URL",glance_internal_url="$GLANCE_PROXY_URL",cinder_internal_url="$CINDER_PROXY_URL",quantum_internal_url="$QUANTUM_PROXY_URL",portal_internal_url="$PORTAL_PROXY_URL",activity_internal_url="$ACTIVITY_PROXY_URL",chargeback_internal_url="$CHARGEBACK_PROXY_URL"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa apache.start

