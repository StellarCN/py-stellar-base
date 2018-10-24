py-stellar-base
===============

.. image:: https://img.shields.io/travis/StellarCN/py-stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Travis (.org)
    :target: https://travis-ci.org/StellarCN/py-stellar-base/

.. image:: https://img.shields.io/readthedocs/stellar-base.svg?style=flat-square&maxAge=1800
    :alt: Read the Docs
    :target: https://stellar-base.readthedocs.io/en/latest/

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

Install from pypi, there are two packages here, please choose one of them:

* The package is built automatically by Travis-CI. |stellar-sdk-image|

.. |stellar-sdk-image| image:: https://img.shields.io/pypi/v/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk

.. code-block:: text

    pip install -U stellar-sdk

* The package is maintained by antb123. |stellar-base-image|

.. |stellar-base-image| image:: https://img.shields.io/pypi/v/stellar-base.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-base

.. code-block:: text

    pip install -U stellar-base

Install from latest source code(*may be unstable*):

.. code-block:: text

    pip install git+git://github.com/StellarCN/py-stellar-base


A Simple Example
----------------

.. code-block:: python

    # Alice pay 10.25 XLM to Bob
    from stellar_base.builder import Builder

    alice_secret = 'SCB6JIZUC3RDHLRGFRTISOUYATKEE63EP7MCHNZNXQMQGZSLZ5CNRTKK'
    bob_address = 'GA7YNBW5CBTJZ3ZZOWX3ZNBKD6OE7A7IHUQVWMY62W2ZBG2SGZVOOPVH'

    builder = Builder(secret=alice_secret)
    builder.add_text_memo("Hello, Stellar!").append_payment_op(
        destination=bob_address, amount='10.25', asset_code='XLM')
    builder.sign()
    response = builder.submit()
    print(response)


Document
--------
* Quick Start: https://stellar-base.readthedocs.io/en/latest/quickstart.html
* API: https://stellar-base.readthedocs.io/en/latest/api.html


Links
-----
* Examples: https://github.com/StellarCN/py-stellar-base/tree/master/examples
* Releases: https://pypi.org/project/stellar-sdk/
* Code: https://github.com/StellarCN/py-stellar-base
* Issue tracker: https://github.com/StellarCN/py-stellar-base/issues
* License: `Apache License 2.0 <https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE>`_

Thank you to all the people who have already contributed to py-stellar-base!

.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon
