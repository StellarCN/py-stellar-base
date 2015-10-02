# coding:utf-8


from . import strkey


class Account(object):

    def __init__(self, address, sequence):
        self.address = address
        self.sequence = sequence

    @staticmethod
    def is_valid_address(address):
        try:
            decoded = strkey.decode_check("account_id", address)
            if len(decoded) is not 32:
                return False
        except:
            return False
        return True
