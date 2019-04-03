# coding: utf-8
# SEP 0010: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md

import requests

from stellar_base import Keypair
from stellar_base.exceptions import BadSignatureError, WebAuthenticationError
from stellar_base.sep.utils import get_stellar_toml
from stellar_base.transaction_envelope import TransactionEnvelope


def get_jwt(domain, account, allow_http=False):
    """SEP: 0010 Stellar Web Authentication

    https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md

    :param str domain: The domain the .toml file is hosted at.
    :param Keypair account: Account used for authentication.
    :param bool allow_http: Specifies whether the request should go over plain
        HTTP vs HTTPS. Note it is recommend that you *always* use HTTPS.

    """
    st = get_stellar_toml(domain, allow_http)
    web_auth_endpoint = st.get('WEB_AUTH_ENDPOINT')
    web_auth_account = st.get('WEB_AUTH_ACCOUNT')
    if web_auth_account is None:
        raise WebAuthenticationError("WEB_AUTH_ACCOUNT not found.")
    if web_auth_endpoint is None:
        raise WebAuthenticationError("WEB_AUTH_ENDPOINT not found.")

    server_keypair = Keypair.from_address(web_auth_account)

    xdr_resp = requests.get(web_auth_endpoint, params={'public_key': account.address().decode()})

    xdr = xdr_resp.json().get('transaction')
    transaction_envelope = TransactionEnvelope.from_xdr(xdr)
    hash = transaction_envelope.hash_meta()
    signatures = transaction_envelope.signatures

    valid = False
    for signature in signatures:
        try:
            server_keypair.verify(hash, signature.signature)
            valid = True
            break
        except BadSignatureError:
            pass

    if not valid:
        raise WebAuthenticationError("Server signature not found.")

    transaction_envelope.sign(account)
    signed_xdr = transaction_envelope.xdr().decode()
    jwt_resp = requests.post(web_auth_endpoint, data={'transaction': signed_xdr})
    if jwt_resp.status_code != 200:
        raise WebAuthenticationError(jwt_resp.json().get('error'))
    return jwt_resp.json().get('token')
