from typing import Optional, Union

from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount
from .operation import Operation

__all__ = ["AccountMerge"]


class AccountMerge(Operation):
    """The :class:`AccountMerge` object, which represents a
    AccountMerge operation on Stellar's network.

    Transfers the native balance (the amount of XLM an account holds) to
    another account and removes the source account from the ledger.

    Threshold: High

    See `Account Merge <https://developers.stellar.org/docs/start/list-of-operations/#account-merge>`_ for more information.

    :param destination: Destination to merge the source account into.
    :param source: The source account for the operation. Defaults to the transaction's source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = (
        stellar_xdr.OperationType.ACCOUNT_MERGE
    )

    def __init__(
        self,
        destination: Union[MuxedAccount, str],
        source: Optional[Union[MuxedAccount, str]] = None,
    ) -> None:
        super().__init__(source)
        if isinstance(destination, str):
            destination = MuxedAccount.from_account(destination)
        self.destination: MuxedAccount = destination

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        destination = self.destination.to_xdr_object()
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, destination=destination
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "AccountMerge":
        """Creates a :class:`AccountMerge` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.destination is not None
        destination = MuxedAccount.from_xdr_object(xdr_object.body.destination)
        op = cls(source=source, destination=destination)
        return op

    def __repr__(self):
        return f"<AccountMerge [destination={self.destination}, source={self.source}]>"
