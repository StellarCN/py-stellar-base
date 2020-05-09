from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_amount
from ..asset import Asset
from ..muxed_account import MuxedAccount
from ..xdr import xdr


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

    TYPE_CODE = xdr.OperationType.CHANGE_TRUST

    def __init__(
        self,
        asset: Asset,
        limit: Union[str, Decimal] = None,
        source: Union[MuxedAccount, str] = None,
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

    def _to_operation_body(self) -> xdr.OperationBody:
        line = self.asset.to_xdr_object()
        limit = xdr.Int64(Operation.to_xdr_amount(self.limit))
        change_trust_op = xdr.ChangeTrustOp(line, limit)
        body = xdr.OperationBody(type=self.TYPE_CODE, change_trust_op=change_trust_op)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "ChangeTrust":
        """Creates a :class:`ChangeTrust` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        line = Asset.from_xdr_object(operation_xdr_object.body.change_trust_op.line)
        limit = Operation.from_xdr_amount(
            operation_xdr_object.body.change_trust_op.limit.int64
        )

        return cls(source=source, asset=line, limit=limit)
