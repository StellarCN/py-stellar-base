# coding: utf-8
import base64

from .stellarxdr import Xdr
from .exceptions import XdrLengthError

# TODO: Consider using six throughout the library?
# Compatibility for Python 3.x that don't have unicode type
try:
    type(unicode)
except NameError:
    unicode = str


# TODO: Consider making an abstract base class
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
    def __init__(self):
        pass

    def to_xdr_object(self):
        """Creates an XDR Memo object that represents this :class:`Memo`."""
        pass

    def xdr(self):
        """Packs and base64 encodes this :class:`Memo` as an XDR string."""
        x = Xdr.StellarXDRPacker()
        x.pack_Memo(self.to_xdr_object())
        return base64.b64encode(x.get_buffer())


class NoneMemo(Memo):
    """The :class:`NoneMemo`, which represents no memo for a transaction."""
    def __init__(self):
        pass

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
            raise TypeError('Expects string type got a ' + type(text).__name__)
        if bytes == str and not isinstance(text, unicode):
            # Python 2 without unicode string
            self.text = text
        else:
            # Python 3 or Python 2 with unicode string
            self.text = bytearray(text, encoding='utf-8')
        length = len(self.text)
        if length > 28:
            raise XdrLengthError(
                "Text should be <= 28 bytes (ascii encoded). "
                "Got {:s}".format(str(length)))

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

    :param bytes memo_hash: A 32 byte hash.

    """
    def __init__(self, memo_hash):
        if len(memo_hash) != 32:
            raise XdrLengthError(
                "Expects a 32 byte mhash value. "
                "Got {:d} bytes instead".format(len(memo_hash)))
        self.memo_hash = memo_hash

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with MEMO_HASH."""
        return Xdr.types.Memo(type=Xdr.const.MEMO_HASH, hash=self.memo_hash)


class RetHashMemo(Memo):
    """The :class:`RetHashMemo` which represents MEMO_RETURN in a transaction.

    MEMO_RETURN is typically used with refunds/returns over the network - it is
    a 32 byte hash intended to be interpreted as the hash of the transaction
    the sender is refunding.

    :param bytes memo_return: A 32 byte hash intended to be interpreted as the
        hash of the transaction the sender is refunding.

    """
    def __init__(self, memo_return):
        if len(memo_return) != 32:
            raise XdrLengthError(
                "Expects a 32 byte hash value. "
                "Got {:d} bytes instead".format(len(memo_return)))
        self.memo_return = memo_return

    def to_xdr_object(self):
        """Creates an XDR Memo object for a transaction with MEMO_RETURN."""
        return Xdr.types.Memo(
            type=Xdr.const.MEMO_RETURN, retHash=self.memo_return)
