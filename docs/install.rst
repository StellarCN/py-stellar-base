.. _install:

************
Installation
************

Via pipenv or pip (Recommended)
===============================

To install py-stellar-sdk, use pipenv to install the module:

.. code-block:: text

    pipenv install stellar-sdk

If you're not using `pipenv <https://docs.pipenv.org/>`_, you should.
Otherwise, you can install it via plain old ``pip``. More on installing Python
and dependencies can be found over in the `Hitchhiker's Guide to Python
<http://docs.python-guide.org/en/latest/starting/installation/>`_.

Via Source Code
===============

Please use the code on pypi whenever possible. The latest code may be unstable.

You can install it from source code via pip:

.. code-block:: bash

    pip install -U git+git://github.com/StellarCN/py-stellar-base

And you can always clone `the repository <https://github.com/StellarCN/py-stellar-base>`_ directly, and install it locally:

.. code-block:: bash

    git clone https://github.com/StellarCN/py-stellar-base.git
    cd py-stellar-base
    pip install .
