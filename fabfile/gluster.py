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

from fabric.api import *
from cuisine import *

import utils

@task
def stop():
    with settings(warn_only=True):
        sudo("nohup service glusterfs-server stop")
@task
def start():
    stop()
    sudo("nohup service glusterfs-server start")

@task
def configure_ubuntu_packages_server():
    """Configure gluster packages"""
    package_ensure('xfsprogs')
    package_ensure('glusterfs-server')

@task
def uninstall_ubuntu_packages():
    """Uninstall gluster packages"""
    package_clean('glusterfs-server')
    package_ensure('xfsprogs')

@task
def add_repos():
    """Clean and Add necessary repositories and updates"""
    package_ensure('python-software-properties')
    sudo('add-apt-repository -y ppa:semiosis/ubuntu-glusterfs-3.3')
    sudo('apt-get -y update')

@task
def configure():
    """Generate gluster configuration. Execute on all gluster servers"""
    configure_ubuntu_packages_server()
    sudo('update-rc.d glusterd defaults')
@task
def configure_client():
    """Configure gluster client."""
    package_ensure('glusterfs-client')


@task
def version():
    """Gluster FS version"""
    sudo('glusterfsd --version')

@task
def pool_attach(peer_host):
    """Attach a host to the pool"""
    sudo('gluster peer probe %s' % peer_host)

@task
def pool_detach(peer_host):
    """Detach a host to the pool"""
    sudo('gluster peer detach %s' % peer_host)

@task
def pool_status():
    """Get pool status"""
    sudo('gluster peer status')

@task
def format_xfs(dev):
    """Format partition with XFS"""
    sudo("mkfs.xfs -f %s" % dev)

@task
def fstab_client_add(dev, mount_point,mount_params='defaults,_netdev'):
    sudo('sed -i "#%s#d" /etc/fstab' % dev)
    sudo('mkdir -p %s' % mount_point)
    mpoint = '%s %s glusterfs %s 0 0' % (dev, mount_point, mount_params)
    sudo('echo "\n%s" >> /etc/fstab' % mpoint)
    sudo('mount -a')

@task
def fstab_client_delete(dev):
    sudo('sed -i "#%s#d" /etc/fstab' % dev)
    sudo('mount -a')

@task
def fstab_add_brick(dev, mount_point,mount_params='delaylog,sunit=256,swidth=1536,logbufs=8,logbsize=256k,noatime,nodiratime'):
    sudo('sed -i "#%s#d" /etc/fstab' % dev)
    sudo('mkdir -p %s' % mount_point)
    mpoint = '%s %s xfs %s 0 0' % (dev, mount_point, mount_params)
    sudo('echo "\n%s" >> /etc/fstab' % mpoint)
    sudo('mount -a')

@task
def fstab_delete_brick(dev):
    sudo('sed -i "#%s#d" /etc/fstab' % dev)
    sudo('mount -a')

@task
def create_volume_distributed_replicated(name,host_list,replica='2',transport='tcp'):
    """Create a distributed replicated volume"""
    sudo("gluster volume create %s replica %s transport %s %s" % (name, replica, transport, host_list))

@task
def delete_volume(name):
    """Delete a volume"""
    sudo("gluster volume delete %s" % name)

@task
def volume_start(name):
    """Start the volume given"""
    sudo("gluster volume start %s" % name)

@task
def volume_stop(name,force=''):
    """Stop the volume given"""
    sudo("gluster volume stop %s %s" % (name,force))

@task
def volume_status(name):
    """Status of the volume given"""
    sudo("gluster volume info %s" % name)

@task
def volume_rebalance_start(name):
    """Starts the rebalance process in the volume given"""
    sudo("gluster volume rebalance %s start" % name)

@task
def volume_rebalance_stop(name):
    """Stops the rebalance process in the volume given"""
    sudo("gluster volume rebalance %s stop" % name)

@task
def volume_rebalance_status(name):
    """Current status of the rebalance process in the volume given"""
    sudo("gluster volume rebalance %s status" % name)
