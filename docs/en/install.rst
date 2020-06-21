.. _install:

************
Installation
************

Via pipenv or pip
===============================

To install py-stellar-sdk, use pipenv to install the module:

.. code-block:: text

    pipenv install stellar-sdk==2.6.1

If you're not using `pipenv <https://docs.pipenv.org/>`_, you should.
Otherwise, you can install it via plain old `pip <https://pip.pypa.io/en/stable/quickstart/>`_. More on installing Python
and dependencies can be found over in the `Hitchhiker's Guide to Python
<http://docs.python-guide.org/en/latest/starting/installation/>`_.

Via Source Code
===============

Please use the code on pypi whenever possible. The latest code may be unstable.

You can clone `the repository <https://github.com/StellarCN/py-stellar-base>`_ directly, and install it locally:

.. code-block:: bash

    git clone https://github.com/StellarCN/py-stellar-base.git
    cd py-stellar-base
    git checkout 2.6.1
    pip install .
