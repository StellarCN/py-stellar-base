from stellar_sdk.network import Network


class TestNetwork:
    public_passphrase = "Public Global Stellar Network ; September 2015"
    testnet_passphrase = "Test SDF Network ; September 2015"

    def test_create_a_network(self):
        network_passphrase = "Public Global Kawaii Network ; September 2019"
        network = Network(network_passphrase)
        assert network.network_passphrase == network_passphrase
        assert (
            network.network_id().hex()
            == "f5a9e59584de0bbe40b875e44be3a0d53ce78d7579fff1f7f8c902d5eb723c70"
        )

    def test_public(self):
        assert Network.public_network().network_passphrase == self.public_passphrase
        assert (
            Network.public_network().network_id().hex()
            == "7ac33997544e3175d266bd022439b22cdb16508c01163f26e5cb2a3e1045a979"
        )

    def test_testnet(self):
        assert Network.testnet_network().network_passphrase == self.testnet_passphrase
        assert (
            Network.testnet_network().network_id().hex()
            == "cee0302d59844d32bdca915c8203dd44b33fbb7edc19051ea37abedf28ecd472"
        )

    def test_equals(self):
        assert Network(self.public_passphrase) == Network.public_network()
        assert Network(self.testnet_passphrase) == Network.testnet_network()
        assert Network(self.public_passphrase) != Network(self.testnet_passphrase)
