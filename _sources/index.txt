.. FABuloso documentation master file, created by
   sphinx-quickstart on Wed Sep 25 14:17:30 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FABuloso: OpenStack deployments
===============================

**FABuloso** is a python tool to easily organize and deploy an `OpenStack <http://www.openstack.org>`_ architecture using `Fabric <http://docs.fabfile.org/>`_. *FABuloso* manages configuration with **components** within **catalogs** (take a look at the :ref:`overview <overview>` for more info about the different parts of *FABuloso*).

.. image:: images/fabuloso.png
    :alt: FABuloso architecture
    :align: center

Why another deployment tool for OpenStack?
------------------------------------------

We know there are really cool tools out there, but we think we have to focus on doing things **simpler** and **easier**. That's because we started developing *FABuloso* to deploy OpenStack clouds at *StackOps*. We think the OpenStack community suffers of the 'Golden Hammer' syndrome about all these nice deployment tools. FABuloso only does what it does, and it does it very well.

Why Fabric?
-----------

*Fabric* is a Python (>= 2.5) library and command-line tool for streamlining the use of SSH for *application deployment* or *systems administration tasks*. It provides a basic suite of operations for executing *local* or *remote* shell commands (normally or via sudo) and *uploading/downloading* files, as well as some auxiliary functionality that helps in such tasks. You can learn more from `its website <http://docs.fabfile.org>`_.

*Fabric* helps us achieve our goals by providing us with a thin layer to communicate with the target server and execute commands on it, with the only requirement of having a base OS installed with a SSH server configured and running. Moreover, being a **push** system gives us full control on the deployment process.

Which OS are supported?
-----------------------

Currently, we provide support for `Ubuntu 12.04 LTS <http://releases.ubuntu.com/12.04>`_ to all our :ref:`catalogs <catalogs>`, but support for more ubuntu versions and other Linux systems is planned in future releases.

Which OpenStack versions are supported?
---------------------------------------

Right now `Folsom <http://www.openstack.org/software/folsom/>`_ is actively supported and we are working to also support `Grizzly <http://www.openstack.org/software/grizzly/>`_ and `Havana <http://www.openstack.org/software/havana/>`_ as soon as possible. Future OpenStack versions will be supported as well.

Where can I get help?
---------------------

To ask for *help*, *propose* new features, *report* bugs or whatever you have to tell about *FABuloso* you can use our discussion mailing at `https://groups.google.com/d/forum/fabuloso-discussion <https://groups.google.com/d/forum/fabuloso-discussion>`_.


User Guide
==========

Once you understand what *FABuloso* does, you can see the `installation <install.html>`_ and `quickstart <quickstart.html>`_ guides to start deploying your first OpenStack architecture.

.. toctree::
    :maxdepth: 2

    reference
    catalogs
    examples


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
