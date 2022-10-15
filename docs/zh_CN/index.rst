.. py-stellar-base documentation master file, created by
   sphinx-quickstart on Sat Jan 20 11:58:02 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. .. include:: ../README.rst

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

.. image:: https://img.shields.io/badge/python-%3E%3D3.7-blue
    :alt: Python - Version
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/implementation-cpython%20%7C%20pypy-blue
    :alt: PyPI - Implementation
    :target: https://pypi.python.org/pypi/stellar-sdk

.. image:: https://img.shields.io/badge/Stellar%20Protocol-19-blue
    :alt: Stellar Protocol
    :target: https://developers.stellar.org/docs/glossary/scp/

py-stellar-base 是用于开发 Stellar 应用程序的 Python 库。它目前支持 Python 3.7+ 和 PyPy3.7+。

它提供了：

- 完全访问 Horizon 各个接口的能力
- 快速的构建与签署事务，并将它提交到 Stellar 网络

入门
----------
我强烈推荐你阅读官方的 `开发者文档 <https://developers.stellar.org/docs/>`_ ，
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
   xdr

API 文档
-----------------
Here you'll find detailed documentation on specific functions, classes, and
methods.

.. toctree::
   :maxdepth: 2

   api

stellar-model
-------------
stellar-model 可以将 Stellar Horizon 返回的 JSON 解析为 Python 实例，以提高你的开发效率，
请 `点击这里 <https://github.com/StellarCN/stellar-model>`__ 获取更多信息。

资源
-----
* 文档: https://stellar-sdk.readthedocs.io
* 源代码: https://github.com/StellarCN/py-stellar-base
* 示例: https://github.com/StellarCN/py-stellar-base/tree/main/examples
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
.. _Stellar JavaScript SDK: https://github.com/stellar/js-stellar-sdk
