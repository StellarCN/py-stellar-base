from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..keypair import Keypair
from ..muxed_account import MuxedAccount
from ..strkey import StrKey
from ..utils import raise_if_not_valid_ed25519_public_key
from .operation import Operation

__all__ = ["BeginSponsoringFutureReserves"]


class BeginSponsoringFutureReserves(Operation):
    """The :class:`BeginSponsoringFutureReserves` object, which represents a BeginSponsoringFutureReserves
    operation on Stellar's network.

    Establishes the is-sponsoring-future-reserves-for relationship between the source account and sponsoredID.
    See `Sponsored Reserves <https://developers.stellar.org/docs/glossary/sponsored-reserves/>`_ for more information.

    Threshold: Medium

    See `Begin Sponsoring Future Reserves <https://developers.stellar.org/docs/start/list-of-operations/#begin-sponsoring-future-reserves>`_ for more information.

    :param sponsored_id: The sponsored account id.
    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.BEGIN_SPONSORING_FUTURE_RESERVES
    )

    def __init__(
        self, sponsored_id: str, source: Optional[Union[MuxedAccount, str]] = None
    ) -> None:
        super().__init__(source)
        self.sponsored_id: str = sponsored_id
        raise_if_not_valid_ed25519_public_key(self.sponsored_id, "sponsored_id")

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        sponsored_id = Keypair.from_public_key(self.sponsored_id).xdr_account_id()
        begin_sponsoring_future_reserves_op = (
            stellar_xdr.BeginSponsoringFutureReservesOp(sponsored_id=sponsored_id)
        )
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE,
            begin_sponsoring_future_reserves_op=begin_sponsoring_future_reserves_op,
        )
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "BeginSponsoringFutureReserves":
        """Creates a :class:`BeginSponsoringFutureReserves` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.begin_sponsoring_future_reserves_op is not None
        assert (
            xdr_object.body.begin_sponsoring_future_reserves_op.sponsored_id.account_id.ed25519
            is not None
        )
        sponsored_id = StrKey.encode_ed25519_public_key(
            xdr_object.body.begin_sponsoring_future_reserves_op.sponsored_id.account_id.ed25519.uint256
        )
        op = cls(source=source, sponsored_id=sponsored_id)
        return op

    def __repr__(self):
        return f"<BeginSponsoringFutureReserves [sponsored_id={self.sponsored_id}, source={self.source}]>"
