# coding: utf-8

import requests
import toml

from .keypair import Keypair
from .utils import DecodeError


def federation(address_or_id, fed_type='name', domain=None, allow_http=False):
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

    return get_federation_info(address_or_id, fed_service, fed_type)


def get_federation_info(address_or_id, federation_service, fed_type='name'):
    params = {'q': address_or_id, 'type': fed_type}
    r = requests.get(federation_service, params=params)
    if r.status_code == 200:
        return r.json()
    else:
        return None


def get_federation_service(domain, allow_http=False):
    st = get_stellar_toml(domain, allow_http)
    if not st:
        return None
    return st.get('FEDERATION_SERVER')


def get_auth_server(domain, allow_http=False):
    st = get_stellar_toml(domain, allow_http)
    if not st:
        return None
    return st.get('AUTH_SERVER')


def get_stellar_toml(domain, allow_http=False):
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


class FederationError(Exception):
    pass
