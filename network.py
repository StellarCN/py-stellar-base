# encoding:utf-8
from .hash import hash

Networks = {
	'PUBLIC': 'Public Global Stellar Network ; September 2015',
	'TESTNET': 'Test SDF Network ; September 2015',
}

class Network(object):

    @staticmethod
    def useDefault():
        return Network.useTestNetwork()

    @staticmethod
    def usePublicNetwork():
        return Network(Networks['PUBLIC'])

    @staticmethod
    def useTestNetwork():
        return Network(Networks['TESTNET'])

    def __init__(self, passphrase):
        self.passphrase = passphrase

    def networkId(self):
        return hash(self.passphrase.encode())