# coding: utf-8
from .utils import xdr_hash

NETWORKS = {
    'PUBLIC': 'Public Global Stellar Network ; September 2015',
    'TESTNET': 'Test SDF Network ; September 2015'
}


class Network(object):
    """The :class:`Network` object, which represents a Stellar network.

    This class represents such a stellar network such as the public livenet and
    the Stellar Development Foundation Test network.

    :param str passphrase: The passphrase for the network

    """

    def __init__(self, passphrase=None):
        if passphrase is None:
            self.passphrase = NETWORKS['TESTNET']
        else:
            self.passphrase = passphrase

    def network_id(self):
        """Get the network ID of the network.

        Get the network ID of the network, which is an XDR hash of the
        passphrase.

        """
        return xdr_hash(self.passphrase.encode())


def test_network():
    """Get the :class:`Network` representing the Test Network."""
    return Network(NETWORKS['TESTNET'])


def live_network():
    """Get the :class:`Network` representing the live Network."""
    return Network(NETWORKS['PUBLIC'])
