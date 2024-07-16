Stellar Python SDK
==================

.. image:: https://img.shields.io/github/actions/workflow/status/StellarCN/py-stellar-base/continuous-integration-workflow.yml?branch=main
    :alt: GitHub Workflow Status
    :target: https://github.com/StellarCN/py-stellar-base/actions

.. image:: https://img.shields.io/readthedocs/stellar-sdk.svg
    :alt: Read the Docs
    :target: https://stellar-sdk.readthedocs.io/en/latest/

.. image:: https://static.pepy.tech/personalized-badge/stellar-sdk?period=total&units=abbreviation&left_color=grey&right_color=brightgreen&left_text=Downloads
    :alt: PyPI - Downloads
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/codeclimate/maintainability/StellarCN/py-stellar-base
    :alt: Code Climate maintainability
    :target: https://codeclimate.com/github/StellarCN/py-stellar-base/maintainability

.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base/v2
    :alt: Codecov
    :target: https://codecov.io/gh/StellarCN/py-stellar-base

.. image:: https://img.shields.io/pypi/v/stellar-sdk.svg
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/python-%3E%3D3.8-blue
    :alt: Python - Version
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue
    :alt: PyPI - Implementation
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/Stellar%20Protocol-21-blue
    :alt: Stellar Protocol
    :target: https://developers.stellar.org/docs/glossary/scp/

py-stellar-base is a Python library for communicating with
a `Stellar Horizon server`_ and `Soroban-RPC server`_. It is used for building Stellar apps on Python. It supports **Python 3.8+** as
well as PyPy 3.8+.

It provides:

- a networking layer API for Horizon endpoints.
- a networking layer API for Soroban-RPC server methods.
- facilities for building and signing transactions, for communicating with a Stellar Horizon and Soroban-RPC instance, and for submitting transactions or querying network history.

Documentation
-------------
py-stellar-base's documentation can be found at https://stellar-sdk.readthedocs.io.

Installing
----------

.. code-block:: text

    pip install --upgrade stellar-sdk

If you need to use asynchronous, please use the following command to install the required dependencies.

.. code-block:: text

    pip install --upgrade stellar-sdk[aiohttp]

We follow `Semantic Versioning 2.0.0 <https://semver.org/>`_, and I strongly
recommend that you specify its major version number in the dependency
file to avoid the unknown effects of breaking changes.

A Simple Example
----------------
You can find more examples `here <https://github.com/StellarCN/py-stellar-base/tree/main/examples>`__.

.. code-block:: python

    # Alice pay 10.25 XLM to Bob
    from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network

    alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
    bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"

    server = Server("https://horizon-testnet.stellar.org")
    alice_account = server.load_account(alice_keypair.public_key)
    base_fee = 100
    transaction = (
        TransactionBuilder(
            source_account=alice_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .add_text_memo("Hello, Stellar!")
        .append_payment_op(bob_address, Asset.native(), "10.25")
        .set_timeout(30)
        .build()
    )
    transaction.sign(alice_keypair)
    response = server.submit_transaction(transaction)
    print(response)

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

Thank you to all the people who have already contributed to py-stellar-base!

.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon
.. _Soroban-RPC server: https://soroban.stellar.org/docs/reference/rpc