.. FABuloso documentation master file, created by
   sphinx-quickstart on Wed Sep 25 14:17:30 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FABuloso's documentation!
====================================

**FABuloso** is a python tool to deploy `OpenStack <http://www.openstack.org>`_ using `Fabric <http://docs.fabfile.org/>`_. `FABuloso` is divided into `components` within `catalogs`.

A `component` is the most fundamental configuration element in FABuloso. Components are written in Python using Fabric and can be used to install software, edit its configuration files, create users, enable and start system services, and in short, do anything you could do through Fabric. In turn, a component is divided into `services` which accept `properties`.

A `catalog` is a collection of `components` with something in common to deploy an OpenStack architecture. For example, in an hypothetical `folsom` catalog we could have mysql, keystone, nova and so on, components.

Now you can take a look at the `installation <install.html>`_ and `quickstart <quickstart.html>`_ guides.

Contents:

.. toctree::
    :maxdepth: 2

    install
    quickstart


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
