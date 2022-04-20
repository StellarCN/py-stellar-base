import os
from typing import Callable, overload

from typeguard import T_CallableOrType
from typeguard import typechecked as _typechecked

_STELLAR_SDK_RUNTIME_TYPE_CHECKING_FLAG: str = "STELLAR_SDK_RUNTIME_TYPE_CHECKING"
_STELLAR_SDK_RUNTIME_TYPE_CHECKING: bool = os.getenv(
    _STELLAR_SDK_RUNTIME_TYPE_CHECKING_FLAG, "True"
).lower() in ("true", "1", "t")


@overload
def type_checked() -> Callable[[T_CallableOrType], T_CallableOrType]:
    ...


@overload
def type_checked(func: T_CallableOrType) -> T_CallableOrType:
    ...


def type_checked(
    func=None,
):
    if _STELLAR_SDK_RUNTIME_TYPE_CHECKING:
        return _typechecked(func=func)
    else:
        return func
