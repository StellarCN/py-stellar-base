from .operation import Operation
from .utils import check_ed25519_public_key
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import Xdr


class BeginSponsoringFutureReserves(Operation):
    """The :class:`BeginSponsoringFutureReserves` object, which represents a BeginSponsoringFutureReserves
    operation on Stellar's network.

    Establishes the is-sponsoring-future-reserves-for relationship between the source account and sponsoredID.
    See `Sponsored Reserves <https://developers.stellar.org/docs/glossary/sponsored-reserves/>_` for more information.

    See `Begin Sponsoring Future Reserves
    <https://developers.stellar.org/docs/start/list-of-operations/#begin-sponsoring-future-reserves>_`.

    Threshold: Medium

    :param sponsored_id: The sponsored account id.
    :param source: The source account (defaults to transaction source).
    """

    def __init__(self, sponsored_id: str, source: str = None) -> None:
        super().__init__(source)
        check_ed25519_public_key(sponsored_id)
        self.sponsored_id: str = sponsored_id

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.BEGIN_SPONSORING_FUTURE_RESERVES

    def _to_operation_body(self) -> Xdr.nullclass:
        sponsored_id = Keypair.from_public_key(self.sponsored_id).xdr_account_id()
        begin_sponsoring_future_reserves_op = Xdr.types.BeginSponsoringFutureReservesOp(
            sponsoredID=sponsored_id
        )
        body = Xdr.nullclass()
        body.type = Xdr.const.BEGIN_SPONSORING_FUTURE_RESERVES
        body.beginSponsoringFutureReservesOp = begin_sponsoring_future_reserves_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "BeginSponsoringFutureReserves":
        """Creates a :class:`BeginSponsoringFutureReserves` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        sponsored_id = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.beginSponsoringFutureReservesOp.sponsoredID.ed25519
        )
        op = cls(source=source, sponsored_id=sponsored_id)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
