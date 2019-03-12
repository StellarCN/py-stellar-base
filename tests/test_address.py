import pytest

from stellar_base import Keypair, Address, Horizon
from stellar_base.exceptions import NotValidParamError
from stellar_base.horizon import HORIZON_TEST, HORIZON_LIVE


@pytest.fixture(scope='class')
def test_data(setup, helpers):
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    keypair = Keypair.random()
    address = keypair.address().decode()
    seed = keypair.seed().decode()
    helpers.fund_account(setup, address)
    return Struct(address=address, seed=seed, horizon_endpoint_uri=setup.horizon_endpoint_uri)


class TestAddress(object):
    def test_seed(self, test_data):
        addr = Address(secret=test_data.seed)
        assert addr.address == test_data.address

    def test_no_address_and_seed_raise(self):
        with pytest.raises(NotValidParamError, match="oops, need a stellar address or secret"):
            Address()

    def test_network(self, test_data):
        assert Address(secret=test_data.seed).network == 'TESTNET'
        assert Address(secret=test_data.seed, network='PUBLIC').network == 'PUBLIC'

    def test_horizon_uri(self, test_data):
        assert Address(secret=test_data.seed).horizon.horizon_uri == Horizon(HORIZON_TEST).horizon_uri
        assert Address(secret=test_data.seed, network='PUBLIC').horizon.horizon_uri == Horizon(HORIZON_LIVE).horizon_uri
        assert Address(secret=test_data.seed,
                       horizon_uri=test_data.horizon_endpoint_uri).horizon.horizon_uri == Horizon(
            horizon_uri=test_data.horizon_endpoint_uri).horizon_uri

    def test_get_data(self, test_data):
        addr = Address(address=test_data.address, horizon_uri=test_data.horizon_endpoint_uri)
        addr.get()
        assert int(addr.sequence) > 0
        for resp in (
        addr.payments(), addr.operations(), addr.effects(), addr.offers(), addr.trades(), addr.transactions()):
            assert isinstance(resp['_embedded']['records'], list)
