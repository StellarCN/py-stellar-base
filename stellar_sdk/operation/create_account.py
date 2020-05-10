from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_ed25519_public_key, check_amount
from ..keypair import Keypair
from ..muxed_account import MuxedAccount
from ..strkey import StrKey
from ..xdr import xdr


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

    TYPE_CODE = xdr.OperationType.CREATE_ACCOUNT

    def __init__(
        self,
        destination: str,
        starting_balance: Union[str, Decimal],
        source: Union[MuxedAccount, str] = None,
    ) -> None:
        super().__init__(source)
        check_ed25519_public_key(destination)
        check_amount(starting_balance)
        self.destination: str = destination
        self.starting_balance: Union[str, Decimal] = starting_balance

    def _to_operation_body(self):
        destination = Keypair.from_public_key(self.destination).xdr_account_id()
        starting_balance = xdr.Int64(Operation.to_xdr_amount(self.starting_balance))
        create_account_op = xdr.CreateAccountOp(destination, starting_balance)
        body = xdr.OperationBody(
            type=self.TYPE_CODE, create_account_op=create_account_op
        )
        return body

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: xdr.Operation) -> "CreateAccount":
        """Creates a :class:`CreateAccount` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        destination = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.create_account_op.destination.account_id.ed25519.uint256
        )
        starting_balance = Operation.from_xdr_amount(
            operation_xdr_object.body.create_account_op.starting_balance.int64
        )

        return cls(
            source=source, destination=destination, starting_balance=starting_balance
        )
