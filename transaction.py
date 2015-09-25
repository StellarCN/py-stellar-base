# code : utf-8

from .stellarxdr import StellarXDR_pack as Xdr
from .memo import Memo
from .keypair import KeyPair
FEE = 10


class Transaction(object):

    def __init__(self, source, opts):
        self.source = source

        self.sequence = int(opts.get('seqNum')) + 1 if opts.get('seqNum') else None
        self.timeBounds = opts.get('timeBounds') or []
        self.memo = opts.get('memo') or Memo.none()
        self.fee = int(opts.get('fee'))if opts.get('fee') else FEE
        self.operations = opts.get('operations') or []

    def add_operation(self, operation):
        self.operations.append(operation)

    def to_xdr_object(self):
        source_account = KeyPair.from_address(self.source).account_id()
        sequence = self.sequence
        memo = self.memo
        fee = self.fee
        ext = Xdr.nullclass()
        ext.v = 0
        time_bounds = self.timeBounds
        operations = self.operations

        return Xdr.types.Transaction(source_account, fee, sequence, time_bounds, memo, operations, ext)
