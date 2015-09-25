# code : utf-8

from .stellarxdr import StellarXDR_pack as xdr
from .memo import Memo
from .keypair import KeyPair
FEE = 10


class Transaction(object):

    def __init__(self, source, opts):
        self.source = source

        self.sequence = int(opts.get('seqNum'))+1 if opts.get('seqNum') else None
        self.timeBounds = opts.get('timeBounds') or []
        self.memo = opts.get('memo') or Memo.none()
        self.fee = int(opts.get('fee'))if opts.get('fee') else FEE
        self.operations = opts.get('operations') or []

    def addOperation(self, operation):
        self.operations.append(operation)

    def toXDRObject(self):
        sourceAccount = KeyPair.fromAddress(self.source).accountId()
        sequence = self.sequence 
        memo = self.memo
        fee = self.fee
        ext = xdr.nullclass()
        ext.v = 0
        timeBounds = self.timeBounds
        operations = self.operations

        return xdr.types.Transaction(sourceAccount, fee, sequence, timeBounds, memo, operations, ext)
