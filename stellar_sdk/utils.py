import hashlib
from decimal import Decimal, ROUND_FLOOR
from typing import List

from .asset import Asset
from .exceptions import NoApproximationError, TypeError


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
            assets_string.append("{}:{}".format(asset.code, asset.issuer))
    return ",".join(assets_string)
