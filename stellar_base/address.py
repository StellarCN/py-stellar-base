# coding: utf-8

from .horizon import Horizon
from .keypair import Keypair
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
        additional attributes from. 'PUBLIC' is an alias for 'Public Global Stellar Network ; September 2015',
        'TESTNET' is an alias for 'Test SDF Network ; September 2015'. Defaults to TESTNET.
    :param str horizon_uri: The horizon url to use for
        connecting to for additional information for the account to which this
        address corresponds to.
    """

    # TODO: Make network an enum
    def __init__(self,
                 address=None,
                 secret=None,
                 network='TESTNET',
                 horizon_uri=None):
        if secret:
            self.address = Keypair.from_seed(secret).address().decode()
        elif address:
            self.address = Keypair.from_address(address).address().decode()
        else:
            raise ValueError('oops, need a stellar address or secret')

        if network.upper() != 'PUBLIC':
            self.network = 'TESTNET'
        else:
            self.network = 'PUBLIC'

        if horizon_uri:
            self.horizon = Horizon(horizon_uri)
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
        self.inflation_destination = None
        self.subentry_count = None

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
        * Inflation Destination
        * Subentry Count

        """

        acc = self.horizon.account(self.address)
        self.sequence = acc.get('sequence')
        self.balances = acc.get('balances')
        self.paging_token = acc.get('paging_token')
        self.thresholds = acc.get('thresholds')
        self.flags = acc.get('flags')
        self.signers = acc.get('signers')
        self.data = acc.get('data')
        self.inflation_destination = acc.get('inflation_destination')
        self.subentry_count = acc.get('subentry_count')

    def payments(self, cursor=None, order='asc', limit=10, sse=False):
        """Retrieve the payments JSON from this instance's Horizon server.

        Retrieve the payments JSON response for the account associated with
        this :class:`Address`.

        :param cursor: A paging token, specifying where to start returning records from.
            When streaming this can be set to "now" to stream object created since your request time.
        :type cursor: int, str
        :param str order: The order in which to return rows, "asc" or "desc".
        :param int limit: Maximum number of records to return.
        :param bool sse: Use server side events for streaming responses.

        """
        return self.horizon.account_payments(address=self.address, cursor=cursor, order=order, limit=limit, sse=sse)

    def offers(self, cursor=None, order='asc', limit=10, sse=False):
        """Retrieve the offers JSON from this instance's Horizon server.

        Retrieve the offers JSON response for the account associated with
        this :class:`Address`.

        :param cursor: A paging token, specifying where to start returning records from.
            When streaming this can be set to "now" to stream object created since your request time.
        :type cursor: int, str
        :param str order: The order in which to return rows, "asc" or "desc".
        :param int limit: Maximum number of records to return.
        :param bool sse: Use server side events for streaming responses.

        """
        return self.horizon.account_offers(self.address, cursor=cursor, order=order, limit=limit, sse=sse)

    def transactions(self, cursor=None, order='asc', limit=10, sse=False):
        """Retrieve the transactions JSON from this instance's Horizon server.

        Retrieve the transactions JSON response for the account associated with
        this :class:`Address`.

        :param cursor: A paging token, specifying where to start returning records from.
            When streaming this can be set to "now" to stream object created since your request time.
        :type cursor: int, str
        :param str order: The order in which to return rows, "asc" or "desc".
        :param int limit: Maximum number of records to return.
        :param bool sse: Use server side events for streaming responses.
        """
        return self.horizon.account_transactions(
            self.address, cursor=cursor, order=order, limit=limit, sse=sse)

    def operations(self, cursor=None, order='asc', limit=10, sse=False):
        """Retrieve the operations JSON from this instance's Horizon server.

        Retrieve the operations JSON response for the account associated with
        this :class:`Address`.

        :param cursor: A paging token, specifying where to start returning records from.
            When streaming this can be set to "now" to stream object created since your request time.
        :type cursor: int, str
        :param str order: The order in which to return rows, "asc" or "desc".
        :param int limit: Maximum number of records to return.
        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        return self.horizon.account_operations(
            self.address, cursor=cursor, order=order, limit=limit, sse=sse)

    def trades(self, cursor=None, order='asc', limit=10, sse=False):
        """Retrieve the trades JSON from this instance's Horizon server.

        Retrieve the trades JSON response for the account associated with
        this :class:`Address`.

        :param cursor: A paging token, specifying where to start returning records from.
            When streaming this can be set to "now" to stream object created since your request time.
        :type cursor: int, str
        :param str order: The order in which to return rows, "asc" or "desc".
        :param int limit: Maximum number of records to return.
        :param bool sse: Use the SSE client for connecting to Horizon.
        """
        return self.horizon.account_trades(
            self.address, cursor=cursor, order=order, limit=limit, sse=sse)

    def effects(self, cursor=None, order='asc', limit=10, sse=False):
        """Retrieve the effects JSON from this instance's Horizon server.

        Retrieve the effects JSON response for the account associated with
        this :class:`Address`.

        :param cursor: A paging token, specifying where to start returning records from.
            When streaming this can be set to "now" to stream object created since your request time.
        :type cursor: int, str
        :param str order: The order in which to return rows, "asc" or "desc".
        :param int limit: Maximum number of records to return.
        :param bool sse: Use the SSE client for connecting to Horizon.

        """
        return self.horizon.account_effects(
            self.address, cursor=cursor, order=order, limit=limit, sse=sse)
