# coding: utf-8

import base64

from .memo import HashMemo, IdMemo, NoneMemo, RetHashMemo, TextMemo
from .operation import Operation
from .stellarxdr import Xdr
from .utils import account_xdr_object, encode_check, \
    is_valid_address


class Transaction(object):
    """The :class:`Transaction` object, which represents a transaction
    on Stellar's network.

    A transaction contains a list of operations (see :class:`Operation
    <stellar_base.operation.Operation>`),
    which are all executed in order as one ACID transaction, along with an
    associated source account, fee, account sequence number, list of
    signatures, both an optional memo and an optional timebound. Typically a
    :class:`Transaction` is placed in a :class:`TransactionEnvelope
    <stellar_base.transaction_envelope.TransactionEnvelope>` which is
    then signed before being sent over the network.

    For more information on Transactions in Stellar, see `Stellar's guide
    on transactions`_.

    .. _Stellar's guide on transactions:
        https://www.stellar.org/developers/guides/concepts/transactions.html

    :param str source: A strkey encoded account ID (public key) of the source
        account for the transaction.
    :param dict opts: A dict that contains the primary components of the
        transaction. The following keys are searched from the dict:

        * opts.sequence - The current sequence number of the source account.
          The sequence number is incremented by 1 automatically, as is
          necessary for a new transaction for a given source account.
        * opts.time_bounds - A list of two Unix timestamps representing the
          lower and upper bound of when a given transaction will be valid.
          NOTE: This should likely be an object containing a minTime and
          maxTime attribute instead, and the implementation may change.
        * opts.memo - The memo being sent with the transaction, being
          represented as one of the subclasses of the
          :class:`Memo <stellar_base.memo.Memo>` object.
          Defaults to :class:`NoneMemo <stellar_base.memo.NoneMemo>`.
        * opts.fee - The fee amount for the transaction, which should equal
          FEE (currently 100 stroops) multiplied by the number of
          operations in the transaction. See `Stellar's latest documentation
          on fees
          <https://www.stellar.org/developers/guides/concepts/fees.html#transaction-fee>`_
          for more information.
        * opts.operations: A list of :class:`Operation
          <stellar_base.operation.Operation>` objects (typically its
          subclasses as defined in :mod:`stellar_base.operation` to be
          included in the transaction. By default this is an empty list.

    """
    # TODO: Why is this passed in as a dictionary (outside of conforming to the
    # JavaScript SDK)? Wouldn't it make more sense to use optional arguments?
    # Several of the components in opts are also required. Especially because
    # they're just being shoved into typed attributes anyways?

    default_fee = 100

    def __init__(self, source, opts):
        opts = dict(opts)
        if not is_valid_address(source):
            raise ValueError('invalid source address: {}'.format(source))

        self.source = source
        self.sequence = int(opts.pop('sequence')) + 1
        # FIXME: Shouldn't timebounds be an object that contains minTime and
        # maxTime fields?
        self.time_bounds = opts.pop('timeBounds', [])
        self.memo = opts.pop('memo', NoneMemo())
        self.fee = int(opts.pop('fee', self.default_fee))
        self.operations = opts.pop('operations', [])
        if opts:
            raise ValueError(
                "Unknown arguments found in opts: {}".format(opts)
            )

    def add_operation(self, operation):
        """Add an :class:`Operation <stellar_base.operation.Operation>` to
        this transaction.

        This method will only add an operation if it is not already in the
        transaction's list of operations, i.e. every operation in the
        transaction should be unique.

        :param Operation operation: The operation to add to this transaction.

        """
        if operation not in self.operations:
            self.operations.append(operation)

    def to_xdr_object(self):
        """Creates an XDR Transaction object that represents this
        :class:`Transaction`.

        """
        source_account = account_xdr_object(self.source)
        memo = self.memo.to_xdr_object()
        operations = [o.to_xdr_object() for o in self.operations]
        ext = Xdr.nullclass()
        ext.v = 0
        return Xdr.types.Transaction(
            source_account, self.fee, self.sequence, self.time_bounds, memo,
            operations, ext)

    def xdr(self):
        """Packs and base64 encodes this :class:`Transaction` as an XDR
        string.

        """
        tx = Xdr.StellarXDRPacker()
        tx.pack_Transaction(self.to_xdr_object())
        return base64.b64encode(tx.get_buffer())

    @classmethod
    def from_xdr_object(cls, tx_xdr_object):
        """Create a :class:`Transaction` object from a Transaction XDR
        object.

        """
        source = encode_check('account', tx_xdr_object.sourceAccount.ed25519)
        sequence = tx_xdr_object.seqNum - 1
        time_bounds = tx_xdr_object.timeBounds  # TODO test

        memo_type = tx_xdr_object.memo.type
        memo_switch = tx_xdr_object.memo.switch
        if memo_type == Xdr.const.MEMO_TEXT:
            memo = TextMemo(memo_switch.decode())
        elif memo_type == Xdr.const.MEMO_ID:
            memo = IdMemo(memo_switch)
        elif memo_type == Xdr.const.MEMO_HASH:
            memo = HashMemo(memo_switch)
        elif memo_type == Xdr.const.MEMO_RETURN:
            memo = RetHashMemo(memo_switch)
        else:
            memo = NoneMemo()

        fee = tx_xdr_object.fee
        operations = list(map(
            Operation.from_xdr_object, tx_xdr_object.operations
        ))
        return cls(
            source, {
                'sequence': sequence,
                'timeBounds': time_bounds,
                'memo': memo,
                'fee': fee,
                'operations': operations
            })
