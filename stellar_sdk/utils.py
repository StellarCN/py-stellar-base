import hashlib
import os
from decimal import Decimal, ROUND_FLOOR
from typing import List
from urllib.parse import urlsplit, urlunsplit

from . import xdr as stellar_xdr
from .asset import Asset
from .exceptions import NoApproximationError, TypeError
from .strkey import StrKey

MUXED_ACCOUNT_STARTING_LETTER: str = "M"
ED25519_PUBLIC_KEY_STARTING_LETTER: str = "G"


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def best_rational_approximation(x):
    x = Decimal(x)
    int32_max = Decimal(2147483647)
    fractions = [[Decimal(0), Decimal(1)], [Decimal(1), Decimal(0)]]
    i = 2
    while True:
        if x > int32_max:
            break
        a = x.to_integral_exact(rounding=ROUND_FLOOR)
        f = x - a
        h = a * fractions[i - 1][0] + fractions[i - 2][0]
        k = a * fractions[i - 1][1] + fractions[i - 2][1]
        if h > int32_max or k > int32_max:
            break
        fractions.append([h, k])
        if f.is_zero():
            break
        x = 1 / f
        i = i + 1
    n = fractions[len(fractions) - 1][0]
    d = fractions[len(fractions) - 1][1]
    if n.is_zero() or d.is_zero():
        raise NoApproximationError("Couldn't find approximation.")
    return {"n": int(n), "d": int(d)}


def hex_to_bytes(hex_string):
    if isinstance(hex_string, bytes):
        return hex_string
    if isinstance(hex_string, str):
        return bytes.fromhex(hex_string)
    raise TypeError("`hex_string` should be a 32 byte hash or hex encoded string.")


def convert_assets_to_horizon_param(assets: List[Asset]) -> str:
    assets_string = []
    for asset in assets:
        if asset.is_native():
            assets_string.append(asset.type)
        else:
            assets_string.append(f"{asset.code}:{asset.issuer}")
    return ",".join(assets_string)


def urljoin_with_query(base: str, path: str) -> str:
    split_url = urlsplit(base)
    query = split_url.query
    real_path = split_url.path
    if path:
        real_path = os.path.join(split_url.path, path)
    url = urlunsplit(
        (split_url.scheme, split_url.netloc, real_path, query, split_url.fragment)
    )
    return url


def parse_ed25519_account_id_from_muxed_account_xdr_object(
    data: stellar_xdr.MuxedAccount,
) -> str:
    if data.ed25519 is not None:
        return StrKey.encode_ed25519_public_key(data.ed25519.uint256)
    assert data.med25519 is not None
    return StrKey.encode_ed25519_public_key(data.med25519.ed25519.uint256)


def is_fee_bump_transaction(xdr: str) -> bool:
    xdr_object = stellar_xdr.TransactionEnvelope.from_xdr(xdr)
    te_type = xdr_object.type
    if te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_FEE_BUMP:
        return True
    elif (
        te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX
        or te_type == stellar_xdr.EnvelopeType.ENVELOPE_TYPE_TX_V0
    ):
        return False
    else:
        raise ValueError(
            f"This transaction envelope type is not supported, type = {te_type}."
        )
