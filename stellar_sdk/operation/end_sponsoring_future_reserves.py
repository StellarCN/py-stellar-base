from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["EndSponsoringFutureReserves"]


class EndSponsoringFutureReserves(Operation):
    """The :class:`EndSponsoringFutureReserves` object, which represents a EndSponsoringFutureReserves
    operation on Stellar's network.

    Terminates the current is-sponsoring-future-reserves-for relationship in which the source account is sponsored.
    See `Sponsored Reserves <https://developers.stellar.org/docs/glossary/sponsored-reserves/>`_ for more information.

    Threshold: Medium

    See `End Sponsoring Future Reserves <https://developers.stellar.org/docs/start/list-of-operations/#end-sponsoring-future-reserves>`_.

    :param source: The source account for the operation. Defaults to the transaction's source account.
    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.END_SPONSORING_FUTURE_RESERVES
    )

    def __init__(self, source: Optional[Union[MuxedAccount, str]] = None) -> None:
        super().__init__(source)

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        body = stellar_xdr.OperationBody(type=self._XDR_OPERATION_TYPE)
        return body

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.Operation
    ) -> "EndSponsoringFutureReserves":
        """Creates a :class:`EndSponsoringFutureReserves` object from an XDR Operation
        object.
        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        op = cls(source=source)
        return op

    def __repr__(self):
        return f"<EndSponsoringFutureReserves [source={self.source}]>"
