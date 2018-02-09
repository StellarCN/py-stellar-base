# coding: utf-8

import requests

from .horizon import Horizon
from .keypair import Keypair
from .utils import AccountNotExistError, NotValidParamError
from .horizon import HORIZON_LIVE, HORIZON_TEST


class Address(object):
    """ check address info from stellar network using horizon rest api or SSE.

    """

    def __init__(self, address=None, secret=None, network='TESTNET', horizon=None):
        if address is None and secret is None:
            raise Exception('oops,need a stellar address or secret')
        if address is None and secret is not None:
            self.address = Keypair.from_seed(secret).address().decode()
        else:
            self.address = address
        self.secret = secret

        if network.upper() != 'PUBLIC':
            self.network = 'TESTNET'
        else:
            self.network = 'PUBLIC'
        if horizon:
            self.horizon = Horizon(horizon)
        elif network.upper() == 'PUBLIC':
            self.horizon = Horizon(HORIZON_LIVE)
        else:
            self.horizon = Horizon(HORIZON_TEST)

        self.sequence = None
        self.balances = None
        self.paging_token = None
        self.thresholds = None
        self.flags = None
        self.signers = None
        self.data = None

    def get(self):
        try:
            acc = self.horizon.account(self.address)
            if acc.get('sequence'):
                self.sequence = acc.get('sequence')
                self.balances = acc.get('balances')
                self.paging_token = acc.get('paging_token')
                self.thresholds = acc.get('thresholds')
                self.flags = acc.get('flags')
                self.signers = acc.get('signers')
                self.data = acc.get('data')
            elif acc.get('status') == 404:
                raise AccountNotExistError(acc.get('title'))
            else:
                raise Exception(acc.get('detail'))
        except requests.ConnectionError:
            raise Exception('network problem')

    def payments(self, sse=False, **kwargs):
        check_params(kwargs)
        return self.horizon.account_payments(self.address, params=kwargs, sse=sse)

    def offers(self, **kwargs):
        check_params(kwargs)
        return self.horizon.account_offers(self.address, params=kwargs)

    def transactions(self, sse=False, **kwargs):
        check_params(kwargs)
        return self.horizon.account_transactions(self.address, params=kwargs, sse=sse)

    def operations(self, sse=False, **kwargs):
        check_params(kwargs)
        return self.horizon.account_operations(self.address, params=kwargs, sse=sse)

    def effects(self, sse=False, **kwargs):
        check_params(kwargs)
        return self.horizon.account_effects(self.address, params=kwargs, sse=sse)


def check_params(data):
    params = {'cursor', 'limit', 'order'}
    for key in data.keys():
        if key not in params:
            raise NotValidParamError('not valid params')
