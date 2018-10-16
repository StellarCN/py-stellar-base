# coding: utf-8

import base64

from .memo import xdr_to_memo, NoneMemo
from .operation import Operation
from .stellarxdr import Xdr
from .stellarxdr.StellarXDR_type import TimeBounds
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
    :param sequence: The current sequence number of the source account.
          The sequence number is incremented by 1 automatically, as is
          necessary for a new transaction for a given source account.
    :type sequence: int, str
    :param dict time_bounds: A dict that contains a minTime and maxTime attribute
            (`{'minTime': 1534392138, 'maxTime': 1534392238}`) representing the
            lower and upper bound of when a given transaction will be valid.
    :param Memo memo: The memo being sent with the transaction, being
          represented as one of the subclasses of the
          :class:`Memo <stellar_base.memo.Memo>` object.
    :param int fee: The fee amount for the transaction, which should equal
          FEE (currently 100 stroops) multiplied by the number of
          operations in the transaction. See `Stellar's latest documentation
          on fees
          <https://www.stellar.org/developers/guides/concepts/fees.html#transaction-fee>`_
          for more information.
    :param list operations: A list of :class:`Operation
          <stellar_base.operation.Operation>` objects (typically its
          subclasses as defined in :mod:`stellar_base.operation` to be
          included in the transaction. By default this is an empty list.
    """

    default_fee = 100

    def __init__(self,
                 source,
                 sequence,
                 time_bounds=None,
                 memo=None,
                 fee=None,
                 operations=None):
        if not is_valid_address(source):
            raise ValueError('invalid source address: {}'.format(source))

        self.source = source
        self.sequence = int(sequence) + 1
        self.memo = memo or NoneMemo()
        self.fee = int(fee) if fee else self.default_fee
        self.operations = operations or []
        # self.time_bounds = [time_bounds['minTime'],
        #                     time_bounds['maxTime']] if time_bounds else []
        if time_bounds is None:
            self.time_bounds = []
        else:
            if not isinstance(time_bounds, dict):
                raise ValueError("time_bounds should be a dict that contains "
                                 "minTime and maxTime fields")
            self.time_bounds = [TimeBounds(minTime=time_bounds['minTime'],
                                           maxTime=time_bounds['maxTime'])]

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
        return Xdr.types.Transaction(source_account, self.fee, self.sequence,
                                     self.time_bounds, memo, operations, ext)

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
        time_bounds_in_xdr = tx_xdr_object.timeBounds  # TODO test
        if time_bounds_in_xdr:
            time_bounds = {
                'maxTime': time_bounds_in_xdr[0].maxTime,
                'minTime': time_bounds_in_xdr[0].minTime
            }
        else:
            time_bounds = None

        memo = xdr_to_memo(tx_xdr_object.memo)

        operations = list(map(
            Operation.from_xdr_object, tx_xdr_object.operations
        ))
        return cls(
            source=source,
            sequence=sequence,
            time_bounds=time_bounds,
            memo=memo,
            fee=tx_xdr_object.fee,
            operations=operations)
