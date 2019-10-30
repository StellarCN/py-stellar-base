.. _assets:


****
资产
****

:py:class:`Asset <stellar_sdk.asset.Asset>` 的实例代表着 Stellar 网络中的资产。目前 Stellar 网络中有着三种类型的资产：

* 原生资产 **XLM** (**ASSET_TYPE_NATIVE**),
* 资产代码长度最长为 4 位的资产 (**ASSET_TYPE_CREDIT_ALPHANUM4**),
* 资产代码长度最长为 12 位的资产 (**ASSET_TYPE_CREDIT_ALPHANUM12**).

你可以通过 :py:meth:`native() <stellar_sdk.asset.Asset.native>` 来创建原生资产：

.. code-block:: python
    :linenos:

    from stellar_sdk import Asset
    native = Asset.native()


你也可以通过 :py:class:`Asset <stellar_sdk.asset.Asset>` 来创建一个自发行资产，它应该包含资产代码与发行账户：

.. code-block:: python
    :linenos:

    from stellar_sdk import Asset
    # 创建资产代码为 TEST，发行方为 GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB 的资产
    test_asset = Asset("TEST", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB")
    is_native = test_asset.is_native()  # False
    # 创建由 GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB 发行的 Google 股票资产
    google_stock_asset = Asset('US38259P7069', 'GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB')
    google_stock_asset_type = google_stock_asset.type  # credit_alphanum12