.. py-stellar-base documentation master file, created by
   sphinx-quickstart on Sat Jan 20 11:58:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. .. include:: ../README.rst

Stellar Python SDK
==================

.. image:: https://img.shields.io/github/actions/workflow/status/StellarCN/py-stellar-base/continuous-integration-workflow.yml?branch=main
    :alt: GitHub Workflow Status
    :target: https://github.com/StellarCN/py-stellar-base/actions

.. image:: https://img.shields.io/readthedocs/stellar-sdk.svg?maxAge=1800
    :alt: Read the Docs
    :target: https://stellar-sdk.readthedocs.io/en/latest/

.. image:: https://static.pepy.tech/personalized-badge/stellar-sdk?period=total&units=abbreviation&left_color=grey&right_color=brightgreen&left_text=Downloads
    :alt: PyPI - Downloads
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/codeclimate/maintainability/StellarCN/py-stellar-base?maxAge=1800
    :alt: Code Climate maintainability
    :target: https://codeclimate.com/github/StellarCN/py-stellar-base/maintainability

.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base/v2?maxAge=1800
    :alt: Codecov
    :target: https://codecov.io/gh/StellarCN/py-stellar-base

.. image:: https://img.shields.io/pypi/v/stellar-sdk.svg?maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/python-%3E%3D3.8-blue
    :alt: Python - Version
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue
    :alt: PyPI - Implementation
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/Stellar%20Protocol-20-blue
    :alt: Stellar Protocol
    :target: https://developers.stellar.org/docs/glossary/scp/

py-stellar-base is a Python library for communicating with
a `Stellar Horizon server`_ and `Soroban-RPC server`_. It is used for building Stellar apps on Python. It supports **Python 3.8+** as
well as PyPy 3.8+.

It provides:

- a networking layer API for Horizon endpoints.
- a networking layer API for Soroban-RPC server methods.
- facilities for building and signing transactions, for communicating with a Stellar Horizon and Soroban-RPC instance, and for submitting transactions or querying network history.

Quickstart
----------
At the absolute basics, you'll want to read up on `Stellar's Documentation
Guides <https://developers.stellar.org/docs/>`_, as it contains a lot of
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
   xdr


API Documentation
-----------------
Here you'll find detailed documentation on specific functions, classes, and
methods.

.. toctree::
   :maxdepth: 2

   api

stellar-model
-------------
stellar-model allows you to parse the JSON returned by Stellar Horizon
into the Python models, click `here <https://github.com/StellarCN/stellar-model>`__ for more information.

Links
-----
* Document: https://stellar-sdk.readthedocs.io
* Code: https://github.com/StellarCN/py-stellar-base
* Examples: https://github.com/StellarCN/py-stellar-base/tree/main/examples
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
.. _Stellar JavaScript SDK: https://github.com/stellar/js-stellar-sdk
.. _Soroban-RPC server: https://soroban.stellar.org/docs/reference/rpc