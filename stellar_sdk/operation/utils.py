from decimal import Decimal
from typing import Optional, Union

from ..keypair import Keypair
from ..price import Price
from ..asset import Asset
from ..exceptions import ValueError, TypeError

_LOWER_LIMIT = "0"
_UPPER_LIMIT = "922337203685.4775807"
_EXPONENT = 7


def check_source(source: Optional[str]) -> None:
    if source is not None:
        check_ed25519_public_key(source)


def check_ed25519_public_key(public_key: str) -> None:
    Keypair.from_public_key(public_key)


def check_asset_code(asset_code: str) -> None:
    Asset.check_if_asset_code_is_valid(asset_code)


def check_price(price: Union[str, Decimal, Price]) -> None:
    if not (
        isinstance(price, str) or isinstance(price, Decimal) or isinstance(price, Price)
    ):
        raise TypeError(
            "amount should be type of {}, {} or {}.".format(str, Decimal, Price)
        )

    if isinstance(price, str) or isinstance(price, Decimal):
        check_amount(price)


def check_amount(amount: Union[str, Decimal]) -> None:
    if not (isinstance(amount, str) or isinstance(amount, Decimal)):
        raise TypeError("amount should be type of {} or {}.".format(str, Decimal))
    amount = Decimal(amount)
    if abs(amount.as_tuple().exponent) > _EXPONENT:
        raise ValueError(
            "Value of '{}' must have at most 7 digits after the decimal.".format(amount)
        )
    if amount < Decimal(_LOWER_LIMIT) or amount > Decimal(_UPPER_LIMIT):
        raise ValueError(
            "Value of '{}' must represent a positive number "
            "and the max valid value is {}.".format(amount, _UPPER_LIMIT)
        )
