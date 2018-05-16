# coding: utf-8

import requests

from .horizon import Horizon
from .keypair import Keypair
from .exceptions import AccountNotExistError, NotValidParamError
from .horizon import HORIZON_LIVE, HORIZON_TEST


class Address(object):
    """The :class:`Address` object, which represents an address (public key) on
    Stellar's network.

    An :class:`Address` is initialized via a public key string, or derived via
    a secret seed. The network on which the account exists is also specified,
    as it is used to verify and set attributes via connecting to Horizon. It
    mostly exists as a helper class for Horizon operations on a given account
    ID.

    :param str address: The address string that represents this
        :class:`Address`.
    :param str secret: The secret seed string that is used to derive the
        address for this :class:`Address`.
    :param str network: The network to connect to for verifying and retrieving
        additional attributes from. Must be either 'PUBLIC' or 'TESTNET'.
    :param Horizon horizon: The :class:`Horizon` instance to use for
        connecting to for additional information for the account to which this
        address corresponds to.

    """

    # TODO: Make network an enum
    def __init__(
            self, address=None, secret=None, network='TESTNET', horizon=None):
        if address is None and secret is None:
            # FIXME: Throw a better exception
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
            if isinstance(horizon, Horizon):
                self.horizon = horizon
            else:
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
        """Retrieve the account data that corresponds to this :class:`Address`.

        Retrieve the account data from Horizon for the account that corresponds
        to this :class:`Address`. Attempt to retrieve the following attributes
        from Horizon:

        * Sequence Number
        * Balances
        * Paging Token
        * Thresholds
        * Flags
        * Signers
        * Data

        :raises AccountNotExistError: If the account does not exist, shown by a
            404 response from a Horizon server.
        :raises Exception: If any other problems come up, or if a network
            connection happens.

        """
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
                # FIXME: Throw a more specific exception.
                raise Exception(acc.get('detail'))
        except requests.ConnectionError:
            raise Exception('network problem')

    def payments(self, sse=False, **kwargs):
        """Retrieve the payments JSON from this instance's Horizon server.

        Retrieve the payments JSON response for the account associated with
        this :class:`Address`.

        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        check_params(kwargs)
        return self.horizon.account_payments(
            self.address, params=kwargs, sse=sse)

    def offers(self, **kwargs):
        """Retrieve the offers JSON from this instance's Horizon server.

        Retrieve the offers JSON response for the account associated with
        this :class:`Address`.

        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        check_params(kwargs)
        return self.horizon.account_offers(self.address, params=kwargs)

    def transactions(self, sse=False, **kwargs):
        """Retrieve the transactions JSON from this instance's Horizon server.

        Retrieve the transactions JSON response for the account associated with
        this :class:`Address`.

        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        check_params(kwargs)
        return self.horizon.account_transactions(
            self.address, params=kwargs, sse=sse)

    def operations(self, sse=False, **kwargs):
        """Retrieve the operations JSON from this instance's Horizon server.

        Retrieve the operations JSON response for the account associated with
        this :class:`Address`.

        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        check_params(kwargs)
        return self.horizon.account_operations(
            self.address, params=kwargs, sse=sse)

    def effects(self, sse=False, **kwargs):
        """Retrieve the effects JSON from this instance's Horizon server.

        Retrieve the effects JSON response for the account associated with
        this :class:`Address`.

        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        check_params(kwargs)
        return self.horizon.account_effects(
            self.address, params=kwargs, sse=sse)


# TODO: Make this a private method of the Address class.
def check_params(data):
    """Check for appropriate keywords for a Horizon request method.

    Check a dict of arguments to make sure that they only contain allowable
    params for requests to Horizon, such as 'cursor', 'limit', and 'order'.

    """

    params_allowed = {'cursor', 'limit', 'order'}
    params = set(data.keys())
    if params - params_allowed:
        raise NotValidParamError('not valid params')
