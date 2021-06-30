.. py-stellar-base documentation master file, created by
   sphinx-quickstart on Sat Jan 20 11:58:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. .. include:: ../README.rst

Stellar Python SDK
==================

.. image:: https://img.shields.io/github/workflow/status/StellarCN/py-stellar-base/GitHub%20Action/master?style=flat-square&maxAge=1800
    :alt: GitHub Action
    :target: https://github.com/StellarCN/py-stellar-base/actions

.. image:: https://img.shields.io/readthedocs/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: Read the Docs
    :target: https://stellar-sdk.readthedocs.io/en/latest/

.. image:: https://img.shields.io/pypi/dm/stellar-sdk?style=flat-square
    :alt: PyPI - Downloads
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/codeclimate/maintainability/StellarCN/py-stellar-base?style=flat-square&maxAge=1800
    :alt: Code Climate maintainability
    :target: https://codeclimate.com/github/StellarCN/py-stellar-base/maintainability

.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base/v2?style=flat-square&maxAge=1800
    :alt: Codecov
    :target: https://codecov.io/gh/StellarCN/py-stellar-base

.. image:: https://img.shields.io/pypi/v/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue?style=flat-square
    :alt: Python - Version
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue?style=flat-square
    :alt: PyPI - Implementation
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/Stellar%20Protocol-17-blue?style=flat-square
    :alt: Stellar Protocol
    :target: https://www.stellar.org/developers/guides/concepts/scp.html

.. image:: https://img.shields.io/badge/Horizon%20Version-2.1.0-blue?style=flat-square
    :alt: Horizon Version
    :target: https://github.com/stellar/go/releases/tag/horizon-v2.1.0

py-stellar-base is a Python library for communicating with
a `Stellar Horizon server`_. It is used for building Stellar apps on Python. It supports **Python 3.6+** as
well as PyPy 3.6+.

It provides:

- a networking layer API for Horizon endpoints.
- facilities for building and signing transactions, for communicating with a Stellar Horizon instance, and for submitting transactions or querying network history.

Quickstart
----------
At the absolute basics, you'll want to read up on `Stellar's Documentation
Guides <https://www.stellar.org/developers/guides/>`_, as it contains a lot of
information on the concepts used below (Transactions, Payments, Operations,
KeyPairs, etc.).

.. toctree::
   :maxdepth: 2

   install
   generate_keypair
   create_account
   querying_horizon
   assets
   building_transactions
   payment
   asynchronous
   multi_signature_account


API Documentation
-----------------
Here you'll find detailed documentation on specific functions, classes, and
methods.

.. toctree::
   :maxdepth: 2

   api


Links
-----
* Document: https://stellar-sdk.readthedocs.io
* Code: https://github.com/StellarCN/py-stellar-base/tree/v2
* Docker: https://hub.docker.com/r/overcat/py-stellar-base
* Examples: https://github.com/StellarCN/py-stellar-base/blob/v2/examples
* Issue tracker: https://github.com/StellarCN/py-stellar-base/issues
* License: `Apache License 2.0 <https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE>`_
* Releases: https://pypi.org/project/stellar-sdk/

Thanks
------
This document is based on `Stellar JavaScript SDK`_ documentation.
Thank you to all the people who have already contributed to Stellar ecosystem!


:ref:`genindex`
---------------


.. _here: https://github.com/StellarCN/py-stellar-base/tree/master/examples
.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _pipenv: https://github.com/pypa/pipenv
.. _Stellar JavaScript SDK: https://www.stellar.org/developers/js-stellar-sdk/reference/
