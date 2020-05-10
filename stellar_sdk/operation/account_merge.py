from typing import Union

from .operation import Operation
from .utils import parse_mux_account_from_account
from ..muxed_account import MuxedAccount
from ..xdr import xdr


class AccountMerge(Operation):
    """The :class:`AccountMerge` object, which represents a
    AccountMerge operation on Stellar's network.

    Transfers the native balance (the amount of XLM an account holds) to
    another account and removes the source account from the ledger.

    Threshold: High

    :param destination: Destination to merge the source account into.
    :param source: The source account (defaults to transaction source).

    """

    TYPE_CODE = xdr.OperationType.ACCOUNT_MERGE

    def __init__(
        self,
        destination: Union[MuxedAccount, str],
        source: Union[MuxedAccount, str] = None,
    ) -> None:
        super().__init__(source)
        self.destination: MuxedAccount = parse_mux_account_from_account(destination)

    def _to_operation_body(self) -> xdr.OperationBody:
        destination = self.destination.to_xdr_object()
        body = xdr.OperationBody(type=self.TYPE_CODE, destination=destination)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "AccountMerge":
        """Creates a :class:`AccountMerge` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = MuxedAccount.from_xdr_object(
            operation_xdr_object.body.destination
        )
        return cls(source=source, destination=destination)
