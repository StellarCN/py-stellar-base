.. py-stellar-sdk documentation master file, created by
   sphinx-quickstart on Sat Jan 20 11:58:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. .. include:: ../README.rst

Stellar Python SDK
==================

.. image:: https://img.shields.io/travis/StellarCN/py-stellar-base/v2?style=flat-square&maxAge=1800
    :alt: Travis (.org)
    :target: https://travis-ci.org/StellarCN/py-stellar-base/

.. image:: https://img.shields.io/readthedocs/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: Read the Docs
    :target: https://stellar-sdk.readthedocs.io/en/latest/

.. image:: https://img.shields.io/codecov/c/github/StellarCN/py-stellar-base/v2?style=flat-square&maxAge=1800
    :alt: Codecov
    :target: https://codecov.io/gh/StellarCN/py-stellar-base

.. image:: https://img.shields.io/codeclimate/maintainability/StellarCN/py-stellar-base?style=flat-square&maxAge=1800
    :alt: Code Climate maintainability
    :target: https://codeclimate.com/github/StellarCN/py-stellar-base/maintainability

.. image:: https://img.shields.io/pypi/v/stellar-sdk.svg?style=flat-square&maxAge=1800
    :alt: PyPI
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue?style=flat-square
    :alt: Python - Version
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue?style=flat-square
    :alt: PyPI - Implementation
    :target: https://pypi.python.org/pypi/stellar-sdk

py-stellar-sdk 是用于开发 Stellar 应用程序的 Python 库。它目前支持 Python 3.6+ 和 PyPy3.6+。

它提供了：

- 完全访问 Horizon 各个接口的能力
- 快速的构建与签署事务，并将它提交到 Stellar 网络

入门
----------
我强烈推荐你阅读官方的 `开发者文档 <https://www.stellar.org/developers/guides/>`_ ，
其中介绍了诸多基础的概念，能帮助你快速的了解 Stellar 网络中的各种概念。

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


API 文档
-----------------
Here you'll find detailed documentation on specific functions, classes, and
methods.

.. toctree::
   :maxdepth: 2

   api


资源
-----
* 文档: https://stellar-sdk.readthedocs.io
* 源代码: https://github.com/StellarCN/py-stellar-base/tree/v2
* Docker: https://hub.docker.com/r/overcat/py-stellar-base
* 示例: https://github.com/StellarCN/py-stellar-base/blob/v2/examples
* Issue 追踪: https://github.com/StellarCN/py-stellar-base/issues
* 许可证: `Apache License 2.0 <https://github.com/StellarCN/py-stellar-base/blob/master/LICENSE>`_
* 已发布版本: https://pypi.org/project/stellar-sdk/

致谢
------
这份文档是在 `Stellar JavaScript SDK`_ 文档的基础上完成的。在此感谢所有向 Stellar 生态贡献过自己的一份力量的同学。


:ref:`genindex`
---------------


.. _here: https://github.com/StellarCN/py-stellar-base/tree/master/examples
.. _Stellar Horizon server: https://github.com/stellar/go/tree/master/services/horizon
.. _pip: https://pip.pypa.io/en/stable/quickstart/
.. _pipenv: https://github.com/pypa/pipenv
.. _Stellar JavaScript SDK: https://www.stellar.org/developers/js-stellar-sdk/reference/
