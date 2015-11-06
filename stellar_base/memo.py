# coding: utf-8
from .utils import XdrLengthError
from .stellarxdr import StellarXDR_pack as Xdr


class NoneMemo (object):
    def __init__(self):
        pass

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_NONE)


class TextMemo (object):
    def __init__(self, text):
        if type(text) != str:
            raise TypeError('Expects string type got a ' + type(text))
        length = len(bytes(text, encoding='utf-8'))
        if length > 32:
            raise XdrLengthError("Text should be < 32 bytes (ascii encoded). Got ".format(str(length)))
        self.text = text

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_TEXT, text=self.text)


class IdMemo (object):
    def __init__(self, mid):
        self.mid = mid

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_ID, id=self.mid)


class HashMemo (object):
    def __init__(self, memo_hash):
        if len(memo_hash) != 32:
            raise XdrLengthError("Expects a 32 byte mhash value. Got {:d} bytes instead".format(len(memo_hash)))
        self.memo_hash = memo_hash

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_HASH, hash=self.memo_hash)


class RetHashMemo (object):
    def __init__(self, memo_return):
        if len(memo_return) != 32:
            raise XdrLengthError("Expects a 32 byte hash value. Got {:d} bytes instead".format(len(memo_return)))
        self.memo_return = memo_return

    def to_xdr_object(self):
        return Xdr.types.Memo(type=Xdr.const.MEMO_RETURN, retHash=self.memo_return)
