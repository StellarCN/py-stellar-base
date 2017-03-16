# coding: utf-8

import requests
import toml

def federation(fed_address, fed_type='name'):
    if '*' not in fed_address:
        raise FederationError('not a valid federation address')

    param, domain = fed_address.rsplit('*',1)
    if param == ''  or domain == '':
        raise FederationError('not a valid federation address')

    if '.' not in domain:
        raise FederationError('not a valid domain name')

    fed_service = get_federation_service(domain)
    if not fed_service:
        raise FederationError('not a valid federation server')

    return get_federation_info(fed_address, fed_service, fed_type)

def get_federation_info(fed_address, federation_service, fed_type='name'):
    params = {'q':fed_address, 'type':fed_type }
    r = requests.get(federation_service,params=params)
    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_federation_service(domain):
    st = get_stellar_toml(domain)
    if not st:
        return None
    return st.get('FEDERATION_SERVER')

def get_auth_server(domain):
    st = get_stellar_toml(domain)
    if not st:
        return None
    return st.get('AUTH_SERVER')

def get_stellar_toml(domain):
    toml_link = '/.well-known/stellar.toml'
    protocol = 'https://'
    url_list = ['' , 'www.', 'stellar.']
    url_list = [ protocol + url + domain + toml_link for url in url_list ]

    for url in url_list:
        r = requests.get(url)
        if r.status_code == 200:
            return toml.loads(r.text) 
    
    return None 
        

class FederationError(Exception):
    pass
