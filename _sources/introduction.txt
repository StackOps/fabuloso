.. _introduction:

Introduction
============

**FABuloso** is a python tool to easily organize and deploy an `OpenStack <http://www.openstack.org>`_ architecture using `Fabric <http://docs.fabfile.org/>`_. *FABuloso* manages configuration with **components** within **catalogs**.


Catalogs
--------

A **catalog** in *FABuloso* is a collection of *components* with certain characteristics in common to deploy an OpenStack architecture. For example, a sample catalog could be *folsom* which would contain all the components needed to deploy OpenStack Folsom.

.. warning::

    Currently we only manage *catalogs* as git repositories. In the future more options will be supported.


Components
----------

A **component** is the most fundamental configuration element in *FABuloso*. It's just a python module defining some functions and a *component.yml* (`yaml <http://yaml.org>`_) defining some *metadata* and *services*. A *service* is a list of functions from that python module that will be executed in the given order.

Components are written in Python using Fabric and can be used to install software, edit its configuration files, create users, enable and start system services, and in short, do anything you could do through Fabric.

.. _component_structure:

Component structure
^^^^^^^^^^^^^^^^^^^

To see how a `component` looks like we're going to use the `nova` component from `<https://github.com/StackOps/fabuloso-catalog/tree/master/nova>`_.

component.yml
"""""""""""""

.. code-block:: yaml

    name: nova
    file: nova.py
    description: Operations over OpenStack Nova service
         
    Services:
        - name: install
          description: Install OpenStack Nova from ubuntu packages
          methods:
              - install
              - set_config_file
        - name: nova_properties
          description: Set properties of the Nova service
          methods:
              - nova_properties
        - name: start
          description: Start Nova Service
          methods:
              - start
        - name: validate
          description: Validates nova to operate with it
          methods:
              - validate_database
              - validate_credentials
              - validate_rabbitmq

Required fields are:

* name: The component name
* file: The path to the python module where service methods are
* description: A brief description about the component
* Services: A list of services that this component exposes. At least one service is needed.

A service requires the following fields:

* name: The name we will use to execute this service
* description: A brief description about the service behavior
* methods: A list of function names from the python module


nova.py
"""""""

.. code-block:: python

    def install(cluster=False):
        """Generate nova configuration. Execute on both servers"""

        package_ensure('nova-api')
        package_ensure('nova-cert')
        package_ensure('nova-common')

        # ...


    def set_config_file(management_ip, user='nova', password='stackops',
                        auth_host='127.0.0.1',
                        auth_port='35357', auth_protocol='http',
                        mysql_username='nova', mysql_password='stackops',
                        mysql_schema='nova', tenant='service',
                        mysql_host='127.0.0.1',
                        mysql_port='3306'):

        f = '/etc/nova/api-paste.ini'

        sudo('sed -i "/volume/d" %s' % f)
        sudo("sed -i 's/admin_password.*$/admin_password = %s/g' %s"
             % (password, f))

        # ...

During the :ref:`component initialization <initializing_component>` `FABuloso` will ask you for the values of `properties`. Properties are the arguments of the `services` methods.


Services
--------

A **service** is the smallest element in a *FABuloso component*. A *component* should have atleast one *service*. *Services* are defined in the component *metadata* and could accept *properties*. To learn more about how to write a component you would take a look at :ref:`the component structure <component_structure>`.


Environments
------------

**Environments** contain the information used by *FABuloso* to securely connect over SSH to a *target host*.


Key Pairs
---------

*FABuloso* can manage **keypairs** in order to securely connect to the target hosts and execute *services*. *Keypairs* will be referenced later when :ref:`adding environments <adding_environment>`.
