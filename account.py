# coding:utf-8


from . import strkey


class Account():

    def __init__(self,address,sequence):
        self.address = address
        self.sequence = sequence

    @staticmethod
    def isValidAddress(address):
        try:
            decoded = strkey.decodeCheck("accountId", address)
            if len(decoded) is not 32:
                return False
        except:
            return False
        return True
