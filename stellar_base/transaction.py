# coding: utf-8

from .memo import *
from .operation import *
from .utils import decode_check

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
        assert opts.get('sequence') is not None

        self.source = source
        self.sequence = int(opts.get('sequence')) + 1
        self.time_bounds = opts.get('timeBounds') or []
        self.memo = opts.get('memo') or NoneMemo()
        self.fee = int(opts.get('fee')) if opts.get('fee') else FEE
        self.operations = opts.get('operations') or []

    def add_operation(self, operation):
        if operation not in self.operations:
            self.operations.append(operation)

    def to_xdr_object(self):
        source_account = account_xdr_object(self.source)
        memo = self.memo.to_xdr_object()
        operations = [o.to_xdr_object() for o in self.operations]
        ext = Xdr.nullclass()
        ext.v = 0
        return Xdr.types.Transaction(source_account, self.fee, self.sequence, self.time_bounds, memo,
                                     operations, ext)

    def xdr(self):
        tx = Xdr.StellarXDRPacker()
        tx.pack_Transaction(self.to_xdr_object())
        return base64.b64encode(tx.get_buffer())

    @classmethod
    def from_xdr_object(cls, tx_xdr_object):
        source = encode_check('account', tx_xdr_object.sourceAccount.ed25519)
        sequence = tx_xdr_object.seqNum - 1
        time_bounds = tx_xdr_object.timeBounds  # TODO test

        memo_type = tx_xdr_object.memo.type
        memo_switch = tx_xdr_object.memo.switch
        if memo_type == Xdr.const.MEMO_TEXT:
            memo = TextMemo(memo_switch)
        elif memo_type == Xdr.const.MEMO_ID:
            memo = IdMemo(memo_switch)
        elif memo_type == Xdr.const.MEMO_HASH:
            memo = HashMemo(memo_switch)
        elif memo_type == Xdr.const.MEMO_RETURN:
            memo = RetHashMemo(memo_switch)
        else:
            memo = NoneMemo()

        fee = tx_xdr_object.fee

        operations = []
        ops = tx_xdr_object.operations
        for op in ops:
            if op.type == Xdr.const.CREATE_ACCOUNT:
                operations.append(CreateAccount.from_xdr_object(op))
            elif op.type == Xdr.const.PAYMENT:
                operations.append(Payment.from_xdr_object(op))
            elif op.type == Xdr.const.PATH_PAYMENT:
                operations.append(PathPayment.from_xdr_object(op))
            elif op.type == Xdr.const.CHANGE_TRUST:
                operations.append(ChangeTrust.from_xdr_object(op))
            elif op.type == Xdr.const.ALLOW_TRUST:
                operations.append(AllowTrust.from_xdr_object(op))
            elif op.type == Xdr.const.SET_OPTIONS:
                operations.append(SetOptions.from_xdr_object(op))
            elif op.type == Xdr.const.MANAGE_OFFER:
                operations.append(ManageOffer.from_xdr_object(op))
            elif op.type == Xdr.const.CREATE_PASSIVE_OFFER:
                operations.append(CreatePassiveOffer.from_xdr_object(op))
            elif op.type == Xdr.const.ACCOUNT_MERGE:
                operations.append(AccountMerge.from_xdr_object(op))
            elif op.type == Xdr.const.INFLATION:
                operations.append(Inflation.from_xdr_object(op))
            elif op.type == Xdr.const.MANAGE_DATA:
                operations.append(ManageData.from_xdr_object(op))

        return cls(
            source, {
                'sequence': sequence,
                'timeBounds': time_bounds,
                'memo': memo,
                'fee': fee,
                'operations': operations
            })
