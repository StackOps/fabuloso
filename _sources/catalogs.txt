Catalogs
========

A **catalog** in *FABuloso* is a collection of *components* with certain characteristics in common. For example, a sample catalog could be *folsom* which would contain all the components needed to deploy OpenStack Folsom.

.. warning::

    Currently we only manage *catalogs* as git repositories. In the future more options will be supported.


Listing catalogs
----------------

To list all catalogs run::

    fabuloso > list_repositories
    fabuloso >

If no catalogs were shown then it's time to add our first catalog.


.. _adding_catalog:

Adding a catalog
----------------

We are going to add `<https://github.com/StackOps/fabuloso-catalog.git>`_  as the *folsom* catalog::

    fabuloso > add_repository folsom https://github.com/StackOps/fabuloso-catalog.git
    fabuloso >

.. warning::

    If you want to register a *catalog* from a private repo (using ssh for example) you should be able to clone that repo from the machine where *FABuloso* is installed. In the future secure connections could be made using  the *FABuloso* keypairs, but currently is not supported. Instead you can forward the authentication agent when connecting over SSH to the *FABuloso* machine.

Now if we *list* our catalogs then we should see the new *folsom*::

    fabuloso > list_repositories
     * folsom
    fabuloso >


Showing a catalog
-----------------

Showing a catalog will show us some info about it::

    fabuloso > show_repository folsom
     * Name: folsom
     * Type: git
     * Url: https://github.com/StackOps/fabuloso-catalog.git
    fabuloso >


Removing a catalog
------------------

We can remove a previously registered *catalog* by running::

    fabuloso > del_repository folsom
    fabuloso >
