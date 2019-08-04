from .utils import sha256


class Network:
    """The :class:`Network` object, which represents a Stellar network.

    This class represents such a stellar network such as the Public network and the Test network.

    :param str network_passphrase: The passphrase for the network.
        (ex. 'Public Global Stellar Network ; September 2015')

    """

    def __init__(self, network_passphrase: str) -> None:
        self.network_passphrase = network_passphrase

    def network_id(self) -> bytes:
        """Get the network ID of the network, which is an XDR hash of the
        passphrase.

        :returns: The network ID of the network.
        """
        return sha256(self.network_passphrase.encode())

    def __eq__(self, other: "Network") -> bool:
        if not isinstance(other, Network):
            return False
        return self.network_passphrase == other.network_passphrase


PUBLIC_NETWORK_PASSPHRASE: str = "Public Global Stellar Network ; September 2015"
"""Get the Public network passphrase."""

TESTNET_NETWORK_PASSPHRASE: str = "Test SDF Network ; September 2015"
"""Get the Test network passphrase."""

PUBLIC: Network = Network(PUBLIC_NETWORK_PASSPHRASE)
"""Get the :class:`Network` representing the PUBLIC Network."""

TESTNET: Network = Network(TESTNET_NETWORK_PASSPHRASE)
"""Get the :class:`Network` representing the Test Network."""
