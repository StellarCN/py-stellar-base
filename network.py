# encoding:utf-8
from .hash import hash

Networks = {'PUBLIC': 'Public Global Stellar Network ; '
            'September 2015', 'TESTNET': 'Test SDF Network ; September 2015'}


class Network(object):

    @staticmethod
    def use_default():
        return Network.use_testnet_work()

    @staticmethod
    def use_public_network():
        return Network(Networks['PUBLIC'])

    @staticmethod
    def use_testnet_work():
        return Network(Networks['TESTNET'])

    def __init__(self, passphrase):
        self.passphrase = passphrase

    def network_id(self):
        return hash(self.passphrase.encode())
