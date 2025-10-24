.. py-stellar-base documentation master file, created by
   sphinx-quickstart on Sat Jan 20 11:58:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Stellar Python SDK
==================

py-stellar-base is a Python library for communicating with
a `Stellar Horizon server`_ and `Soroban-RPC server`_. It is used for building Stellar apps on Python. It supports **Python 3.10+** as
well as PyPy 3.10+.

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