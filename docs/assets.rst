.. _assets:


******
Assets
******

Object of the :py:class:`Asset <stellar_sdk.asset.Asset>`
class represents an asset in the Stellar network. Right now there are 3 possible types of assets in the Stellar network:


* native **XLM** asset (**ASSET_TYPE_NATIVE**),
* issued assets with asset code of maximum 4 characters (**ASSET_TYPE_CREDIT_ALPHANUM4**),
* issued assets with asset code of maximum 12 characters (**ASSET_TYPE_CREDIT_ALPHANUM12**).

To create a new native asset representation use static :py:meth:`native() <stellar_sdk.asset.Asset.native>` method:

.. code-block:: python
    :linenos:

    from stellar_sdk import Asset
    native = Asset.native()

To represent an issued asset you need to create a new object of type :py:class:`Asset <stellar_sdk.asset.Asset>` with an asset code and issuer:

.. code-block:: python
    :linenos:

    from stellar_sdk import Asset
    # Creates TEST asset issued by GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB
    test_asset = Asset("TEST", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB")
    is_native = test_asset.is_native()  # False
    # Creates Google stock asset issued by GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB
    google_stock_asset = Asset('US38259P7069', 'GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB')
    google_stock_asset_type = google_stock_asset.type  # credit_alphanum12