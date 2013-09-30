Services
========

A **service** is the smallest element in a *FABuloso component*. A *component* should have atleast one *service*. *Services* are defined in the component *metadata* and could accept *properties*. To learn more about how to write a component you would take a look at :ref:`the component structure <component_structure>`.

.. note::

    In order to **list** or **execute** services you need first to  :ref:`initialize the component <initializing_component>`.


.. _listing_services:

Listing services
----------------

To list the *component services* run::

    fabuloso [folsom.mysql/testing] > list_services

    Available services are:
     * set_quantum
     * set_keystone
     * teardown
     * set_cinder
     * set_automation
     * set_accounting
     * set_nova
     * install
     * set_glance
     * validate
     * set_portal
    fabuloso [folsom.mysql/testing] >

Well, let's execute some of these services.


.. _executing_service:

Executing a service
-------------------

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
