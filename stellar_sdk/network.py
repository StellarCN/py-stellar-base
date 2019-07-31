from .utils import sha256


class Network:
    def __init__(self, network_passphrase: str) -> None:
        self.network_passphrase = network_passphrase

    def network_id(self) -> bytes:
        return sha256(self.network_passphrase.encode())

    def __eq__(self, other: 'Network') -> bool:
        return self.network_passphrase == other.network_passphrase


_network_passphrases = {
    'PUBLIC': 'Public Global Stellar Network ; September 2015',
    'TESTNET': 'Test SDF Network ; September 2015'
}

PUBLIC = Network(_network_passphrases['PUBLIC'])  # type: Network
TESTNET = Network(_network_passphrases['TESTNET'])  # type: Network
