# code : utf-8

from .memo import *
from .utils import decode_check
from .utils import account_xdr_object

FEE = 100


class Transaction(object):
    def __init__(self, source, opts):
        """source should be a stellar address who will submit this Transaction,and should be a string .
            opts should be a dict ,will contain some  variables to build a transaction
            opts.sequence : needed .the last sequence the source use.  should be a string.
            opts.time_bounds : a list with two Unix timestamps, default is a empty list
            opts.memo : a stellar_base *memo object ,can be string or hash object ,
                        default is a NoneMemo object .see memo.py
            opts.fee  : count in stroops , at least 100 ,default is 100
            opts.operations : a list of  stellar_base operation objects ,default is a empty list
        """
        assert source is not None
        assert decode_check('account', source)
        assert type(opts) is dict
        assert opts.get('seqNum') is not None

        self.source = source
        self.sequence = int(opts.get('seqNum')) + 1
        self.time_bounds = opts.get('timeBounds') or []
        self.memo = opts.get('memo') or NoneMemo()
        self.fee = int(opts.get('fee')) if opts.get('fee') else FEE
        self.operations = opts.get('operations') or []

    def add_operation(self, operation):
        self.operations.append(operation)

    def to_xdr_object(self):
        source_account = account_xdr_object(self.source)
        memo = self.memo.to_xdr_object()
        operations = [o.to_xdr_object() for o in self.operations]
        ext = Xdr.nullclass()
        ext.v = 0
        return Xdr.types.Transaction(source_account, self.fee, self.sequence, self.time_bounds, memo,
                                     operations, ext)
