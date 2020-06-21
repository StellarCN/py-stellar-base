.. _install:

*****
安装
*****

通过 pipenv 或 pip 安装
=========================

通过 pipenv 来安装 Stellar Python SDK ：

.. code-block:: text

    pipenv install stellar-sdk==2.6.1

我们推荐你使用 `pipenv <https://docs.pipenv.org/>`_ 来安装这个模块。当然你也可以使用 `pip <https://pip.pypa.io/en/stable/quickstart/>`_。
想要更多的了解如何安装依赖，请参阅 `Hitchhiker's Guide to Python
<http://docs.python-guide.org/en/latest/starting/installation/>`_。

通过源码安装
============

请尽可能使用上述方法安装。最新的代码可能不稳定。

你可以先克隆 `这个仓库 <https://github.com/StellarCN/py-stellar-base>`_，然后通过源码安装 SDK：

.. code-block:: bash

    git clone https://github.com/StellarCN/py-stellar-base.git
    cd py-stellar-base
    git checkout 2.6.1
    pip install .
