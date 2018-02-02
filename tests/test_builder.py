# encoding: utf-8
import json

import requests

from stellar_base.builder import Builder, HORIZON_TEST
from stellar_base.keypair import Keypair
from stellar_base.utils import SignatureExistError


class TestBuilder(object):
    def __init__(self):

        self.cold = Keypair.random()
        self.hot = Keypair.random()
        # self.hot = Keypair.from_seed('SECRET')
        # self.cold = Keypair.from_seed('SECRET')

    def test_builder(self):
        cold_account = self.cold.address().decode()
        hot_account = self.hot.address().decode()
        fund(cold_account)

        cold = Builder(self.cold.seed().decode()) \
            .append_create_account_op(hot_account, 200) \
            .append_set_options_op(inflation_dest=cold_account, set_flags=1,
                                   home_domain='256kw.com', master_weight=10,
                                   low_threshold=5, ) \
            .append_trust_op(cold_account, 'BEER', 1000, source=hot_account) \
            .append_allow_trust_op(hot_account, 'BEER', True)
        # append twice for test
        cold.append_payment_op(hot_account, 50.123, 'BEER', cold_account) \
            .append_payment_op(hot_account, 50.123, 'BEER', cold_account)

        cold.sign(self.hot.seed().decode())
        try:  # sign twice
            cold.sign(self.hot.seed().decode())
        except SignatureExistError:
            assert True
        except:
            assert False

        cold.sign()
        assert len(cold.te.signatures) == 2
        assert len(cold.ops) == 5

        try:
            response = cold.submit()
            print(response)
        except:
            assert False

    def test_builder_xdr(self):
        cold_account = self.cold.address().decode()
        hot_account = self.hot.address().decode()
        fund(cold_account)

        fund(hot_account)

        cold = Builder(self.cold.seed().decode()) \
            .append_trust_op(cold_account, 'BEER', 1000, hot_account) \
            .append_payment_op(hot_account, 100, 'BEER', cold_account) \
            .append_payment_op(cold_account, 2.222,
                               'BEER', cold_account, hot_account)
        xdr = cold.gen_xdr()
        hot = Builder(self.hot.seed().decode())
        hot.import_from_xdr(xdr)
        # hot.sign()

        try:
            response = hot.submit()
        except:
            assert False


def fund(address):
    for attempt in range(3):
        r = requests.get(HORIZON_TEST + '/friendbot?addr=' +
                         address)  # Get 10000 lumens
        t = r.text
        try:
            assert 'hash' in json.loads(
                t) or 'op_already_exists' in json.loads(t)
            return True
        except AssertionError:
            pass
    raise Exception("fund failed")
