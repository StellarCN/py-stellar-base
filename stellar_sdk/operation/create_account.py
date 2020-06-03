from decimal import Decimal
from typing import Union

from .operation import Operation
from .utils import check_ed25519_public_key, check_amount
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import Xdr


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

    @classmethod
    def type_code(cls) -> int:
        return Xdr.const.CREATE_ACCOUNT

    def _to_operation_body(self):
        destination = Keypair.from_public_key(self.destination).xdr_account_id()

        create_account_op = Xdr.types.CreateAccountOp(
            destination, Operation.to_xdr_amount(self.starting_balance)
        )

        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_ACCOUNT
        body.createAccountOp = create_account_op
        return body

    @classmethod
    def from_xdr_object(
        cls, operation_xdr_object: Xdr.types.Operation
    ) -> "CreateAccount":
        """Creates a :class:`CreateAccount` object from an XDR Operation object.

        """
        source = Operation.get_source_from_xdr_obj(operation_xdr_object)

        destination = StrKey.encode_ed25519_public_key(
            operation_xdr_object.body.createAccountOp.destination.ed25519
        )
        starting_balance = Operation.from_xdr_amount(
            operation_xdr_object.body.createAccountOp.startingBalance
        )

        op = cls(
            source=source, destination=destination, starting_balance=starting_balance
        )
        op._source_muxed = Operation.get_source_muxed_from_xdr_obj(operation_xdr_object)
        return op
