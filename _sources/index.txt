.. FABuloso documentation master file, created by
   sphinx-quickstart on Wed Sep 25 14:17:30 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

FABuloso: OpenStack deployments (Built by StackOps)
===================================================

**FABuloso** is a python tool to easily organize and deploy an `OpenStack <http://www.openstack.org>`_ architecture using `Fabric <http://docs.fabfile.org/>`_. *FABuloso* manages configuration with **components** within **catalogs** (take a look at the :ref:`overview <overview>` for more info about the different parts of *FABuloso*).

.. image:: images/fabuloso.png
    :alt: FABuloso architecture
    :align: center

Why another deployment tool for OpenStack?
------------------------------------------

We know there are really cool tools out there, but we think we have to focus on doing things **simpler** and **easier**. That's the reason why we started developing *FABuloso* to deploy OpenStack clouds at *StackOps*. We think the OpenStack community suffers of the 'Golden Hammer' syndrome about all these nice deployment tools. FABuloso only does what it does, and it does it very well.

About StackOps
--------------

The **OpenStack™** open source platform offers cloud computing solutions for companies of all sizes and industries. Thanks to contributions from developers from around the world, **its technology improves every day**. For this reason, StackOps has always trusted it to provide service to our customers.

However, many of our potential customers found **the platform difficult to use**.

For this reason, in 2010 StackOps created **StackOps Community Distro©**, inception of all the suite of StackOps products, the distribution package that makes it **easy to deploy clouds with OpenStack™ and eliminates the technological barrier** for the end user.

And it worked.

The appearance of StackOps© caused such a storm that StackOps achieved `extensive media coverage <http://www.eweek.com/c/a/Cloud-Computing/StackOps-Distribution-Offers-an-Introduction-to-OpenStack-Cloud-679865/>`_, blogs, `books <http://shop.oreilly.com/product/0636920021674.do>`_ and of course **thousands of downloads**. This product offered real value to people. And since then there have been new users every day. For this reason, the product improved in 2013; **StackOps 360©**, a solution for **managing your own clouds and those of third parties effortlessly with OpenStack™**.

STACKOPS 360: Effortless OpenStack™
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**StackOps 360®** is a package of four products bundled on top of our popular StackOps distro built on *FABuloso*, enabling easy management, of both public and private clouds, with complete functionality:

    * Create computing clouds
    * Automate your processes
    * Control resource usage
    * Offer your customers a pay‐per-use solution
    * Provide the best user experience

So when you are ready to get your *FABuloso* flavored OpenStack deployment to an enterprise-grade, fully supported solution, `download StackOps360 <http://stackops.com/products-services>`_ and don’t forget to `contact us <http://stackops.com/contact>`_.

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
