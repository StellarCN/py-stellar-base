from .operation import Operation
from ..xdr import Xdr


class EndSponsoringFutureReserves(Operation):
    """The :class:`EndSponsoringFutureReserves` object, which represents a EndSponsoringFutureReserves
    operation on Stellar's network.

    Terminates the current is-sponsoring-future-reserves-for relationship in which the source account is sponsored.
    See `Sponsored Reserves <https://developers.stellar.org/docs/glossary/sponsored-reserves/>_` for more information.

    See `End Sponsoring Future Reserves
    <https://developers.stellar.org/docs/start/list-of-operations/#end-sponsoring-future-reserves>_`.

    Threshold: Medium

    :param source: The source account (defaults to transaction source).
    """

    def __init__(self, source: str = None) -> None:
        super().__init__(source)

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.END_SPONSORING_FUTURE_RESERVES

    def _to_operation_body(self) -> Xdr.nullclass:
        body = Xdr.nullclass()
        body.type = Xdr.const.END_SPONSORING_FUTURE_RESERVES
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "EndSponsoringFutureReserves":
        """Creates a :class:`EndSponsoringFutureReserves` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        op = cls(source=source,)
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
