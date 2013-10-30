Installation
============


From Apt
--------

*FABuloso* can be installed through the *StackOps* apt repos. Just add the repos to your ``sources.list``:

.. code-block:: bash

    echo 'deb http://repos.stackops.net/ folsom main' >> /etc/apt/sources.list
    echo 'deb http://repos.stackops.net/ folsom-updates main' >> /etc/apt/sources.list
    echo 'deb http://repos.stackops.net/ folsom-security main' >> /etc/apt/sources.list
    echo 'deb http://repos.stackops.net/ folsom-backports main' >> /etc/apt/sources.list

And now you can run ``update`` and install *python-fabuloso*:

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install python-fabuloso


From PyPI
---------

To install *FABuloso* from the public Python Package index just run:

.. code-block:: bash

    $ pip install fabuloso


From Github
-----------

We recommend to install *FABuloso* into a *virtualenv*:

.. code-block:: bash

    $ virtualenv .venv
    $ source .venv/bin/activate
    (.venv)$

You can install the latest *FABuloso* from the `github repo <https://github.com/StackOps/fabuloso>`_ using pip:

.. code-block:: bash

    (.venv)$ pip install -e git+git://github.com/StackOps/fabuloso.git#egg=fabuloso

Or manually:

.. code-block:: bash

    (.venv)$ git clone git://github.com/StackOps/fabuloso.git
    (.venv)$ cd fabuloso
    (.venv)$ python setup.py install
