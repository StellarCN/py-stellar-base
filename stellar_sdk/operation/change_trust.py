from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount
from ..asset import Asset
from ..xdr import Xdr


class ChangeTrust(Operation):
    """The :class:`ChangeTrust` object, which represents a ChangeTrust
    operation on Stellar's network.

    Creates, updates, or deletes a trustline. For more on trustlines, please
    refer to the `assets documentation
    <https://www.stellar.org/developers/guides/concepts/assets.html>_`.

    Threshold: Medium

    :param asset: The asset for the trust line.
    :param limit: The limit for the asset, defaults to max int64(922337203685.4775807).
        If the limit is set to "0" it deletes the trustline.
    :param source: The source account (defaults to transaction source).

    """

    _DEFAULT_LIMIT = "922337203685.4775807"

    def __init__(
        self, asset: Asset, limit: Union[str, Decimal] = None, source: str = None,
    ) -> None:
        super().__init__(source)
        self.asset: Asset = asset
        if (
            limit is None
        ):  # We don't need this if the user can send the value with correct type.
            self.limit: Union[str, Decimal] = self._DEFAULT_LIMIT
        else:
            check_amount(limit)
            self.limit = limit

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CHANGE_TRUST

    def _to_operation_body(self) -> Xdr.nullclass:
        line = self.asset.to_xdr_object()
        limit = Operation.to_xdr_amount(self.limit)

        change_trust_op = Xdr.types.ChangeTrustOp(line, limit)
        body = Xdr.nullclass()
        body.type = Xdr.const.CHANGE_TRUST
        body.changeTrustOp = change_trust_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "ChangeTrust":
        """Creates a :class:`ChangeTrust` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        line = Asset.from_xdr_object(operation_xdr_object.body.changeTrustOp.line)
        limit = Operation.from_xdr_amount(operation_xdr_object.body.changeTrustOp.limit)

        op = cls(source=source, asset=line, limit=limit)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
