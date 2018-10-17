# coding: utf-8
import sys
import six
import abc
import base64

from stellar_base.utils import convert_hex_to_bytes
from .stellarxdr import Xdr
from .exceptions import XdrLengthError

if sys.version_info.major == 3:
    unicode = str


@six.add_metaclass(abc.ABCMeta)
class Memo(object):
    """The :class:`Memo` object, which represents the base class for memos for
    use with Stellar transactions.

    The memo for a transaction contains optional extra information about the
    transaction taking place. It is the responsibility of the client to
    interpret this value.

    See the following implementations that serve a more practical use with the
    library:

    * :class:`NoneMemo` - No memo.
    * :class:`TextMemo` - A string encoded using either ASCII or UTF-8, up to
        28-bytes long.
    * :class:`IdMemo` - A 64 bit unsigned integer.
    * :class:`HashMemo` - A 32 byte hash.
    * :class:`RetHashMemo` -  A 32 byte hash intended to be interpreted as the
        hash of the transaction the sender is refunding.

    See `Stellar's documentation on Transactions
    <https://www.stellar.org/developers/guides/concepts/transactions.html>`_
    for more information on how memos are used within transactions, as well as
    information on the available types of memos.

    """

    @abc.abstractmethod
    def to_xdr_object(self):
        """Creates an XDR Memo object that represents this :class:`Memo`."""

    @classmethod
    def from_xdr_object(cls, xdr_obj):
        return cls(xdr_obj.switch)

    def xdr(self):
        """Packs and base64 encodes this :class:`Memo` as an XDR string."""
        x = Xdr.StellarXDRPacker()
        x.pack_Memo(self.to_xdr_object())
        return base64.b64encode(x.get_buffer())

    def __eq__(self, other):
        return self.xdr() == other.xdr()


class NoneMemo(Memo):
    """The :class:`NoneMemo`, which represents no memo for a transaction."""

    @classmethod
    def from_xdr_object(cls, _xdr_obj):
        return cls()

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with no memo."""
        return Xdr.types.Memo(type=Xdr.const.MEMO_NONE)


class TextMemo(Memo):
    """The :class:`TextMemo`, which represents MEMO_TEXT in a transaction.

    :param str text: A string encoded using either ASCII or UTF-8, up to
        28-bytes long.

    """

    def __init__(self, text):
        if not isinstance(text, (str, unicode)):
            raise TypeError('Expects string type got a {}'.format(type(text)))
        if bytes == str and not isinstance(text, unicode):
            # Python 2 without unicode string
            self.text = text
        else:
            # Python 3 or Python 2 with unicode string
            self.text = bytearray(text, encoding='utf-8')
        length = len(self.text)
        if length > 28:
            raise XdrLengthError("Text should be <= 28 bytes (ascii encoded). "
                                 "Got {:s}".format(str(length)))

    @classmethod
    def from_xdr_object(cls, xdr_obj):
        return cls(xdr_obj.switch.decode())

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with MEMO_TEXT."""
        return Xdr.types.Memo(type=Xdr.const.MEMO_TEXT, text=self.text)


class IdMemo(Memo):
    """The :class:`IdMemo` which represents MEMO_ID in a transaction.

    :param int memo_id: A 64 bit unsigned integer.

    """

    def __init__(self, memo_id):
        self.memo_id = int(memo_id)

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with MEMO_ID."""
        return Xdr.types.Memo(type=Xdr.const.MEMO_ID, id=self.memo_id)


class HashMemo(Memo):
    """The :class:`HashMemo` which represents MEMO_HASH in a transaction.

    :param memo_hash: A 32 byte hash or hex encoded string.
    :type memo_hash: bytes, str
    """

    def __init__(self, memo_hash):
        self.memo_hash = convert_hex_to_bytes(memo_hash)

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with MEMO_HASH."""
        return Xdr.types.Memo(type=Xdr.const.MEMO_HASH, hash=self.memo_hash)


class RetHashMemo(Memo):
    """The :class:`RetHashMemo` which represents MEMO_RETURN in a transaction.

    MEMO_RETURN is typically used with refunds/returns over the network - it is
    a 32 byte hash intended to be interpreted as the hash of the transaction
    the sender is refunding.

    :param memo_return: A 32 byte hash or hex encoded string intended to be interpreted as the
        hash of the transaction the sender is refunding.
    :type memo_return: bytes, str

    """

    def __init__(self, memo_return):
        self.memo_return = convert_hex_to_bytes(memo_return)

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with MEMO_RETURN."""
        return Xdr.types.Memo(
            type=Xdr.const.MEMO_RETURN, retHash=self.memo_return)


_xdr_type_map = {
    Xdr.const.MEMO_TEXT: TextMemo,
    Xdr.const.MEMO_ID: IdMemo,
    Xdr.const.MEMO_HASH: HashMemo,
    Xdr.const.MEMO_RETURN: RetHashMemo
}


def xdr_to_memo(xdr_obj):
    memo_cls = _xdr_type_map.get(xdr_obj.type, NoneMemo)
    return memo_cls.from_xdr_object(xdr_obj)
