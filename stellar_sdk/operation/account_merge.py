from .operation import Operation

from ..keypair import Keypair
from ..strkey import StrKey
from ..stellarxdr import Xdr


class AccountMerge(Operation):
    @classmethod
    def type_code(cls):
        return Xdr.const.ACCOUNT_MERGE

    def __init__(self, destination, source=None):
        super().__init__(source)
        self.destination = destination

    def to_operation_body(self):
        destination = Keypair.from_public_key(self.destination).xdr_account_id()
        body = Xdr.nullclass
        body.type = Xdr.const.ACCOUNT_MERGE
        body.destination = destination
        return body

    @classmethod
    def from_xdr_object(cls, op_xdr_object):
        source = Operation.get_source_from_xdr_obj(op_xdr_object)
        destination = StrKey.encode_ed25519_public_key(op_xdr_object.body.destination.ed25519)
        return cls(source=source, destination=destination)
