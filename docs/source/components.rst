Components
==========

A **component** is the fundamental configuration element in `FABuloso`. It's just a python module defining some functions and a `component.yml` (`yaml <http://yaml.org>`_) defining some `metadata` and `services`. A `service` is a list of functions from that python module that will be executed in the given order.

Component structure
-------------------

To see how a `component` looks like we're going to use the `nova` component from `<https://github.com/StackOps/fabuloso-catalog/tree/master/nova>`_.

component.yml
^^^^^^^^^^^^^

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
^^^^^^^

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
