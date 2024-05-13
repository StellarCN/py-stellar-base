from .utils import sha256

__all__ = ["Network"]


class Network:
    """The :class:`Network` object, which represents a Stellar network.

    This class represents such a stellar network such as the Public network and the Test network.

    :param network_passphrase: The passphrase for the network.
        (ex. ``"Public Global Stellar Network ; September 2015"``)

    """

    PUBLIC_NETWORK_PASSPHRASE: str = "Public Global Stellar Network ; September 2015"
    """The Public network passphrase."""

    TESTNET_NETWORK_PASSPHRASE: str = "Test SDF Network ; September 2015"
    """The Test network passphrase."""

    FUTURENET_NETWORK_PASSPHRASE: str = "Test SDF Future Network ; October 2022"
    """The Future network passphrase."""

    STANDALONE_NETWORK_PASSPHRASE: str = "Standalone Network ; February 2017"
    """The Standalone network passphrase."""

    SANDBOX_NETWORK_PASSPHRASE = "Local Sandbox Stellar Network ; September 2022"
    """The Sandbox network passphrase."""

    def __init__(self, network_passphrase: str) -> None:
        self.network_passphrase: str = network_passphrase

    def network_id(self) -> bytes:
        """Get the network ID of the network, which is an hash of the
        passphrase.

        :returns: The network ID of the network.
        """
        return sha256(self.network_passphrase.encode())

    @classmethod
    def public_network(cls) -> "Network":
        """Get the :class:`Network` object representing the PUBLIC Network.

        :return: PUBLIC Network
        """
        return cls(cls.PUBLIC_NETWORK_PASSPHRASE)

    @classmethod
    def testnet_network(cls) -> "Network":
        """Get the :class:`Network` object representing the TESTNET Network.

        :return: TESTNET Network
        """
        return cls(cls.TESTNET_NETWORK_PASSPHRASE)

    def __hash__(self):
        return hash(self.network_passphrase)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.network_passphrase == other.network_passphrase

    def __repr__(self):
        return f"<Network [network_passphrase={self.network_passphrase}]>"
