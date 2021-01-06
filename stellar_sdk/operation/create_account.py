from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_ed25519_public_key, check_amount
from .. import xdr as stellar_xdr
from ..keypair import Keypair
from ..strkey import StrKey


class CreateAccount(Operation):
    """The :class:`CreateAccount` object, which represents a Create Account
    operation on Stellar's network.

    This operation creates and funds a new account with the specified starting
    balance.

    Threshold: Medium

    :param destination: Destination account ID to create an account for.
    :param starting_balance: Amount in XLM the account should be
        funded for. Must be greater than the `reserve balance amount
        <https://www.stellar.org/developers/learn/concepts/fees.html>`_.
    :param source: The source account for the payment. Defaults to the
        transaction's source account.

    """

    _XDR_OPERATION_TYPE: stellar_xdr.OperationType = stellar_xdr.OperationType.CREATE_ACCOUNT

    def __init__(
        self,
        destination: str,
        starting_balance: Union[str, Decimal],
        source: str = None,
    ) -> None:
        super().__init__(source)
        check_ed25519_public_key(destination)
        check_amount(starting_balance)
        self.destination: str = destination
        self.starting_balance: Union[str, Decimal] = starting_balance

    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        destination = Keypair.from_public_key(self.destination).xdr_account_id()
        starting_balance = stellar_xdr.Int64(
            Operation.to_xdr_amount(self.starting_balance)
        )
        create_account_op = stellar_xdr.CreateAccountOp(destination, starting_balance)
        body = stellar_xdr.OperationBody(
            type=self._XDR_OPERATION_TYPE, create_account_op=create_account_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "CreateAccount":
        """Creates a :class:`CreateAccount` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(xdr_object)
        assert xdr_object.body.create_account_op is not None
        assert (
            xdr_object.body.create_account_op.destination.account_id.ed25519 is not None
        )
        destination = StrKey.encode_ed25519_public_key(
            xdr_object.body.create_account_op.destination.account_id.ed25519.uint256
        )
        starting_balance = Operation.from_xdr_amount(
            xdr_object.body.create_account_op.starting_balance.int64
        )
        op = cls(
            source=source, destination=destination, starting_balance=starting_balance
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(xdr_object)
        return op

    def __str__(self):
        return (
            f"<CreateAccount [destination={self.destination}, "
            f"starting_balance={self.starting_balance}, "
            f"source={self.source}]>"
        )
