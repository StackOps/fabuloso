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
from fabric.api import sudo, settings
from cuisine import package_ensure


def stop():
    with settings(warn_only=True):
        sudo("nohup service rabbitmq-server stop")


def start():
    stop()
    sudo("nohup service rabbitmq-server start")


def configure_ubuntu_packages():
    """Configure rabbitmq ubuntu packages"""
    package_ensure('rabbitmq-server')


def configure(cluster=False, password='guest'):
    """Generate rabbitmq configuration. Execute on both servers"""
    configure_ubuntu_packages()
    sudo('rabbitmqctl change_password guest %s' % password)
    if cluster:
        stop()
        sudo('update-rc.d rabbitmq-server disable S 2 3 4 5')
        sudo('chmod -R og=rxw /var/lib/rabbitmq')
        sudo('chown -R rabbitmq:rabbitmq /var/lib/rabbitmq')
        sudo('chmod 700 /var/lib/rabbitmq/.erlang.cookie')
