.. _fabuloso_shell:

CLI
===

*FABuloso* comes with a *command-line interface* in addition to the :ref:`interactive shell <fabuloso_shell>` to ease the automation of different *FABuloso* tasks within a *shell script*.

First of all, run ``fabuloso`` without arguments to see all available commands:

.. code-block:: bash

    $ fabuloso
    Usage:
        fabuloso [--debug] list_repositories
        fabuloso [--debug] show_repository <name>
        fabuloso [--debug] add_repository <name> <url>
        fabuloso [--debug] del_repository <name>
        fabuloso [--debug] list_components [<name>]
        fabuloso [--debug] list_services [--environment=<name>]
                                         <component>
        fabuloso [--debug] execute_service [--environment=<name>]
                                           [--properties=<file>]...
                                           <component> <service>
        fabuloso [--debug] list_environments
        fabuloso [--debug] show_environment <name>
        fabuloso [--debug] add_environment <name> <username> <host> <port> <key>
        fabuloso [--debug] del_environment <name>
        fabuloso [--debug] list_keys
        fabuloso [--debug] show_key <name>
        fabuloso [--debug] add_key <name> <key_path> <pub_path>
        fabuloso [--debug] gen_key <name>
        fabuloso [--debug] del_key <name>
    $

Now, take a look at the sections bellow to see all these commands in action.


Catalogs
--------

Listing catalogs
^^^^^^^^^^^^^^^^

To list all catalogs run::

    $ fabuloso list_repositories
    $

If no catalogs were shown then it's time to add our first catalog.

Adding a catalog
^^^^^^^^^^^^^^^^

We are going to add `<https://github.com/StackOps/fabuloso-catalog.git>`_  as the *folsom* catalog::

    $ fabuloso add_repository folsom https://github.com/StackOps/fabuloso-catalog.git

Now if we *list* our catalogs then we should see the new *folsom*::

    $ fabuloso list_repositories
    +---------+------+--------------------------------------------------+
    |   Name  | Type |                       URL                        |
    +---------+------+--------------------------------------------------+
    |  folsom | git  | https://github.com/StackOps/fabuloso-catalog.git |
    +---------+------+--------------------------------------------------+
    $

Showing a catalog
^^^^^^^^^^^^^^^^^

Showing a catalog will show us some info about it::

    $ fabuloso show_repository folsom
    +----------+--------------------------------------------------+
    | Property |                      Value                       |
    +----------+--------------------------------------------------+
    |   url    | https://github.com/StackOps/fabuloso-catalog.git |
    |   type   |                       git                        |
    |   name   |                      folsom                      |
    +----------+--------------------------------------------------+
    $

Removing a catalog
^^^^^^^^^^^^^^^^^^

We can remove a previously registered *catalog* by running::

    $ fabuloso del_repository folsom


Components
----------

Listing components
^^^^^^^^^^^^^^^^^^

Assuming we have added the *folsom* catalog as described :ref:`here <adding_catalog>` we can see all its components by running::

    $ fabuloso list_components
    +-------------------------+
    |           Name          |
    +-------------------------+
    |      folsom.apache      |
    |      folsom.cinder      |
    |      folsom.compute     |
    |      folsom.glance      |
    |     folsom.keystone     |
    |       folsom.mysql      |
    |       folsom.nova       |
    |        folsom.os        |
    |      folsom.quantum     |
    |  folsom.quantum_plugins |
    |     folsom.rabbitmq     |
    |      folsom.storage     |
    |       folsom.swift      |
    |      grizzly.apache     |
    |      grizzly.cinder     |
    |     grizzly.compute     |
    |            ...          |
    +-------------------------+
    $

We also can filter components by catalog **name** as follows::

    $ fabuloso list_components grizzly
    +-------------------------+
    |           Name          |
    +-------------------------+
    |      grizzly.apache     |
    |      grizzly.cinder     |
    |     grizzly.compute     |
    |       grizzly.fake      |
    |      grizzly.glance     |
    |     grizzly.keystone    |
    |      grizzly.mysql      |
    |       grizzly.nova      |
    |        grizzly.os       |
    |     grizzly.quantum     |
    | grizzly.quantum_plugins |
    |     grizzly.rabbitmq    |
    |     grizzly.storage     |
    |      grizzly.swift      |
    +-------------------------+
    $


Services
--------

Listing services
^^^^^^^^^^^^^^^^

To list the *component services* run::

    $ fabuloso list_services folsom.mysql
    +----------------+
    |      Name      |
    +----------------+
    |  set_quantum   |
    |  set_keystone  |
    |    teardown    |
    |   set_cinder   |
    | set_automation |
    | set_accounting |
    |    set_nova    |
    |    install     |
    |   set_glance   |
    |    validate    |
    |   set_portal   |
    +----------------+
    $

Well, let's execute some of these services.

Executing a service
^^^^^^^^^^^^^^^^^^^

Run::

    $ fabuloso execute_service folsom.mysql install
    [localhost] sudo: echo mysql-server-5.5 mysql-server/root_password password stackops | debconf-set-selections
    [localhost] sudo: echo mysql-server-5.5 mysql-server/root_password_again password stackops | debconf-set-selections
    [localhost] sudo: echo mysql-server-5.5 mysql-server/start_on_boot boolean true | debconf-set-selections
    [localhost] run: dpkg-query -W -f='${Status} ' mysql-server && echo OK;true
    [localhost] out: install ok installed OK
    [localhost] out:

    [localhost] run: dpkg-query -W -f='${Status} ' python-mysqldb && echo OK;true
    [localhost] out: install ok installed OK
    [localhost] out:

    [localhost] sudo: nohup service mysql stop

    [...]

    $


Environments
------------

Listing environments
^^^^^^^^^^^^^^^^^^^^

By default *FABuloso* comes with the ``localhost`` environment preconfigured, so the **list_environments** command will return only that environment::

    $ fabuloso list_environments
    +-----------+----------+-----------+------+-----------+
    |    Name   | Username |    Host   | Port |  Key Name |
    +-----------+----------+-----------+------+-----------+
    | localhost | stackops | localhost |  22  | nonsecure |
    +-----------+----------+-----------+------+-----------+
    $

Adding an environment
^^^^^^^^^^^^^^^^^^^^^

Run the ``add_environment`` command with the environment **name**, **username**, **host**, **port** and **key**::

    $ fabuloso add_environment testing stackops 10.0.0.2 22 nonsecure
    +----------+-----------+
    | Property |   Value   |
    +----------+-----------+
    | username |  stackops |
    | key_name | nonsecure |
    |   host   |  10.0.0.2 |
    |   name   |  testing  |
    |   port   |     22    |
    +----------+-----------+
    $

Showing an environment
^^^^^^^^^^^^^^^^^^^^^^

To see the values of a specific environment we can run::

    $ fabuloso show_environment localhost
    +----------+-----------+
    | Property |   Value   |
    +----------+-----------+
    | username |  stackops |
    | key_name | nonsecure |
    |   host   | localhost |
    |   name   | localhost |
    |   port   |     22    |
    +----------+-----------+
    $

Removing an environment
^^^^^^^^^^^^^^^^^^^^^^^

We can remove an environment from our *FABuloso* installation by running::

    $ fabuloso del_environment testing
    $


Keypairs
--------

Listing keypairs
^^^^^^^^^^^^^^^^

You can list keypairs to see it::

    $ fabuloso list_keys
    +-----------+------------------------------------+----------------------------------------+
    |    Name   |               Key file             |               Pub file                 |
    +-----------+------------------------------------+----------------------------------------+
    | nonsecure | /etc/fabuloso/keys/nonsecureid_rsa | /etc/fabuloso/keys/nonsecureid_rsa.pub |
    +-----------+------------------------------------+----------------------------------------+
    $

Showing a keypair
^^^^^^^^^^^^^^^^^

Also you can get the key info and contents by running::

    $ fabuloso show_key nonsecure
    +----------+----------------------------------------+
    | Property |                  Value                 |
    +----------+----------------------------------------+
    | key_file |   /etc/fabuloso/keys/nonsecureid_rsa   |
    |   name   |                 nonsecure              |
    | pub_file | /etc/fabuloso/keys/nonsecureid_rsa.pub |
    +----------+----------------------------------------+
    $

Adding a keypair
^^^^^^^^^^^^^^^^

To add an existent *keypair* run::

    $ fabuloso add_key my-secure-key ~/my-secure-key ~/my-secure-key.pub
    +----------+----------------------------------------+
    | Property |                  Value                 |
    +----------+----------------------------------------+
    | key_file |    /etc/fabuloso/keys/my-secure-key    |
    |   name   |               my-secure-key            |
    | pub_file |  /etc/fabuloso/keys/my-secure-key.pub  |
    +----------+----------------------------------------+
    $

Now list the keys to see the new added key::

    $ fabuloso list_keys
    +---------------+------------------------------------+----------------------------------------+
    |      Name     |               Key file             |               Pub file                 |
    +---------------+------------------------------------+----------------------------------------+
    |   nonsecure   | /etc/fabuloso/keys/nonsecureid_rsa | /etc/fabuloso/keys/nonsecureid_rsa.pub |
    +---------------+------------------------------------+----------------------------------------+
    | my-secure-key |  /etc/fabuloso/keys/my-secure-key  |  /etc/fabuloso/keys/my-secure-key.pub  |
    +---------------+------------------------------------+----------------------------------------+
    $

Generating a keypair
^^^^^^^^^^^^^^^^^^^^

You can also generate a completely new *keypair* with the ``gen_key`` command::

    $ fabuloso gen_key my-new-key
    +----------+-----------------------------------+
    | Property |              Value                |
    +----------+-----------------------------------+
    | key_file |   /etc/fabuloso/keys/my-new-key   |
    |   name   |           my-new-key              |
    | pub_file | /etc/fabuloso/keys/my-new-key.pub |
    +----------+-----------------------------------+
    $

Removing a keypair
^^^^^^^^^^^^^^^^^^

In order to remove an existing *keypair* use the ``del_key`` command followed by the key name::

    $ fabuloso del_key my-secure-key
    $
