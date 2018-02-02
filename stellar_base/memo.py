# coding: utf-8
import base64

from .stellarxdr import Xdr
from .utils import XdrLengthError

# Compatibility for Python 3.x that don't have unicode type
try:
    type(unicode)
except NameError:
    unicode = str


class Memo(object):
    # def __init__(self):
    #     pass

    def to_xdr_object(self):
        pass

    def xdr(self):
        x = Xdr.StellarXDRPacker()
        x.pack_Memo(self.to_xdr_object())
        return base64.b64encode(x.get_buffer())


class NoneMemo(Memo):
    def __init__(self):
        pass

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_NONE)


class TextMemo(Memo):
    def __init__(self, text):
        if not isinstance(text, (str, unicode)):
            raise TypeError('Expects string type got a ' + type(text).__name__)
        if bytes == str and not isinstance(text, unicode):  # Python 2 without unicode string
            self.text = text
        else:  # python 3 or python 2 with unicode string
            self.text = bytearray(text, encoding='utf-8')
        length = len(self.text)
        if length > 28:
            raise XdrLengthError("Text should be <= 28 bytes (ascii encoded). Got {:s}".format(str(length)))

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_TEXT, text=self.text)


class IdMemo(Memo):
    def __init__(self, memo_id):
        self.memo_id = int(memo_id)

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_ID, id=self.memo_id)


class HashMemo(Memo):
    def __init__(self, memo_hash):
        if len(memo_hash) != 32:
            raise XdrLengthError("Expects a 32 byte mhash value. Got {:d} bytes instead".format(len(memo_hash)))
        self.memo_hash = memo_hash

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_HASH, hash=self.memo_hash)


class RetHashMemo(Memo):
    def __init__(self, memo_return):
        if len(memo_return) != 32:
            raise XdrLengthError("Expects a 32 byte hash value. Got {:d} bytes instead".format(len(memo_return)))
        self.memo_return = memo_return

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_RETURN, retHash=self.memo_return)
