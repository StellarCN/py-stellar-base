from decimal import Decimal
from typing import Optional, Union

from ..asset import Asset
from ..exceptions import ValueError, TypeError
from ..keypair import Keypair
from ..price import Price

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
        raise TypeError(f"price should be type of {str}, {Decimal} or {Price}.")

    if isinstance(price, str) or isinstance(price, Decimal):
        check_amount(price)


def check_amount(amount: Union[str, Decimal]) -> None:
    if not (isinstance(amount, str) or isinstance(amount, Decimal)):
        raise TypeError(f"amount should be type of {str} or {Decimal}.")
    amount = Decimal(amount)
    if abs(amount.as_tuple().exponent) > _EXPONENT:
        raise ValueError(
            f"Value of '{amount}' must have at most 7 digits after the decimal."
        )
    if amount < Decimal(_LOWER_LIMIT) or amount > Decimal(_UPPER_LIMIT):
        raise ValueError(
            f"Value of '{amount}' must represent a positive number "
            f"and the max valid value is {_UPPER_LIMIT}."
        )
