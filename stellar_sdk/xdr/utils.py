from decimal import Decimal, Context, Inexact
from typing import Union

_ONE = Decimal(10 ** 7)


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
    <https://www.stellar.org/developers/guides/concepts/assets.html#amount-precision-and-representation>`_
    for more information.

    :param value: The amount to convert to an integer for XDR
        serialization.

    """
    if not (isinstance(value, str) or isinstance(value, Decimal)):
        raise TypeError(
            f"Value of type '{value}' must be of type {str} or {Decimal}, but got {type(value)}."
        )
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
    """Converts an str amount from an XDR amount object

    :param value: The amount to convert to a string from an XDR int64
        amount.

    """
    return str(Decimal(value) / _ONE)
