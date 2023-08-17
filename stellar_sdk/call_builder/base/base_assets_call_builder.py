from ...call_builder.base.base_call_builder import BaseCallBuilder

__all__ = ["BaseAssetsCallBuilder"]


class BaseAssetsCallBuilder(BaseCallBuilder):
    """Creates a new :class:`AssetsCallBuilder` pointed to server defined by horizon_url.

    See `List All Assets <https://developers.stellar.org/api/resources/assets/list/>`__ for more information.

    :param horizon_url: Horizon server URL.
    """

    def __init__(self, horizon_url: str) -> None:
        super().__init__(horizon_url)
        self.endpoint: str = "assets"

    def for_code(self, asset_code: str):
        """This endpoint filters all assets by the asset code.

        See `List All Assets <https://developers.stellar.org/api/resources/assets/list/>`__ for more information.

        :param asset_code: asset code, for example: `USD`
        :return: current AssetCallBuilder instance
        """
        self._add_query_param("asset_code", asset_code)
        return self

    def for_issuer(self, asset_issuer: str):
        """This endpoint filters all assets by the asset issuer.

        See `List All Assets <https://developers.stellar.org/api/resources/assets/list/>`__ for more information.

        :param asset_issuer: asset issuer,
            for example: ``"GDGQVOKHW4VEJRU2TETD6DBRKEO5ERCNF353LW5WBFW3JJWQ2BRQ6KDD"``
        :return: current AssetCallBuilder instance
        """
        self._add_query_param("asset_issuer", asset_issuer)
        return self
