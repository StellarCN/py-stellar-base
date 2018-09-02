# coding: utf-8

import requests

try:
    from sseclient import SSEClient
except ImportError:
    SSEClient = None
try:
    # Python 3
    from urllib.parse import urlencode
except ImportError:
    # Python 2
    from urllib import urlencode

from .exceptions import HorizonError

HORIZON_LIVE = "https://horizon.stellar.org"
HORIZON_TEST = "https://horizon-testnet.stellar.org"


class Horizon(object):
    def __init__(self, horizon=None, sse=False, timeout=20):
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

        :param str horizon: The horizon base URL
        :param bool sse: Default to using server side events for streaming
            responses when available.
        :param int timeout: The timeout for all requests.

        """
        if sse and SSEClient is None:
            raise ValueError('SSE not supported, missing sseclient module')

        if horizon is None:
            self.horizon = HORIZON_TEST
        else:
            self.horizon = horizon

        self.session = requests.Session()
        self.sse = sse
        self.timeout = timeout

    def _request(self, verb, endpoint, **kwargs):
        url = '{base}{endpoint}'.format(base=self.horizon, endpoint=endpoint)
        if kwargs.get('sse', False):
            if 'params' in kwargs and kwargs['params']:
                url = '{}?{}'.format(url, urlencode(kwargs['params']))
            messages = SSEClient(url)
            return messages
        else:
            kwargs.pop('sse', None)
            try:
                # FIXME: We should really consider raising the HTTPError when
                # it happens and wrapping its JSON response in a HorizonError
                resp = self.session.request(
                    verb, url, timeout=self.timeout, **kwargs)
                return resp.json()
            except requests.RequestException:
                raise HorizonError(
                    'Could not successfully make a request to Horizon.')

    def _get(self, endpoint, **kwargs):
        # If sse has been passed in by an endpoint (meaning it supports sse)
        # but it hasn't been explicitly been set by the request, default to the
        # this instance's setting on SSE requests.
        if 'sse' in kwargs and kwargs['sse'] is None:
            kwargs['sse'] = self.sse
        return self._request('GET', endpoint, **kwargs)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def submit(self, te, **kwargs):
        """Submit a transaction to Horizon.

        `POST /transactions
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-create.html>`_

        Uses form-encoded data to send over to Horizon.

        :param bytes te: The transaction envelope to submit
        :return: The JSON response indicating the success/failure of the
            submitted transaction.
        :rtype: dict

        """
        payload = {'tx': te}
        return self._post('/transactions', data=payload, **kwargs)

    def account(self, address, **kwargs):
        """Returns information and links relating to a single account.

        `GET /accounts/{account}
        <https://www.stellar.org/developers/horizon/reference/endpoints/accounts-single.html>`_

        :param str address: The account ID to retrieve details about
        :return: The account details in a JSON response
        :rtype: dict

        """

        endpoint = '/accounts/{account_id}'.format(account_id=address)
        return self._get(endpoint, **kwargs)

    def account_data(self, account_id, data_key, **kwargs):
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
        return self._get(endpoint, **kwargs)

    def account_effects(self, address, params=None, sse=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def account_offers(self, address, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def account_operations(self, address, params=None, sse=None, **kwargs):
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
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def account_transactions(self, address, params=None, sse=None, **kwargs):
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
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def account_payments(self, address, params=None, sse=None, **kwargs):
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
        endpoint = '/accounts/{account_id}/payments'.format(
            account_id=address)
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def assets(self, params=None, **kwargs):
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
        endpoint = '/assets'
        return self._get(endpoint, params=params, **kwargs)

    def transactions(self, params=None, sse=None, **kwargs):
        """This endpoint represents all validated transactions.

        `GET /transactions{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: The list of all transactions
        :rtype: dict

        """
        endpoint = '/transactions'
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def transaction(self, tx_hash, **kwargs):
        """The transaction details endpoint provides information on a single
        transaction.

        `GET /transactions/{hash}
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-single.html>`_

        :param str tx_hash: The hex-encoded transaction hash
        :return: A single transaction's details
        :rtype: dict

        """
        endpoint = '/transactions/{tx_hash}'.format(tx_hash=tx_hash)
        return self._get(endpoint, **kwargs)

    def transaction_operations(self, tx_hash, params=None, **kwargs):
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
        endpoint = '/transactions/{tx_hash}/operations'.format(
            tx_hash=tx_hash)
        return self._get(endpoint, params=params, **kwargs)

    def transaction_effects(self, tx_hash, params=None, **kwargs):
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
        endpoint = '/transactions/{tx_hash}/effects'.format(
            tx_hash=tx_hash)
        return self._get(endpoint, params=params, **kwargs)

    def transaction_payments(self, tx_hash, params=None, **kwargs):
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
        endpoint = '/transactions/{tx_hash}/payments'.format(
            tx_hash=tx_hash)
        return self._get(endpoint, params=params, **kwargs)

    def order_book(self, params=None, **kwargs):
        """Return, for each orderbook, a summary of the orderbook and the bids
        and asks associated with that orderbook.

        See the external docs below for information on the arguments required.

        `GET /order_book
        <https://www.stellar.org/developers/horizon/reference/endpoints/orderbook-details.html>`_

        :param dict params: The query parameters to pass to this request.
        :return: A list of orderbook summaries as a JSON object.
        :rtype: dict

        """
        endpoint = '/order_book'
        return self._get(endpoint, params=params, **kwargs)

    def ledgers(self, params=None, sse=None, **kwargs):
        """This endpoint represents all ledgers.

        `GET /ledgers{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :return: All ledgers on the network.
        :rtype: dict

        """
        endpoint = '/ledgers'
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def ledger(self, ledger_id, **kwargs):
        """The ledger details endpoint provides information on a single ledger.

        `GET /ledgers/{sequence}
        <https://www.stellar.org/developers/horizon/reference/endpoints/ledgers-single.html>`_

        :param int ledger_id: The id of the ledger to look up
        :return: The details of a single ledger
        :rtype: dict

        """
        endpoint = '/ledgers/{ledger_id}'.format(ledger_id=ledger_id)
        return self._get(endpoint, **kwargs)

    def ledger_effects(self, ledger_id, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def ledger_operations(self, ledger_id, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def ledger_payments(self, ledger_id, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def ledger_transactions(self, ledger_id, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def effects(self, params=None, sse=None, **kwargs):
        """This endpoint represents all effects.

        `GET /effects{?cursor,limit,order}
        <https://www.stellar.org/developers/horizon/reference/endpoints/effects-all.html>`_

        :param dict params: The query parameters to pass to this request, such
            as cursor, order, and limit.
        :param bool sse: Use server side events for streaming responses
        :return: A list of all effects
        :rtype: dict

        """
        endpoint = '/effects'
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def operations(self, params=None, sse=None, **kwargs):
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
        endpoint = '/operations'
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def operation(self, op_id, **kwargs):
        """The operation details endpoint provides information on a single
        operation.

        `GET /operations/{id}
        <https://www.stellar.org/developers/horizon/reference/endpoints/operations-single.html>`_

        :param id op_id: The operation ID to get details on.
        :return: Details on a single operation
        :rtype: dict
        """
        endpoint = '/operations/{op_id}'.format(op_id=op_id)
        return self._get(endpoint, **kwargs)

    def operation_effects(self, op_id, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def payments(self, params=None, sse=None, **kwargs):
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
        endpoint = '/payments'
        return self._get(endpoint, params=params, sse=sse, **kwargs)

    def paths(self, params=None, **kwargs):
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
        return self._get(endpoint, params=params, **kwargs)

    def trades(self, params=None, **kwargs):
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
        endpoint = '/trades'
        return self._get(endpoint, params=params, **kwargs)

    def trade_aggregations(self, params=None, **kwargs):
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
        endpoint = '/trade_aggregations'
        return self._get(endpoint, params=params, **kwargs)


def horizon_testnet():
    """Create a Horizon instance utilizing SDF's Test Network."""
    return Horizon(HORIZON_TEST)


def horizon_livenet():
    """Create a Horizon instance utilizing SDF's Live Network."""
    return Horizon(HORIZON_LIVE)
