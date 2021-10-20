import os
from typing import Callable, overload

from typeguard import T_CallableOrType
from typeguard import typechecked as _typechecked

_STELLAR_SDK_ENFORCE_TYPE_CHECK_FLAG: str = "STELLAR_SDK_ENFORCE_TYPE_CHECK"
_STELLAR_SDK_ENFORCE_TYPE_CHECK: bool = os.getenv(
    _STELLAR_SDK_ENFORCE_TYPE_CHECK_FLAG, "False"
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
    return _typechecked(func=func, always=_STELLAR_SDK_ENFORCE_TYPE_CHECK)
