FABuloso
========

**FABuloso** is a python tool to deploy `OpenStack <http://www.openstack.org>`_ using `Fabric <http://docs.fabfile.org/>`_. *FABuloso* manages configuration with **components** within **catalogs**.

A *component* is the most fundamental configuration element in FABuloso. Components are written in Python using Fabric and can be used to install software, edit its configuration files, create users, enable and start system services, and in short, do anything you could do through Fabric. In turn, a component is divided into *services* which accept **properties**.

A *catalog* is a collection of *components* with something in common to deploy an OpenStack architecture. For example, in an hypothetical *folsom* catalog we could have mysql, keystone, nova and so on, components.

Installation
------------

Just run::

    $ python setup.py install

License
-------

Apache 2.0
