from .utils import sha256


class Network:
    def __init__(self, network_passphrase: str) -> None:
        self.network_passphrase = network_passphrase

    def network_id(self) -> bytes:
        return sha256(self.network_passphrase.encode())

    def __eq__(self, other: 'Network') -> bool:
        return self.network_passphrase == other.network_passphrase


PUBLIC_NETWORK_PASSPHRASE: str = 'Public Global Stellar Network ; September 2015'
TESTNET_NETWORK_PASSPHRASE: str = 'Test SDF Network ; September 2015'

PUBLIC: Network = Network(PUBLIC_NETWORK_PASSPHRASE)
TESTNET: Network = Network(TESTNET_NETWORK_PASSPHRASE)
