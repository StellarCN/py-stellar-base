# coding: utf-8

from .stellarxdr import StellarXDR_pack as Xdr


class Memo(object):

    @staticmethod
    def none():
        return Xdr.types.Memo(type=Xdr.const.MEMO_NONE)

    @staticmethod
    def text(text):
        if type(text) != str:
            raise Exception('Expects string type got a '+type(text))
        length = len(bytes(text, encoding='utf-8'))
        if length > 32:
            raise Exception("Text should be < 32 bytes (ascii encoded). Got " + str(length))
        return Xdr.types.Memo(type=Xdr.const.MEMO_TEXT, text=text)

    @staticmethod
    def id(mid):
        # TODO int64
        return Xdr.types.Memo(type=Xdr.const.MEMO_ID, id=mid)

    @staticmethod
    def hash(mhash):
        if len(mhash) != 32:
            raise Exception("Expects a 32 byte mhash value. Got " + str(len(mhash)) + " bytes instead")
        return Xdr.types.Memo(type=Xdr.const.MEMO_HASH, hash=mhash)

    @staticmethod
    def rethash(rethash):
        if len(rethash) != 32:
            raise Exception("Expects a 32 byte hash value. Got " + str(len(rethash)) + " bytes instead")
        return Xdr.types.Memo(type=Xdr.const.MEMO_RETURN, retHash=rethash)
    Xdr.types.Memo()
