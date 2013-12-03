Python API
==========

*FABuloso* also comes with a *Python API* that can be used to automate some tasks from a custom Python script.

Let's import ``fabuloso`` from you Python interpreter::

    >>> import fabuloso
    >>> 

The core logic of the *Python API* resides in the ``Fabuloso`` class, so before start working with the *API* we need to instantiate it::

    >>> FAB = fabuloso.Fabuloso()
    >>> FAB
    <fabuloso.Fabuloso object at 0x7feec5abf4d0>
    >>>

Now we can perform the following operations.


Catalogs
--------

Listing catalogs
^^^^^^^^^^^^^^^^

The ``list_repositories`` method returns a list of ``Repository`` objects::

    >>> for catalog in FAB.list_repositories():
    ...     print catalog['name'], catalog['type'], catalog['url']
    ...
    folsom git https://github.com/StackOps/fabuloso-catalog.git
    >>>

Adding a catalog
^^^^^^^^^^^^^^^^

To add a new *catalog* we can use the ``add_repository`` method, which accepts the repo **name** and **url** as arguments::

    >>> FAB.add_repository('grizzly', 'https://github.com/StackOps/fabuloso-catalog-grizzly.git')
    >>>

You can also add a new *catalog* from a specific git branch::

    >>> FAB.add_repository('grizzly', 'https://github.com/StackOps/fabuloso-catalog-grizzly.git', branch='development')
    >>>

Furthermore, you can clone the repository using a FABuloso registered ssh key::

    >>> FAB.add_repository('grizzly', 'https://github.com/StackOps/fabuloso-catalog-grizzly.git', auth_keys='my-secure-key')
    >>>

Removing a catalog
^^^^^^^^^^^^^^^^^^

To remove a *catalog* use the ``delete_repository`` method with the **name** of the catalog you want to remove::

    >>> FAB.delete_repository('grizzly')
    >>>


Components
----------

Listing components
^^^^^^^^^^^^^^^^^^

To get all the catalogs components just run::

    >>> for component in FAB.list_components():
    ...     print component
    ...
    <Component:folsom.quantum_plugins>
    <Component:folsom.compute>
    <Component:folsom.nova>
    <Component:folsom.swift>
    <Component:folsom.mysql>
    [...]
    >>>

You can also list components by *catalog* by passing the catalog **name** as the first ``list_components`` method argument::

    >>> for component in FAB.list_components('grizzly'):
    ...     print component
    ...
    <Component:grizzly.quantum_plugins>
    <Component:grizzly.compute>
    <Component:grizzly.nova>
    [...]
    >>>

Initializing a component
^^^^^^^^^^^^^^^^^^^^^^^^

To *initialize a component* you should call the ``init_component`` method with the component **name**, **properties** and target **environment**::

    >>> nova = FAB.init_component('folsom.nova', properties_dict, environment)
    >>> print nova
    <Component:folsom.nova>
    >>>

The ``properties_dict`` argument passed to the ``init_component`` method above should be a *dict* containing all the properties for the given component. This could be the generated with the ``get_template`` method explained below.

Component template
^^^^^^^^^^^^^^^^^^

To generate a template dict with the all component properties and its default values we can call the ``get_template`` method with the component name as the first positional argument::

    >>> FAB.get_template('folsom.nova')
    {'admin_token': '',
     'auth_host': '127.0.0.1',
     'auth_port': '35357',
     'auth_protocol': 'http',
     'cluster': False,
     'database_type': '',
     'drop_schema': None,
     'endpoint': '',
     'host': '',
     'install_database': None,
     'management_ip': '',
     'mysql_host': '127.0.0.1',
     'mysql_password': 'stackops',
     'mysql_port': '3306',
     'mysql_schema': 'nova',
     'mysql_username': 'nova',
     'password': '',
     'port': '',
     'props': '',
     'rpassword': None,
     'rport': None,
     'ruser': None,
     'schema': '',
     'service_type': '',
     'tenant': '',
     'user': '',
     'username': '',
     'virtual_host': None}
     >>>

The returned dict can be stored, modified and finally used to *initialize a component* and then run some of its services.


Services
--------

Executing a service
^^^^^^^^^^^^^^^^^^^

In order to **execute a service** you first need to have an initialized component (see above). The *component* should have a *method* for each defined *service*, so to execute a service you should call a method with the service *name*::

    >>> nova.install()
    [localhost] run: dpkg-query -W -f='${Status} ' nova-api && echo OK;true
    [localhost] sudo: apt-get install -y nova-api
    [localhost] out: ...

    [...]

    >>>


Environments
------------

Listing environments
^^^^^^^^^^^^^^^^^^^^

To list all the available *environments* execute the ``list_environments`` method::

    >>> for env in FAB.list_environments():
    ...     print env['name'], env['key_name'], env['host'], env['port'], env['username']
    localhost nonsecure localhost 22 stackops
    >>>


Adding an environment
^^^^^^^^^^^^^^^^^^^^^

In order to add a new *environment* you should call the ``add_environment`` with the environemnt **name** and the **username**, **host**, **port** and **key_name** arguments::

    >>> FAB.add_environment('testing', 'stackops', 'localhost', 2222, 'nonsecure')
    <Environment 'testing': user=stackops, host=localhost, port=2222, key=nonsecure>
    >>>

Removing an environment
^^^^^^^^^^^^^^^^^^^^^^^

To *delete* an existent *environment* execute the ``delete_environment`` method with the environment **name** as argument::

    >>> FAB.delete_environment('testing')
    >>>


Keypairs
--------

Listing keypairs
^^^^^^^^^^^^^^^^

To list all the available *keypairs* run the ``list_keys`` method::

    >>> FAB.list_keys()
    [<SshKey: nonsecure, /etc/fabuloso/keys/nonsecureid_rsa, /etc/fabuloso/keys/nonsecureid_rsa.pub>]
    >>>

Showing a keypair
^^^^^^^^^^^^^^^^^

To get an especific *keypair* run the ``get_key`` method with the key **name** as argument::

    >>> FAB.get_key('nonsecure')
    <SshKey: nonsecure, /etc/fabuloso/keys/nonsecureid_rsa, /etc/fabuloso/keys/nonsecureid_rsa.pub>

Adding a keypair
^^^^^^^^^^^^^^^^

If you want to add a new *keypair* you need to call the ``add_key`` method with the key **name**, **key_path** and **pub_path** values as arguments::

    >>> FAB.add_key('my-secure-key', '~/secureid', '~/secureid.pub')
    >>>

Removing a keypair
^^^^^^^^^^^^^^^^^^

Finally, to remove a *keypair* use the ``delete_key`` method with the key **name** as argument::

    >>> FAB.delete_key('my-secure-key')
    >>>
