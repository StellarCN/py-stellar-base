from .operation import Operation

from ..strkey import StrKey
from ..stellarxdr import Xdr
from ..keypair import Keypair


class CreateAccount(Operation):
    @classmethod
    def type_code(cls):
        return Xdr.const.CREATE_ACCOUNT

    def __init__(self, destination, starting_balance, source=None):
        super().__init__(source)
        self.destination = destination
        self.starting_balance = starting_balance

    def to_operation_body(self):
        destination = Keypair.from_public_key(self.destination).xdr_account_id()

        create_account_op = Xdr.types.CreateAccountOp(
            destination, Operation.to_xdr_amount(self.starting_balance))

        body = Xdr.nullclass()
        body.type = Xdr.const.CREATE_ACCOUNT
        body.createAccountOp = create_account_op
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object) -> 'CreateAccount':
        source = Operation.get_source_from_xdr_obj(op_xdr_object)

        destination = StrKey.encode_ed25519_public_key(op_xdr_object.body.createAccountOp.destination.ed25519)
        starting_balance = Operation.from_xdr_amount(op_xdr_object.body.createAccountOp.startingBalance)

        return cls(source=source, destination=destination, starting_balance=starting_balance)
