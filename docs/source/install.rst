Installation
============

From github
-----------

We recommend to install *FABuloso* into a *virtualenv*:

.. code-block:: bash

    $ virtualenv .venv
    $ source .venv/bin/activate
    (.venv)$

You can install the latest `FABuloso` from the `github repo <https://github.com/StackOps/fabuloso>`_ using pip:

.. code-block:: bash

    (.venv)$ pip install -e git+git://github.com/StackOps/fabuloso.git#egg=fabuloso

Or manually:

.. code-block:: bash

    (.venv)$ git clone git://github.com/StackOps/fabuloso.git
    (.venv)$ cd fabuloso
    (.venv)$ python setup.py install
