Quickstart
==========

.. note::

    First you need to `install <install.html>`_ `FABuloso` on your system. Once installed you can follow this quickstart guide to start deploying OpenStack.

In order to deploy some `components` we will use the builtin `FABuloso` shell.

Starting the shell
------------------

Just open a terminal and type:

.. code-block:: bash

    $ fabuloso

The `FABuloso` shell should be started. Type `help` to see all available commands::

    fabuloso > help

    Available methods are:

    * add_environment
    * add_key
    * add_repository
    * del_environment
    * del_repository
    * execute_service
    * finalize_component
    * init_component
    * list_components
    * list_environments
    * list_keys
    * list_repositories
    * list_services
    * show_environment
    * show_key
    * show_repository

    fabuloso > 

Listing components
------------------

To list all the available `FABuloso` components run::

    fabuloso > list_components

    Available components are:
    fabuloso >

No components yet, so lets :ref:`add our first catalog <adding_catalog>`. Now you can list the new added components::

    fabuloso > list_components

    Available components are:
     * folsom.quantum_plugins
     * folsom.compute
     * folsom.nova
     * folsom.swift
     * folsom.mysql
     * folsom.rabbitmq
     * folsom.cinder
     * folsom.apache
     * folsom.glance
     * folsom.storage
     * folsom.fake
     * folsom.quantum
     * folsom.os
     * folsom.keystone

Deploying a component
---------------------

Now that we have some components we can perform our first *OpenStack* deployment. First we must :ref:`add a new environment <adding_environment>` in order to connect with the target host over *SSH*.


Initializing a component
^^^^^^^^^^^^^^^^^^^^^^^^

The first step to deploy a component is to :ref:`initialize it <initializing_component>`. The component initialization is where we customize our deployment using the so called *properties* (this is the way components are configurable in *FABuloso*).

So, run the following command and populate the prompted properties::

    fabuloso > init_component folsom.mysql test
    -(initializing folsom.mysql in environment test) Insert value for property 'drop_schema' [None]: 
    -(initializing folsom.mysql in environment test) Insert value for property 'cinder_password' [stackops]: c1nd3r
    -(initializing folsom.mysql in environment test) Insert value for property 'keystone_user' [keystone]: 
    -(initializing folsom.mysql in environment test) Insert value for property 'cinder_user' [cinder]: 
    -(initializing folsom.mysql in environment test) Insert value for property 'automation_password' [stackops]: 4ut0m4t10n
    -(initializing folsom.mysql in environment test) Insert value for property 'nova_user' [nova]: 
    -(initializing folsom.mysql in environment test) Insert value for property 'port' []: 
    -(initializing folsom.mysql in environment test) Insert value for property 'glance_user' [glance]: 

    ...

    -(initializing folsom.mysql in environment test) Insert value for property 'host' [localhost]: 
    fabuloso [folsom.mysql/test] >

.. note::

    To populate properties you can use a custom value or the default value given between `[ ]`.

Running a service
^^^^^^^^^^^^^^^^^

Right, the component is now initialized and customized for our needs. Now we can :ref:`execute a service <_executing_service>` in order to change the target machine state.

List the available services::

    fabuloso [folsom.mysql/test] > list_services
     * set_quantum
     * set_keystone
     * teardown
     * set_cinder
     * set_nova
     * install
     * set_glance
     * validate

Well, lets execute the `install` service::

    fabuloso [folsom.mysql/test] > execute_service install
    [10.0.0.2] sudo: DEBIAN_FRONTEND=noninteractive apt-get -q --yes -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install mysql-server
    [10.0.0.2] out: Reading package lists...
    [10.0.0.2] out: Building dependency tree...
    [10.0.0.2] out: Reading state information...
    [10.0.0.2] out: The following extra packages will be installed:
    [10.0.0.2] out:   libdbd-mysql-perl libdbi-perl libhtml-template-perl libnet-daemon-perl libplrpc-perl libterm-readkey-perl mysql-client-5.5
    [10.0.0.2] out:   mysql-client-core-5.5 mysql-server-5.5 mysql-server-core-5.5
    [10.0.0.2] out: Suggested packages:
    [10.0.0.2] out:   libipc-sharedcache-perl tinyca mailx
    [10.0.0.2] out: The following NEW packages will be installed:
    [10.0.0.2] out:   libdbd-mysql-perl libdbi-perl libhtml-template-perl libnet-daemon-perl libplrpc-perl libterm-readkey-perl mysql-client-5.5
    [10.0.0.2] out:   mysql-client-core-5.5 mysql-server mysql-server-5.5 mysql-server-core-5.5
    [10.0.0.2] out: ...

The `install` service has finished successfully. We can run another service, such as `validate` to check the expected machine state::

    fabuloso [folsom.mysql/test] > execute_service validate
    ...

    fabuloso [folsom.mysql/test] >

Finally, to end the component deployment, run::

    fabuloso [folsom.mysql/test] > finalize_component
    fabuloso >

And we are in the initial `FABuloso` prompt again. Ready to deploy whatever component.
