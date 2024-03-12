"""This file contains constants, functions and classes used internally by this SDK.
They may change at any time, so please do not use them directly.
"""

import hashlib
import re
from decimal import ROUND_FLOOR, Context, Decimal, Inexact
from typing import TYPE_CHECKING, Dict, Optional, Sequence, Union
from urllib.parse import urljoin, urlsplit, urlunsplit

from .exceptions import Ed25519PublicKeyInvalidError, NoApproximationError
from .strkey import StrKey

if TYPE_CHECKING:
    from .asset import Asset

MUXED_ACCOUNT_STARTING_LETTER: str = "M"
ED25519_PUBLIC_KEY_STARTING_LETTER: str = "G"
_LOWER_LIMIT = "0"
_UPPER_LIMIT = "922337203685.4775807"
_EXPONENT = 7
_ONE = Decimal(10**7)


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def best_rational_approximation(x) -> Dict[str, int]:
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


def hex_to_bytes(hex_string: Union[str, bytes]) -> bytes:
    if isinstance(hex_string, str):
        return bytes.fromhex(hex_string)
    return hex_string


def convert_assets_to_horizon_param(assets: Sequence["Asset"]) -> str:
    assets_string = []
    for asset in assets:
        if asset.is_native():
            assets_string.append(asset.type)
        else:
            assets_string.append(f"{asset.code}:{asset.issuer}")
    return ",".join(assets_string)


def urljoin_with_query(base: str, path: Optional[str]) -> str:
    split_url = urlsplit(base)
    query = split_url.query
    real_path = split_url.path
    if path:
        if not real_path.endswith("/"):
            real_path += "/"
        real_path = urljoin(real_path, path)
    url = urlunsplit(
        (split_url.scheme, split_url.netloc, real_path, query, split_url.fragment)
    )
    return url


def is_valid_hash(data: str) -> bool:
    if not data:
        return False
    asset_code_re = re.compile(r"^[a-zA-Z0-9]{64}$")
    return bool(asset_code_re.match(data))


def raise_if_not_valid_ed25519_public_key(value: str, argument_name: str) -> None:
    try:
        StrKey.decode_ed25519_public_key(value)
    except Exception as e:
        raise Ed25519PublicKeyInvalidError(
            f'Value of argument "{argument_name}" is not a valid ed25519 public key: {value}'
        ) from e


def raise_if_not_valid_amount(value: str, argument_name: str) -> None:
    amount = Decimal(value)
    exponent = amount.as_tuple().exponent
    if not isinstance(exponent, int) or abs(exponent) > _EXPONENT:
        raise ValueError(
            f'Value of argument "{argument_name}" must have at most 7 digits after the decimal: {amount}'
        )
    if amount < Decimal(_LOWER_LIMIT) or amount > Decimal(_UPPER_LIMIT):
        raise ValueError(
            f'Value of argument "{argument_name}" must represent a positive number '
            f"and the max valid value is {_UPPER_LIMIT}: {amount}"
        )


def raise_if_not_valid_hash(value: str, argument_name: str) -> None:
    if not is_valid_hash(value):
        raise ValueError(
            f'Value of argument "{argument_name}" is not a valid hash: {value}'
        )


def raise_if_not_valid_balance_id(value: str, argument_name: str) -> None:
    if len(value) != 72 or value[:8] != "00000000" or not is_valid_hash(value[8:]):
        raise ValueError(
            f'Value of argument "{argument_name}" is not a valid balance id: {value}'
        )


def to_xdr_amount(value: Union[str, Decimal]) -> int:
    """Converts an amount to the appropriate value to send over the network
    as a part of an XDR object.

    Each asset amount is encoded as a signed 64-bit integer in the XDR
    structures. An asset amount unit (that which is seen by end users) is
    scaled down by a factor of ten million (10,000,000) to arrive at the
    native 64-bit integer representation. For example, the integer amount
    value 25,123,456 equals 2.5123456 units of the asset. This scaling
    allows for seven decimal places of precision in human-friendly amount
    units.

    This static method correctly multiplies the value by the scaling factor
    in order to come to the integer value used in XDR structures.

    See `Stellar's documentation on Asset Precision
    <https://developers.stellar.org/docs/issuing-assets/anatomy-of-an-asset/#amount-precision>`_
    for more information.

    :param value: The amount to convert to an integer for XDR
        serialization.

    """
    # throw exception if value * ONE has decimal places (it can't be represented as int64)
    try:
        amount = int(
            (Decimal(value) * _ONE).to_integral_exact(context=Context(traps=[Inexact]))
        )
    except Inexact:
        raise ValueError(
            f"Value of '{value}' must have at most 7 digits after the decimal."
        )

    if amount < 0 or amount > 9223372036854775807:
        raise ValueError(
            f"Value of '{value}' must represent a positive number "
            "and the max valid value is 922337203685.4775807."
        )

    return amount


def from_xdr_amount(value: int) -> str:
    """Converts a str amount from an XDR amount object

    :param value: The amount to convert to a string from an XDR int64
        amount.

    """
    return str(Decimal(value) / _ONE)
