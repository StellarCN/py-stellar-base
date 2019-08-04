[In Development] py-stellar-sdk
===============================

.. image:: https://img.shields.io/pypi/v/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk
.. image:: https://img.shields.io/travis/StellarCN/py-stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Travis (.org)
    :target: https://travis-ci.org/StellarCN/py-stellar-base/

.. image:: https://img.shields.io/readthedocs/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: Read the Docs
    :target: https://stellar-sdk.readthedocs.io/en/latest/

.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Codecov
    :target: https://codecov.io/gh/StellarCN/py-stellar-base



py-stellar-sdk is a Python library for communicating with
a `Stellar Horizon server`_. It is used for building Stellar apps on Python.

It provides:

- a networking layer API for Horizon endpoints.
- facilities for building and signing transactions, for communicating with a Stellar Horizon instance, and for submitting transactions or querying network history.

Installing
----------

Install from pypi:

.. code-block:: text

    pip install -U stellar-sdk


Install from latest source code(*may be unstable*):

.. code-block:: text

    pip install git+git://github.com/StellarCN/py-stellar-base


A Simple Example
----------------

.. code-block:: python

    # Alice pay 10.25 XLM to Bob
    # TODO: WIP

Document
--------
* Quick Start: https://stellar-sdk.readthedocs.io/en/latest/quickstart.html
* API: https://stellar-sdk.readthedocs.io/en/latest/api.html


Links
-----
* Code: https://github.com/StellarCN/py-stellar-base
* Docker: https://hub.docker.com/r/overcat/py-stellar-base
* Examples: https://github.com/StellarCN/py-stellar-base/tree/master/examples
* Issue tracker: https://github.com/StellarCN/py-stellar-base/issues
* License: `Apache License 2.0 <https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE>`_
* Releases: https://pypi.org/project/stellar-sdk/

Thank you to all the people who have already contributed to py-stellar-base!

.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon
