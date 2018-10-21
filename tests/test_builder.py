# encoding: utf-8

import pytest

from stellar_base.builder import Builder
from stellar_base.keypair import Keypair
from stellar_base.exceptions import SignatureExistError

# TODO: These endpoints really need to be mocked out.


@pytest.fixture(scope='module')
def test_data(setup, helpers):
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)

    cold = Keypair.random()
    cold_secret = cold.seed()
    cold_account = cold.address().decode()

    helpers.fund_account(setup, cold.address().decode())

    return Struct(cold_secret=cold_secret, cold_account=cold_account)


def test_builder(setup, test_data):
    hot = Keypair.random()
    hot_account = hot.address().decode()
    hot_secret = hot.seed()

    cold = Builder(secret=test_data.cold_secret, horizon_uri=setup.horizon_endpoint_uri, network=setup.network) \
        .append_create_account_op(hot_account, '200') \
        .append_set_options_op(inflation_dest=test_data.cold_account, set_flags=1,
                               home_domain='256kw.com', master_weight=10,
                               low_threshold=5, ) \
        .append_change_trust_op('BEER', test_data.cold_account, '1000', hot_account) \
        .append_allow_trust_op(hot_account, 'BEER', True)
    # append twice for test
    cold.append_payment_op(hot_account, '50.123', 'BEER', test_data.cold_account) \
        .append_payment_op(hot_account, '50.123', 'BEER', test_data.cold_account)
    # TODO: append_bump_sequence_op test
    cold.sign()
    cold.sign(hot_secret)
    # try to sign twice
    with pytest.raises(SignatureExistError):
        cold.sign(hot_secret)

    assert len(cold.te.signatures) == 2
    assert len(cold.ops) == 5

    response = cold.submit()
    assert response.get('hash') == cold.hash_hex()


def test_builder_xdr(setup, helpers, test_data):
    hot = Keypair.random()
    hot_account = hot.address().decode()
    hot_secret = hot.seed()

    helpers.fund_account(setup, hot_account)

    cold = Builder(secret=test_data.cold_secret, horizon_uri=setup.horizon_endpoint_uri, network=setup.network) \
        .append_change_trust_op('BEER', test_data.cold_account, '1000', hot_account) \
        .append_allow_trust_op(hot_account, 'BEER', True, test_data.cold_account) \
        .append_payment_op(hot_account, '100', 'BEER', test_data.cold_account, test_data.cold_account) \
        .append_payment_op(test_data.cold_account, '2.222', 'BEER', test_data.cold_account, hot_account)
    cold.sign()

    xdr = cold.gen_xdr()

    hot = Builder(
        secret=hot_secret,
        horizon_uri=setup.horizon_endpoint_uri,
        network=setup.network)
    hot.import_from_xdr(xdr)
    hot.sign()

    assert len(hot.te.signatures) == 2
    assert len(hot.ops) == 4

    response = hot.submit()
    assert response.get('hash') == hot.hash_hex()
