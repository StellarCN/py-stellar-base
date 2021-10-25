import hashlib
import os
import re
from decimal import ROUND_FLOOR, Decimal
from typing import Dict, List, Optional, Union
from urllib.parse import urlsplit, urlunsplit

from .asset import Asset
from .exceptions import Ed25519PublicKeyInvalidError, NoApproximationError, ValueError
from .strkey import StrKey
from .type_checked import type_checked

MUXED_ACCOUNT_STARTING_LETTER: str = "M"
ED25519_PUBLIC_KEY_STARTING_LETTER: str = "G"
_LOWER_LIMIT = "0"
_UPPER_LIMIT = "922337203685.4775807"
_EXPONENT = 7


@type_checked
def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


@type_checked
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


@type_checked
def hex_to_bytes(hex_string: Union[str, bytes]) -> bytes:
    if isinstance(hex_string, str):
        return bytes.fromhex(hex_string)
    return hex_string


@type_checked
def convert_assets_to_horizon_param(assets: List[Asset]) -> str:
    assets_string = []
    for asset in assets:
        if asset.is_native():
            assets_string.append(asset.type)
        else:
            assets_string.append(f"{asset.code}:{asset.issuer}")
    return ",".join(assets_string)


@type_checked
def urljoin_with_query(base: str, path: Optional[str]) -> str:
    split_url = urlsplit(base)
    query = split_url.query
    real_path = split_url.path
    if path:
        real_path = os.path.join(split_url.path, path)
    url = urlunsplit(
        (split_url.scheme, split_url.netloc, real_path, query, split_url.fragment)
    )
    return url


@type_checked
def is_valid_hash(data: str) -> bool:
    if not data:
        return False
    asset_code_re = re.compile(r"^[a-zA-Z0-9]{64}$")
    return bool(asset_code_re.match(data))


@type_checked
def raise_if_not_valid_ed25519_public_key(value: str, argument_name: str) -> None:
    try:
        StrKey.decode_ed25519_public_key(value)
    except Exception as e:
        raise Ed25519PublicKeyInvalidError(
            f'Value of argument "{argument_name}" is not a valid ed25519 public key: {value}'
        ) from e


@type_checked
def raise_if_not_valid_amount(value: str, argument_name: str) -> None:
    amount = Decimal(value)
    if abs(amount.as_tuple().exponent) > _EXPONENT:
        raise ValueError(
            f'Value of argument "{argument_name}" must have at most 7 digits after the decimal: {amount}'
        )
    if amount < Decimal(_LOWER_LIMIT) or amount > Decimal(_UPPER_LIMIT):
        raise ValueError(
            f'Value of argument "{argument_name}" must represent a positive number '
            f"and the max valid value is {_UPPER_LIMIT}: {amount}"
        )


@type_checked
def raise_if_not_valid_hash(value: str, argument_name: str) -> None:
    if not is_valid_hash(value):
        raise ValueError(
            f'Value of argument "{argument_name}" is not a valid hash: {value}'
        )


@type_checked
def raise_if_not_valid_balance_id(value: str, argument_name: str) -> None:
    if len(value) != 72 or value[:8] != "00000000" or not is_valid_hash(value[8:]):
        raise ValueError(
            f'Value of argument "{argument_name}" is not a valid balance id: {value}'
        )
