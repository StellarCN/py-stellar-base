# coding: utf-8
import requests
import toml


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
