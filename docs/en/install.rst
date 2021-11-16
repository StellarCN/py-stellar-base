.. _install:

************
Installation
************

Via pip
===============================

Use pip to install and update py-stellar-base:

.. code-block:: text

    pip install -U stellar-sdk

The py-stellar-base release follows `Semantic Versioning 2.0.0 <https://semver.org/>`_,
and I strongly recommend that you specify its major version number
in the dependency file to avoid the unknown effects of a corrupt update.
More on installing Python and dependencies can be found over in the `Hitchhiker's Guide to Python
<http://docs.python-guide.org/en/latest/starting/installation/>`_.

Via Source Code
===============

Please use the code on pypi whenever possible. The latest code may be unstable.

You can clone `the repository <https://github.com/StellarCN/py-stellar-base>`_ directly, and install it locally:

.. code-block:: bash

    git clone https://github.com/StellarCN/py-stellar-base.git
    cd py-stellar-base
    pip install .
