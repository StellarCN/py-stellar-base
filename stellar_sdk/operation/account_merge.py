from .operation import Operation
from .utils import check_ed25519_public_key
from ..keypair import Keypair
from ..strkey import StrKey
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

    def __init__(self, destination: str, source: str = None) -> None:
        super().__init__(source)
        check_ed25519_public_key(destination)
        self.destination: str = destination

    @classmethod
    def type_code(cls) -> xdr.OperationType:
        return xdr.OperationType.ACCOUNT_MERGE

    def _to_operation_body(self) -> xdr.OperationBody:
        destination = Keypair.from_public_key(self.destination).xdr_account_id()
        body = xdr.OperationBody(type=self.type_code(), destination=destination)
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "AccountMerge":
        """Creates a :class:`AccountMerge` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.destination.account_id.ed25519.uint256
        )
        return cls(source=source, destination=destination)
