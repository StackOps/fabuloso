#, puts, local   Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
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

# Configure Compute Node
# Configure Apache
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa apache.configure:keystone_host="$AUTH_HOST",ec2_internal_url="$EC2_PROXY_URL",compute_internal_url="$COMPUTE_PROXY_URL",keystone_internal_url="$KEYSTONE_PROXY_URL",glance_internal_url="$GLANCE_PROXY_URL",cinder_internal_url="$CINDER_PROXY_URL",quantum_internal_url="$QUANTUM_PROXY_URL",portal_internal_url="$PORTAL_PROXY_URL",activity_internal_url="$ACTIVITY_PROXY_URL",chargeback_internal_url="$CHARGEBACK_PROXY_URL"
fab -H $HOST:$PORT -u stackops -i bootstrap/nonsecureid_rsa apache.start

