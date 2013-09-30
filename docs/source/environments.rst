Environments
============

**Environments** contain the information used by *FABuloso* to securely connect over SSH to a *target host*.


Listing environments
--------------------

By default *FABuloso* does not come with a preconfigured environment, so the **list_environments** command will return nothing::

    fabuloso > list_environments
    fabuloso >

Let's add a new environment.


.. _adding_environment:

Adding an environment
--------------------

Run::

    fabuloso > add_environment
    -(Adding new environment)- Name: testing
    -(Adding new environment)- Remote username: stackops
    -(Adding new environment)- Remote host: 10.0.0.2
    -(Adding new environment)- Remote port: 22
    -(Adding new environment)- Ssh Key name: nonsecure
    fabuloso >

The **name** field is the identifier we're going to use to reference our *environment* when deploying some component. The remaining fields are the data used to connect over *SSH* to the target host (**username**, **host**, **port** and **key name**).

.. note::

    The **key name** should be an existent *FABuloso* keypair. See how to add a new keypair :ref:`here <adding_keypair>`.

Now listing keys should show the new added environment::

    fabuloso > list_environments
     * testing
    fabuloso >


Showing an environment
----------------------

To see the values of a specific environment we can run::

    fabuloso > show_environment testing
     * Name: testing
     * Username: stackops
     * Host: 10.0.0.2
     * Port: 22
     * Key: nonsecure
    fabuloso >


Removing an environment
-----------------------

We can remove an environment from our *FABuloso* installation by running::

    fabuloso > del_environment testing
    fabuloso >
