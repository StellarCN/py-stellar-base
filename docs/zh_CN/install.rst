.. _install:

*****
安装
*****

通过 pip 安装
=========================

使用 pip 来安装最新版的 Stellar Python SDK ：

.. code-block:: text

    pip install -U stellar-sdk

Stellar Python SDK 的发布遵循 `Semantic Versioning 2.0.0 <https://semver.org/>`_ ，我强烈建议
你在依赖文件中锁定其版本号，以避免破坏性更新带来的未知影响。想要更多的了解如何安装依赖，请参阅 `Hitchhiker's Guide to Python
<http://docs.python-guide.org/en/latest/starting/installation/>`_ 。

通过源码安装
============

请尽可能使用上述方法安装。最新的代码可能不稳定。

你可以先克隆 `这个仓库 <https://github.com/StellarCN/py-stellar-base>`_，然后通过源码安装 SDK：

.. code-block:: bash

    git clone https://github.com/StellarCN/py-stellar-base.git
    cd py-stellar-base
    pip install .
