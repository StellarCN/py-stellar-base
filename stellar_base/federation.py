# coding: utf-8

import requests
import toml

from .exceptions import FederationError, DecodeError
from .keypair import Keypair


def federation(address_or_id, fed_type='name', domain=None, allow_http=False):
    """Send a federation query to a Stellar Federation service.

    For more info, see the `complete guide on Stellar Federation.
    <https://www.stellar.org/developers/guides/concepts/federation.html>`_.

    :param str address_or_id: The address which you expect te retrieve
        federation information about.
    :param str fed_type: The type of federation query that you are making. Must
        be 'name', 'id', 'forward', or 'txid'.
    :param str domain: The domain that corresponds to the address or ID;
        this is where the stellar.toml file lives (which ultimately points to
        the URL of the federation service).
    :param bool allow_http: Whether to allow for requests over plain HTTP over
        HTTPS. Note - you should *always* use HTTPS outside of testing.
    :return dict: The federation query response decoded from JSON as a dict.

    """
    if fed_type == 'name':
        if '*' not in address_or_id:
            raise FederationError('not a valid federation address')

        param, domain = address_or_id.rsplit('*', 1)
        if param == '' or domain == '':
            raise FederationError('not a valid federation address')
    elif fed_type == 'id':
        try:
            Keypair.from_address(address_or_id)
        except DecodeError:
            raise FederationError('not a valid account id')
    else:
        raise FederationError('not a valid fed_type')

    if '.' not in domain:
        raise FederationError('not a valid domain name')
    fed_service = get_federation_service(domain, allow_http)
    if not fed_service:
        raise FederationError('not a valid federation server')

    return _get_federation_info(address_or_id, fed_service, fed_type)


def _get_federation_info(address_or_id, federation_service, fed_type='name'):
    """Send a federation query to a Stellar Federation service.

    Note: The preferred method of making this call is via
    :function:`federation`, as it handles error checking and parsing of
    arguments.

    :param str address_or_id: The address which you expect te retrieve
        federation information about.
    :param str federation_service: The url of the federation service you're
        requesting information from.
    :param str fed_type: The type of federation query that you are making. Must
        be 'name', 'id', 'forward', or 'txid'.
    :return dict: The federation query response decoded from JSON as a dict.

    """
    params = {'q': address_or_id, 'type': fed_type}
    r = requests.get(federation_service, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_federation_service(domain, allow_http=False):
    """Retrieve the FEDERATION_SERVER config from a domain's stellar.toml.

    :param str domain: The domain the .toml file is hosted at.
    :param bool allow_http: Specifies whether the request should go over plain
        HTTP vs HTTPS. Note it is recommend that you *always* use HTTPS.
    :return str: The FEDERATION_SERVER url.

    """
    st = get_stellar_toml(domain, allow_http)
    if not st:
        return None
    return st.get('FEDERATION_SERVER')


def get_auth_server(domain, allow_http=False):
    """Retrieve the AUTH_SERVER config from a domain's stellar.toml.

    :param str domain: The domain the .toml file is hosted at.
    :param bool allow_http: Specifies whether the request should go over plain
        HTTP vs HTTPS. Note it is recommend that you *always* use HTTPS.
    :return str: The AUTH_SERVER url.

    """
    st = get_stellar_toml(domain, allow_http)
    if not st:
        return None
    return st.get('AUTH_SERVER')


def get_stellar_toml(domain, allow_http=False):
    """Retrieve the stellar.toml file from a given domain.

    Retrieve the stellar.toml file for information about interacting with
    Stellar's federation protocol for a given Stellar Anchor (specified by a
    domain).

    :param str domain: The domain the .toml file is hosted at.
    :param bool allow_http: Specifies whether the request should go over plain
        HTTP vs HTTPS. Note it is recommend that you *always* use HTTPS.
        :return: The stellar.toml file as a an object via :func:`toml.loads`.

    """
    toml_link = '/.well-known/stellar.toml'
    if allow_http:
        protocol = 'http://'
    else:
        protocol = 'https://'
    url_list = ['', 'www.', 'stellar.']
    url_list = [protocol + url + domain + toml_link for url in url_list]

    for url in url_list:
        r = requests.get(url)
        if r.status_code == 200:
            return toml.loads(r.text)

    return None

