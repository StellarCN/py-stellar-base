Stellar Python SDK
==================

.. image:: https://img.shields.io/github/workflow/status/StellarCN/py-stellar-base/GitHub%20Action/master?maxAge=1800
    :alt: GitHub Action
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

.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8%20%7C%203.9-blue
    :alt: Python - Version
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue
    :alt: PyPI - Implementation
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/Stellar%20Protocol-18-blue
    :alt: Stellar Protocol
    :target: https://developers.stellar.org/docs/glossary/scp/

py-stellar-base is a Python library for communicating with
a `Stellar Horizon server`_. It is used for building Stellar apps on Python. It supports **Python 3.6+** as
well as PyPy 3.6+.

It provides:

- a networking layer API for Horizon endpoints.
- facilities for building and signing transactions, for communicating with a Stellar Horizon instance, and for submitting transactions or querying network history.

Documentation
-------------
py-stellar-base's documentation can be found at https://stellar-sdk.readthedocs.io.

Installing
----------

.. code-block:: text

    pip install stellar-sdk==6.0.0b0


A Simple Example
----------------

Building transaction with synchronous server

.. code-block:: python

    # Alice pay 10.25 XLM to Bob
    from stellar_sdk import Asset, Server, Keypair, TransactionBuilder, Network

    alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
    bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"

    server = Server("https://horizon-testnet.stellar.org")
    alice_account = server.load_account(alice_keypair.public_key)
    base_fee = server.fetch_base_fee()
    transaction = (
        TransactionBuilder(
            source_account=alice_account,
            network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
            base_fee=base_fee,
        )
        .add_text_memo("Hello, Stellar!")
        .append_payment_op(bob_address, Asset.native(), "10.25")
        .build()
    )
    transaction.sign(alice_keypair)
    response = server.submit_transaction(transaction)
    print(response)


* Building transaction with asynchronous server

.. code-block:: python

    # Alice pay 10.25 XLM to Bob
    import asyncio

    from stellar_sdk import Asset, ServerAsync, Keypair, TransactionBuilder, Network
    from stellar_sdk.client.aiohttp_client import AiohttpClient

    alice_keypair = Keypair.from_secret("SBFZCHU5645DOKRWYBXVOXY2ELGJKFRX6VGGPRYUWHQ7PMXXJNDZFMKD")
    bob_address = "GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH"


    async def payment():
        async with ServerAsync(
            horizon_url="https://horizon-testnet.stellar.org", client=AiohttpClient()
        ) as server:
            alice_account = await server.load_account(alice_keypair.public_key)
            base_fee = await server.fetch_base_fee()
            transaction = (
                TransactionBuilder(
                    source_account=alice_account,
                    network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
                    base_fee=base_fee,
                )
                .add_text_memo("Hello, Stellar!")
                .append_payment_op(bob_address, Asset.native(), "10.25")
                .build()
            )

            transaction.sign(alice_keypair)
            response = await server.submit_transaction(transaction)
            print(response)


    if __name__ == "__main__":
        asyncio.run(payment())

stellar-model
-------------
stellar-model allows you to parse the JSON returned by Stellar Horizon
into the Python models, click `here <https://github.com/StellarCN/stellar-model>`__ for more information.

Links
-----
* Document: https://stellar-sdk.readthedocs.io
* Code: https://github.com/StellarCN/py-stellar-base
* Examples: https://github.com/StellarCN/py-stellar-base/tree/dev/examples
* Issue tracker: https://github.com/StellarCN/py-stellar-base/issues
* License: `Apache License 2.0 <https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE>`_
* Releases: https://pypi.org/project/stellar-sdk/

Thank you to all the people who have already contributed to py-stellar-base!

.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _pipenv: https://github.com/pypa/pipenv