# coding: utf-8

import requests
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE
from requests.exceptions import RequestException
from requests.compat import urljoin
from time import sleep
from urllib3.util import Retry

from .exceptions import HorizonError

import logging

logger = logging.getLogger(__name__)

try:
    from sseclient import SSEClient
except ImportError:
    SSEClient = None

HORIZON_LIVE = "https://horizon.stellar.org"
HORIZON_TEST = "https://horizon-testnet.stellar.org"
DEFAULT_REQUEST_TIMEOUT = 11  # two ledgers + 1 sec, let's retry faster and not wait 60 secs.
DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = 'py-stellar-base'


class Horizon(object):
    def __init__(self,
                 horizon_uri=None,
                 pool_size=DEFAULT_POOLSIZE,
                 num_retries=DEFAULT_NUM_RETRIES,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT,
                 backoff_factor=DEFAULT_BACKOFF_FACTOR,
                 user_agent=USER_AGENT):
        """The :class:`Horizon` object, which represents the interface for
        making requests to a Horizon server instance.

        This class aims to be up to date with Horizon's API endpoints; however,
        you can utilize the internal session via ``self.session`` (which is a
        :class:`requests.Session` object) to make arbitrary requests to
        a Horizon instance's API.

        In general, on HTTP errors (non 2XX/3XX responses), no exception is
        raised, and the return dictionary must be checked to see if it is an
        error or a valid response. Any other errors however are raised by this
        class.

        :param str horizon_uri: The horizon base URL
        :param int timeout: The timeout for all requests.
        :param int pool_size persistent connection to Horizon and connection pool
        :param int num_retries configurable request retry functionality
        :param float backoff_factor a backoff factor to apply between attempts after the second try
        :param str user_agent String representing the user-agent you want, such as "py-stellar-base"

        """
        if horizon_uri is None:
            self.horizon_uri = HORIZON_TEST
        else:
            self.horizon_uri = horizon_uri

        self.pool_size = pool_size
        self.num_retries = num_retries
        self.request_timeout = request_timeout
        self.backoff_factor = backoff_factor

        # adding 504 to the list of statuses to retry
        self.status_forcelist = list(
            Retry.RETRY_AFTER_STATUS_CODES).append(504)

        # configure standard session

        # configure retry handler
        retry = Retry(
            total=self.num_retries,
            backoff_factor=self.backoff_factor,
            redirect=0,
            status_forcelist=self.status_forcelist)
        # init transport adapter
        adapter = HTTPAdapter(
            pool_connections=self.pool_size,
            pool_maxsize=self.pool_size,
            max_retries=retry)

        # init session
        session = requests.Session()

        # set default headers
        session.headers.update({'User-Agent': user_agent})

        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self._session = session

        # configure SSE session (differs from our standard session)

        sse_retry = Retry(
            total=1000000, redirect=0, status_forcelist=self.status_forcelist)
        sse_adapter = HTTPAdapter(
            pool_connections=self.pool_size,
            pool_maxsize=self.pool_size,
            max_retries=sse_retry)
        sse_session = requests.Session()
        sse_session.headers.update({'User-Agent': user_agent})
        sse_session.mount('http://', sse_adapter)
        sse_session.mount('https://', sse_adapter)
        self._sse_session = sse_session

    def submit(self, te):
        """Submit the transaction using a pooled connection, and retry on failure.

        `POST /transactions
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-create.html>`_

        Uses form-encoded data to send over to Horizon.

        :return: The JSON response indicating the success/failure of the
            submitted transaction.
        :rtype: dict

        """
        params = {'tx': te}
        url = urljoin(self.horizon_uri, 'transactions/')

        # POST is not included in Retry's method_whitelist for a good reason.
        # our custom retry mechanism follows
        reply = None
        retry_count = self.num_retries
        while True:
            try:
                reply = self._session.post(
                    url, data=params, timeout=self.request_timeout)
                return check_horizon_reply(reply.json())
            except (RequestException, ValueError) as e:
                if reply:
                    msg = 'horizon submit exception: {}, reply: [{}] {}'.format(
                        str(e), reply.status_code, reply.text)
                else:
                    msg = 'horizon submit exception: {}'.format(str(e))
                logging.warning(msg)

                if reply and reply.status_code not in self.status_forcelist:
                    raise Exception('invalid horizon reply: [{}] {}'.format(
                        reply.status_code, reply.text))
                # retry
                if retry_count <= 0:
                    raise
                retry_count -= 1
                logging.warning('submit retry attempt {}'.format(retry_count))
                sleep(self.backoff_factor)

    def query(self, rel_url, params=None, sse=False):
        abs_url = urljoin(self.horizon_uri, rel_url)
        reply = self._query(abs_url, params, sse)
        return check_horizon_reply(reply) if not sse else reply

    def _query(self, url, params=None, sse=False):
        if not sse:
            reply = self._session.get(
                url, params=params, timeout=self.request_timeout)
            try:
                return reply.json()
            except ValueError:
                raise Exception('invalid horizon reply: [{}] {}'.format(
                    reply.status_code, reply.text))

        # SSE connection
        if SSEClient is None:
            raise ValueError('SSE not supported, missing sseclient module')

        return SSEClient(url, retry=0, session=self._sse_session, connect_retry=-1, params=params)

    def account(self, address):
        """Returns information and links relating to a single account.

        `GET /accounts/{account}
        <https://www.stellar.org/developers/horizon/reference/endpoints/accounts-single.html>`_

        :param str address: The account ID to retrieve details about
        :return: The account details in a JSON response
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}'.format(account_id=address)
        return self.query(endpoint)

    def account_data(self, account_id, data_key):
        """This endpoint represents a single data associated with a given
        account.

        `GET /accounts/{account}/data/{key}
        <https://www.stellar.org/developers/horizon/reference/endpoints/data-for-account.html>`_

        :param str account_id: The account ID to look up a data item from
        :param str data_key: The name of the key for the data item in question
        :return: The value of the data field for the given account and data
            key
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}/data/{data_key}'.format(
            account_id=account_id, data_key=data_key)
        return self.query(endpoint)

    def account_effects(self, address, params=None, sse=False):
        """This endpoint represents all effects that changed a given account.

        `GET /accounts/{account}/effects{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-account.html>`_

        :param str address: The account ID to look up effects for.
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: The list of effects in a JSON response.
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}/effects'.format(account_id=address)
        return self.query(endpoint, params, sse)

    def account_offers(self, address, params=None):
        """This endpoint represents all the offers a particular account makes.

        `GET /accounts/{account}/offers{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/offers-for-account.html>`_

        :param str address: The account ID to retrieve offers from
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: The list of offers for an account in a JSON response.
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}/offers'.format(account_id=address)
        return self.query(endpoint, params)

    def account_operations(self, address, params=None, sse=False):
        """This endpoint represents all operations that were included in valid
        transactions that affected a particular account.

        `GET /accounts/{account}/operations{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-account.html>`_

        :param str address: The account ID to list operations on
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: The list of operations for an account in a JSON response.
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}/operations'.format(
            account_id=address)
        return self.query(endpoint, params, sse)

    def account_transactions(self, address, params=None, sse=False):
        """This endpoint represents all transactions that affected a given
        account.

        `GET /accounts/{account_id}/transactions{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-for-account.html>`_

        :param str address: The account ID to list transactions from
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: The list of transactions for an account in a JSON response.
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}/transactions'.format(
            account_id=address)
        return self.query(endpoint, params, sse)

    def account_payments(self, address, params=None, sse=False):
        """This endpoint responds with a collection of Payment operations where
        the given account was either the sender or receiver.

        `GET /accounts/{id}/payments{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-account.html>`_

        :param str address: The account ID to list payments to/from
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: The list of payments for an account in a JSON response.
        :rtype: dict

        """
        endpoint = '/accounts/{account_id}/payments'.format(account_id=address)
        return self.query(endpoint, params, sse)

    def assets(self, params=None):
        """This endpoint represents all assets. It will give you all the assets
        in the system along with various statistics about each.

        See the documentation below for details on query parameters that are
        available.

        `GET /assets{?asset_code,asset_issuer,cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/assets-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: A list of all valid payment operations
        :rtype: dict

        """
        endpoint = '/assets/'
        return self.query(endpoint, params)

    def transactions(self, params=None, sse=False):
        """This endpoint represents all validated transactions.

        `GET /transactions{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: The list of all transactions
        :rtype: dict

        """
        endpoint = '/transactions/'
        return self.query(endpoint, params, sse)

    def transaction(self, tx_hash):
        """The transaction details endpoint provides information on a single
        transaction.

        `GET /transactions/{hash}
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-single.html>`_

        :param str tx_hash: The hex-encoded transaction hash
        :return: A single transaction's details
        :rtype: dict

        """
        endpoint = '/transactions/{tx_hash}'.format(tx_hash=tx_hash)
        return self.query(endpoint)

    def transaction_operations(self, tx_hash, params=None):
        """This endpoint represents all operations that are part of a given
        transaction.

        `GET /transactions/{hash}/operations{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-transaction.html>`_

        :param str tx_hash: The hex-encoded transaction hash
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: A single transaction's operations
        :rtype: dict

        """
        endpoint = '/transactions/{tx_hash}/operations'.format(tx_hash=tx_hash)
        return self.query(endpoint, params)

    def transaction_effects(self, tx_hash, params=None):
        """This endpoint represents all effects that occurred as a result of a
        given transaction.

        `GET /transactions/{hash}/effects{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-transaction.html>`_

        :param str tx_hash: The hex-encoded transaction hash
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: A single transaction's effects
        :rtype: dict

        """
        endpoint = '/transactions/{tx_hash}/effects'.format(tx_hash=tx_hash)
        return self.query(endpoint, params)

    def transaction_payments(self, tx_hash, params=None):
        """This endpoint represents all payment operations that are part of a
        given transaction.

        `GET /transactions/{hash}/payments{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-transaction.html>`_

        :param str tx_hash: The hex-encoded transaction hash
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: A single transaction's payment operations
        :rtype: dict

        """
        endpoint = '/transactions/{tx_hash}/payments'.format(tx_hash=tx_hash)
        return self.query(endpoint, params)

    def order_book(self, params=None):
        """Return, for each orderbook, a summary of the orderbook and the bids
        and asks associated with that orderbook.

        See the external docs below for information on the arguments required.

        `GET /order_book
        <https://www.stellar.org/developers/horizon/reference/endpoints/orderbook-details.html>`_

        :param dict params: The query parameters to pass to this request.
        :return: A list of orderbook summaries as a JSON object.
        :rtype: dict

        """
        endpoint = '/order_book/'
        return self.query(endpoint, params)

    def ledgers(self, params=None, sse=False):
        """This endpoint represents all ledgers.

        `GET /ledgers{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: All ledgers on the network.
        :rtype: dict

        """
        endpoint = '/ledgers/'
        return self.query(endpoint, params, sse)

    def ledger(self, ledger_id):
        """The ledger details endpoint provides information on a single ledger.

        `GET /ledgers/{sequence}
        <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-single.html>`_

        :param int ledger_id: The id of the ledger to look up
        :return: The details of a single ledger
        :rtype: dict

        """
        endpoint = '/ledgers/{ledger_id}'.format(ledger_id=ledger_id)
        return self.query(endpoint)

    def ledger_effects(self, ledger_id, params=None):
        """This endpoint represents all effects that occurred in the given
        ledger.

        `GET /ledgers/{id}/effects{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-ledger.html>`_

        :param int ledger_id: The id of the ledger to look up
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: The effects for a single ledger
        :rtype: dict

        """
        endpoint = '/ledgers/{ledger_id}/effects'.format(ledger_id=ledger_id)
        return self.query(endpoint, params)

    def ledger_operations(self, ledger_id, params=None):
        """This endpoint returns all operations that occurred in a given
        ledger.

        `GET /ledgers/{id}/operations{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/operations-for-ledger.html>`_

        :param int ledger_id: The id of the ledger to look up
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: The operations contained in a single ledger
        :rtype: dict

        """
        endpoint = '/ledgers/{ledger_id}/operations'.format(
            ledger_id=ledger_id)
        return self.query(endpoint, params)

    def ledger_payments(self, ledger_id, params=None):
        """This endpoint represents all payment operations that are part of a
        valid transactions in a given ledger.

        `GET /ledgers/{id}/payments{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/payments-for-ledger.html>`_

        :param int ledger_id: The id of the ledger to look up
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: The payments contained in a single ledger
        :rtype: dict

        """
        endpoint = '/ledgers/{ledger_id}/payments'.format(ledger_id=ledger_id)
        return self.query(endpoint, params)

    def ledger_transactions(
            self,
            ledger_id,
            params=None,
    ):
        """This endpoint represents all transactions in a given ledger.

        `GET /ledgers/{id}/transactions{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-for-ledger.html>`_

        :param int ledger_id: The id of the ledger to look up.
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: The transactions contained in a single ledger
        :rtype: dict

        """
        endpoint = '/ledgers/{ledger_id}/transactions'.format(
            ledger_id=ledger_id)
        return self.query(endpoint, params)

    def effects(self, params=None, sse=False):
        """This endpoint represents all effects.

        `GET /effects{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: A list of all effects
        :rtype: dict

        """
        endpoint = '/effects/'
        return self.query(endpoint, params, sse)

    def operations(self, params=None, sse=False):
        """This endpoint represents all operations that are part of validated
        transactions.

        `GET /operations{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/operations-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: A list of all operations
        :rtype: dict

        """
        endpoint = '/operations/'
        return self.query(endpoint, params, sse)

    def operation(self, op_id, params=None):
        """The operation details endpoint provides information on a single
        operation.

        `GET /operations/{id}
        <https://www.stellar.org/developers/horizon/reference/endpoints/operations-single.html>`_

        :param id op_id: The operation ID to get details on.
        :return: Details on a single operation
        :rtype: dict
        """
        endpoint = '/operations/{op_id}'.format(op_id=op_id)
        return self.query(endpoint, params)

    def operation_effects(self, op_id, params=None):
        """This endpoint represents all effects that occurred as a result of a
        given operation.

        `GET /operations/{id}/effects{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/effects-for-operation.html>`_

        :param int op_id: The operation ID to get effects on.
        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: A list of effects on the given operation
        :rtype: dict

        """
        endpoint = '/operations/{op_id}/effects'.format(op_id=op_id)
        return self.query(endpoint, params)

    def payments(self, params=None, sse=False):
        """This endpoint represents all payment operations that are part of
        validated transactions.

        `GET /payments{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/payments-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: A list of all valid payment operations
        :rtype: dict

        """
        endpoint = '/payments/'
        return self.query(endpoint, params, sse)

    def paths(self, params=None):
        """Load a list of assets available to the source account id and find
        any payment paths from those source assets to the desired
        destination asset.

        See the below docs for more information on required and optional
        parameters for further specifying your search.

        `GET /paths
        <https://www.stellar.org/developers/horizon/reference/endpoints/path-finding.html>`_

        :param dict params: The query parameters to pass to this request, such
            as source_account, destination_account, destination_asset_type,
            etc.
        :return: A list of paths that can be used to complete a payment based
            on a given query.
        :rtype: dict

        """
        endpoint = '/paths'
        return self.query(endpoint, params)

    def trades(self, params=None):
        """Load a list of trades, optionally filtered by an orderbook.

        See the below docs for more information on required and optional
        parameters for further specifying your search.

        `GET /trades
        <https://www.stellar.org/developers/horizon/reference/endpoints/trades.html>`_

        :param dict params: The query parameters to pass to this request, such
            as base_asset_type, counter_asset_type, cursor, order, limit, etc.
        :return: A list of trades filtered by a given query
        :rtype: dict

        """
        endpoint = '/trades/'
        return self.query(endpoint, params)

    def trade_aggregations(self, params=None):
        """Load a list of aggregated historical trade data, optionally filtered
        by an orderbook.

        `GET /trade_aggregations
        <https://www.stellar.org/developers/horizon/reference/endpoints/trade_aggregations.html>`_

        :param dict params: The query parameters to pass to this request, such
            as start_time, end_time, base_asset_type, counter_asset_type,
            order, limit, etc.
        :return: A list of collected trade aggregations
        :rtype: dict

        """
        endpoint = '/trade_aggregations/'
        return self.query(endpoint, params)


def check_horizon_reply(reply):
    if 'status' not in reply:
        return reply
    raise HorizonError(reply)


def horizon_testnet():
    """Create a Horizon instance utilizing SDF's Test Network."""
    return Horizon(HORIZON_TEST)


def horizon_livenet():
    """Create a Horizon instance utilizing SDF's Live Network."""
    return Horizon(HORIZON_LIVE)
