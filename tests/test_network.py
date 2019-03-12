from stellar_base.network import test_network, live_network, Network, NETWORKS


class TestNetwork(object):
    def test_default_network(self):
        assert Network().passphrase == NETWORKS['TESTNET']

    def test_test_network(self):
        assert test_network().network_id() == Network(passphrase=NETWORKS['TESTNET']).network_id()

    def test_public_network(self):
        assert live_network().network_id() == Network(passphrase=NETWORKS['PUBLIC']).network_id()
