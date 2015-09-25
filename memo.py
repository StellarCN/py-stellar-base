# coding: utf-8

from .stellarxdr import StellarXDR_pack as xdr


class Memo(object):

    @staticmethod
    def none():
        return xdr.types.Memo(type=xdr.const.MEMO_NONE)

    @staticmethod
    def text(text):
        if type(text) != str:
            raise Exception('Expects string type got a '+type(text))
        length = len(bytes(text, encoding='utf-8'))
        if length > 32:
            raise Exception("Text should be < 32 bytes (ascii encoded). Got " + str(length))
        return xdr.types.Memo(type=xdr.const.MEMO_TEXT, text=text)

    @staticmethod
    def id(id):
        # TODO int64
        return xdr.types.Memo(type=xdr.const.MEMO_ID, id=id)

    @staticmethod
    def hash(hash):
        if len(hash) != 32:
            raise Exception("Expects a 32 byte hash value. Got " + len(hash) + " bytes instead")
        return xdr.types.Memo(type=xdr.const.MEMO_HASH, hash=hash)

    @staticmethod
    def rethash(rethash):
        if len(rethash) != 32:
            raise Exception("Expects a 32 byte hash value. Got " + len(rethash) + " bytes instead")
        return xdr.types.Memo(type=xdr.const.MEMO_RETURN, rethash=rethash)
