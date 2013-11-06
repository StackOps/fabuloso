.. _fabuloso_shell:

Interactive shell
=================

*FABuloso* comes with an *interactive shell* to help working with it. The first step is to start the *shell*:

.. code-block:: bash

    $ fabuloso-shell

This opens the *FABuloso* shell with the ``fabuloso >`` prompt. You can type ``help`` to see all the available commands::

    fabuloso > help
    Available methods are:

    * add_environment
    * add_key
    * add_repository
    * del_environment
    * del_key
    * del_repository
    * execute_service
    * finalize_component
    * gen_key
    * init_component
    * list_components
    * list_environments
    * list_keys
    * list_repositories
    * list_services
    * show_environment
    * show_key
    * show_repository

Now, take a look at the sections bellow to see all these commands in action.


Catalogs
--------

Listing catalogs
^^^^^^^^^^^^^^^^

To list all catalogs run::

    fabuloso > list_repositories
    fabuloso >

If no catalogs were shown then it's time to add our first catalog.

.. _adding_catalog:

Adding a catalog
^^^^^^^^^^^^^^^^

We are going to add `<https://github.com/StackOps/fabuloso-catalog.git>`_  as the *folsom* catalog::

    fabuloso > add_repository folsom https://github.com/StackOps/fabuloso-catalog.git
    fabuloso >

.. note::

    You can also register a new *catalog* from a private git repository by passing an optional third argument with the name of one of the *FABuloso* :ref:`key pairs <key_pairs>`.

Now if we *list* our catalogs then we should see the new *folsom*::

    fabuloso > list_repositories
    +---------+------+--------------------------------------------------+
    |   Name  | Type |                       URL                        |
    +---------+------+--------------------------------------------------+
    |  folsom | git  | https://github.com/StackOps/fabuloso-catalog.git |
    +---------+------+--------------------------------------------------+
    fabuloso >

Showing a catalog
^^^^^^^^^^^^^^^^^

Showing a catalog will show us some info about it::

    fabuloso > show_repository folsom
    +----------+--------------------------------------------------+
    | Property |                      Value                       |
    +----------+--------------------------------------------------+
    |   url    | https://github.com/StackOps/fabuloso-catalog.git |
    |   type   |                       git                        |
    |   name   |                      folsom                      |
    +----------+--------------------------------------------------+
    fabuloso >

Removing a catalog
^^^^^^^^^^^^^^^^^^

We can remove a previously registered *catalog* by running::

    fabuloso > del_repository folsom
    fabuloso >


Components
----------

Listing components
^^^^^^^^^^^^^^^^^^

Assuming we have added the *folsom* catalog as described :ref:`here <adding_catalog>` we can see all its components by running::

    fabuloso > list_components
    +-------------------------+
    |           Name          |
    +-------------------------+
    |      folsom.apache      |
    |      folsom.cinder      |
    |      folsom.compute     |
    |       folsom.fake       |
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
    |       grizzly.fake      |
    |      grizzly.glance     |
    |     grizzly.keystone    |
    |            ...          |
    +-------------------------+
    fabuloso >

Also you can filter components by catalog **name** as follows::

    fabuloso > list_components grizzly

    Available components are:
    +------------------+
    |       Name       |
    +------------------+
    |  grizzly.apache  |
    |  grizzly.cinder  |
    | grizzly.compute  |
    |   grizzly.fake   |
    |  grizzly.glance  |
    | grizzly.keystone |
    |        ...       |
    +------------------+
    fabuloso >

.. note::

    *Components* names are always prefixed by the *catalog* name.

.. _initializing_component:

Initializing a component
^^^^^^^^^^^^^^^^^^^^^^^^

In order to work with a component we need to **initialize** it::

    fabuloso > init_component folsom.mysql testing
    fabuloso [folsom.mysql/testing] >

To *initialize* a component we need to pass the *component name* and the target *environment* where we would like to execute services on. Note that once initialized, the shell prompt will show that we are "inside" an initialized component.

Now we can :ref:`list <listing_services>` and :ref:`execute <executing_service>` services.

.. _finalizing_component:

Finalizing a component
^^^^^^^^^^^^^^^^^^^^^^

When you have finished working with a component you can run ``finalize_component`` to go back to the main *FABuloso* shell::

    fabuloso [folsom.mysql/testing] > execute_service install

    [...]

    fabuloso [folsom.mysql/testing] > finalize_component
    fabuloso >


Services
--------

.. _listing_services:

Listing services
^^^^^^^^^^^^^^^^

.. note::

    In order to **list** or **execute** services you need first to  :ref:`initialize the component <initializing_component>`.

To list the *component services* run::

    fabuloso [folsom.mysql/testing] > list_services
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
    fabuloso [folsom.mysql/testing] >

Well, let's execute some of these services.

.. _executing_service:

Executing a service
^^^^^^^^^^^^^^^^^^^

Run::

    fabuloso [folsom.mysql/testing] > execute_service install
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

    ...

    fabuloso [folsom.mysql/testing] >

.. note::

    Don't forget to :ref:`finalize the component <finalizing_component>` after you finished working with the *component*.


Environments
------------

Listing environments
^^^^^^^^^^^^^^^^^^^^

By default *FABuloso* comes with the ``localhost`` environment preconfigured, so the **list_environments** command will return only that environment::

    fabuloso > list_environments
    +-----------+----------+-----------+------+-----------+
    |    Name   | Username |    Host   | Port |  Key Name |
    +-----------+----------+-----------+------+-----------+
    | localhost | stackops | localhost |  22  | nonsecure |
    +-----------+----------+-----------+------+-----------+
    fabuloso >

Let's add a new environment.

.. _adding_environment:

Adding an environment
^^^^^^^^^^^^^^^^^^^^^

Run::

    fabuloso > add_environment
    -(Adding new environment)- Name: testing
    -(Adding new environment)- Remote username: stackops
    -(Adding new environment)- Remote host: 10.0.0.2
    -(Adding new environment)- Remote port: 22
    -(Adding new environment)- Ssh Key name: nonsecure
    +----------+-----------+
    | Property |   Value   |
    +----------+-----------+
    | username | stackops  |
    | key_name | nonsecure |
    |   host   | 10.0.0.2  |
    |   name   |  testing  |
    |   port   |     22    |
    +----------+-----------+
    fabuloso >

The **name** field is the identifier we're going to use to reference our *environment* when deploying some component. The remaining fields are the data used to connect over *SSH* to the target host (**username**, **host**, **port** and **key name**).

.. note::

    The **key name** should be an existent *FABuloso* keypair. See how to add a new keypair :ref:`here <adding_keypair>`.

Now listing keys should show the new added environment::

    fabuloso > list_environments
    +-----------+----------+-----------+------+-----------+
    |    Name   | Username |    Host   | Port |  Key Name |
    +-----------+----------+-----------+------+-----------+
    | localhost | stackops | localhost |  22  | nonsecure |
    |  testing  | stackops | 10.0.0.2  |  22  | nonsecure |
    +-----------+----------+-----------+------+-----------+
    fabuloso >

Showing an environment
^^^^^^^^^^^^^^^^^^^^^^

To see the values of a specific environment we can run::

    fabuloso > show_environment localhost
    +----------+-----------+
    | Property |   Value   |
    +----------+-----------+
    | username |  stackops |
    | key_name | nonsecure |
    |   host   | localhost |
    |   name   | localhost |
    |   port   |     22    |
    +----------+-----------+
    fabuloso >

Removing an environment
^^^^^^^^^^^^^^^^^^^^^^^

We can remove an environment from our *FABuloso* installation by running::

    fabuloso > del_environment testing
    fabuloso >


Keypairs
--------

Listing keypairs
^^^^^^^^^^^^^^^^

By default *FABuloso* comes with the *nonsecure* keypair. You can list keypairs to see it::

    fabuloso > list_keys
    +-----------+------------------------------------+----------------------------------------+
    |    Name   |               Key file             |               Pub file                 |
    +-----------+------------------------------------+----------------------------------------+
    | nonsecure | /etc/fabuloso/keys/nonsecureid_rsa | /etc/fabuloso/keys/nonsecureid_rsa.pub |
    +-----------+------------------------------------+----------------------------------------+
    fabuloso >

Showing a keypair
^^^^^^^^^^^^^^^^^

Also you can get the key info and contents by running::

    fabuloso > show_key nonsecure
    +----------+----------------------------------------+
    | Property |                  Value                 |
    +----------+----------------------------------------+
    | key_file |   /etc/fabuloso/keys/nonsecureid_rsa   |
    |   name   |                 nonsecure              |
    | pub_file | /etc/fabuloso/keys/nonsecureid_rsa.pub |
    +----------+----------------------------------------+
    fabuloso >

.. _adding_keypair:

Adding a keypair
^^^^^^^^^^^^^^^^

To add an existent *keypair* run::

    fabuloso > add_key
    -(Adding new keypair)-Name: my-secure-key
    -(Adding new keypair)-Key path: ~/my-secure-key
    -(Adding new keypair)-Pub path: ~/my-secure-key.pub
    +----------+----------------------------------------+
    | Property |                  Value                 |
    +----------+----------------------------------------+
    | key_file |    /etc/fabuloso/keys/my-secure-key    |
    |   name   |               my-secure-key            |
    | pub_file |  /etc/fabuloso/keys/my-secure-key.pub  |
    +----------+----------------------------------------+
    fabuloso >

Now list the keys to see the new added key::

    fabuloso > list_keys
    +---------------+------------------------------------+----------------------------------------+
    |      Name     |               Key file             |               Pub file                 |
    +---------------+------------------------------------+----------------------------------------+
    |   nonsecure   | /etc/fabuloso/keys/nonsecureid_rsa | /etc/fabuloso/keys/nonsecureid_rsa.pub |
    +---------------+------------------------------------+----------------------------------------+
    | my-secure-key |  /etc/fabuloso/keys/my-secure-key  |  /etc/fabuloso/keys/my-secure-key.pub  |
    +---------------+------------------------------------+----------------------------------------+
    fabuloso >

Generating a keypair
^^^^^^^^^^^^^^^^^^^^

To generate a new *keypair* run::

    fabuloso > gen_key my-new-key
    +----------+-----------------------------------+
    | Property |              Value                |
    +----------+-----------------------------------+
    | key_file |   /etc/fabuloso/keys/my-new-key   |
    |   name   |           my-new-key              |
    | pub_file | /etc/fabuloso/keys/my-new-key.pub |
    +----------+-----------------------------------+
    fabuloso >

Removing a keypair
^^^^^^^^^^^^^^^^^^

In order to remove an existing *keypair* just type the ``del_key`` command followed by the key name::

    fabuloso > del_key my-secure-key
    fabuloso >
