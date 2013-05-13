#!/usr/bin/env python

from fabric.api import task
from fabric.context_managers import hide
from baseos import add_repos
from baseos import add_users
from baseos import change_hostname
from rabbitmq import configure as rabbit_configure
from rabbitmq import start as rabbit_start
from mysql import configure as mysql_configure
from mysql import start as mysql_start


HOSTNAME = 'controller'


@task
def configure_rabbit_and_mysql():
    """ Basic system configuration.

    Configures rabbitmq and mysql services and starts them.
    """
    with hide('stdout', 'status', 'running'):
        add_repos()
        add_users()
        change_hostname(HOSTNAME)
        rabbit_configure()
        rabbit_start()
        mysql_configure()
        mysql_start()
