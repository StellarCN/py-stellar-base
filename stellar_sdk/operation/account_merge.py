from typing import Optional

from .operation import Operation
from .utils import check_ed25519_public_key
from ..keypair import Keypair
from ..utils import parse_ed25519_account_id_from_muxed_account_xdr_object
from ..xdr import Xdr


class AccountMerge(Operation):
    """The :class:`AccountMerge` object, which represents a
    AccountMerge operation on Stellar's network.

    Transfers the native balance (the amount of XLM an account holds) to
    another account and removes the source account from the ledger.

    Threshold: High

    :param destination: Destination to merge the source account into.
    :param source: The source account (defaults to transaction source).

    """

    def __init__(self, destination: str, source: str = None,) -> None:
        super().__init__(source)
        check_ed25519_public_key(destination)
        self._destination: str = destination
        self._destination_muxed: Optional[Xdr.types.MuxedAccount] = None

    @property
    def destination(self) -> str:
        return self._destination

    @destination.setter
    def destination(self, value: str):
        check_ed25519_public_key(value)
        self._destination_muxed = None
        self._destination = value

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.ACCOUNT_MERGE

    def _to_operation_body(self) -> Xdr.nullclass:
        if self._destination_muxed is not None:
            destination = self._destination_muxed
        else:
            destination = Keypair.from_public_key(self._destination).xdr_muxed_account()
        body = Xdr.nullclass()
        body.type = Xdr.const.ACCOUNT_MERGE
        body.destination = destination
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "AccountMerge":
        """Creates a :class:`AccountMerge` object from an XDR Operation
        object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)
        destination = parse_ed25519_account_id_from_muxed_account_xdr_object(
            operation_xdr_object.body.destination
        )
        op = cls(source=source, destination=destination)
        op._destination_muxed = operation_xdr_object.body.destination
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
