from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter, DEFAULT_POOLSIZE
from requests.exceptions import RequestException

from urllib3.exceptions import NewConnectionError
from urllib3.util import Retry

from .response.root import Root
from .response.account import Account
from . import __version__

import logging

logger = logging.getLogger(__name__)

try:
    from sseclient import SSEClient
except ImportError:
    SSEClient = None

HORIZON_PUBLIC = "https://horizon.stellar.org"
HORIZON_TESTNET = "https://horizon-testnet.stellar.org"
DEFAULT_REQUEST_TIMEOUT = 11  # two ledgers + 1 sec, let's retry faster and not wait 60 secs.
DEFAULT_NUM_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 0.5
USER_AGENT = {
    'X-Client-Name': 'py-stellar-sdk',
    'X-Client-Version': __version__
}


class Horizon(object):
    def __init__(self,
                 horizon_uri=HORIZON_TESTNET,
                 pool_size=DEFAULT_POOLSIZE,
                 num_retries=DEFAULT_NUM_RETRIES,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT,
                 backoff_factor=DEFAULT_BACKOFF_FACTOR,
                 user_agent=None):
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
        :param int request_timeout: The timeout for all requests.
        :param int pool_size: persistent connection to Horizon and connection pool
        :param int num_retries: configurable request retry functionality
        :param float backoff_factor: a backoff factor to apply between attempts after the second try
        :param dict user_agent: representing the user-agent you want,
            such as `{'X-Client-Name': 'py-stellar-base', 'X-Client-Version': __version__}`

        """

        if user_agent is None:
            user_agent = USER_AGENT
        self.horizon_uri = horizon_uri
        self.pool_size = pool_size
        self.num_retries = num_retries
        self.request_timeout = request_timeout
        self.backoff_factor = backoff_factor
        self.user_agent = user_agent

        # adding 504 to the tuple of statuses to retry
        self.status_forcelist = tuple(Retry.RETRY_AFTER_STATUS_CODES) + (504,)

        # configure standard session

        # configure retry handler
        retry = Retry(
            total=self.num_retries,
            backoff_factor=self.backoff_factor,
            redirect=0,
            status_forcelist=self.status_forcelist,
            raise_on_status=False)
        # init transport adapter
        adapter = HTTPAdapter(
            pool_connections=self.pool_size,
            pool_maxsize=self.pool_size,
            max_retries=retry)

        # init session
        session = requests.Session()

        # set default headers
        session.headers.update(self.user_agent)

        session.mount('http://', adapter)
        session.mount('https://', adapter)
        self._session = session

    def submit(self, te):
        """Submit the transaction using a pooled connection

        `POST /transactions
        <https://www.stellar.org/developers/horizon/reference/endpoints/transactions-create.html>`_

        Uses form-encoded data to send over to Horizon.

        :return: The JSON response indicating the success/failure of the
            submitted transaction.
        :rtype: dict

        """
        params = {'tx': te}
        url = urljoin(self.horizon_uri, 'transactions/')

        reply = self._session.post(
            url, data=params, timeout=self.request_timeout)
        return reply.json()

    def query(self, rel_url, params=None):
        abs_url = urljoin(self.horizon_uri, rel_url)
        reply = self._query(abs_url, params)
        return reply

    def _query(self, url, params=None):
        reply = None
        try:
            reply = self._session.get(
                url, params=params, timeout=self.request_timeout)
            return reply.json()
        except (RequestException, NewConnectionError, ValueError) as e:
            if reply is not None:
                pass  # TODO
            else:
                pass

    def root(self):
        endpoint = '/'
        resp = self.query(endpoint)
        return Root(resp)

    def account(self, address):
        endpoint = '/accounts/{account_id}'.format(account_id=address)
        resp = self.query(endpoint)
        return Account(resp)
