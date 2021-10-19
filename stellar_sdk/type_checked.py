import os
from functools import wraps
from typing import Callable, Union

from typeguard import T_CallableOrType
from typeguard import typechecked as _typechecked

from .exceptions import TypeError as SDKTypeError

_STELLAR_SDK_ENFORCE_TYPE_CHECK_FLAG: str = "STELLAR_SDK_ENFORCE_TYPE_CHECK_FLAG"
_STELLAR_SDK_ENFORCE_TYPE_CHECK: bool = os.getenv(
    _STELLAR_SDK_ENFORCE_TYPE_CHECK_FLAG, "False"
).lower() in ("true", "1", "t")


def type_checked(
        func: T_CallableOrType,
) -> Union[Callable[[T_CallableOrType], T_CallableOrType], T_CallableOrType]:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = _typechecked(func=func, always=_STELLAR_SDK_ENFORCE_TYPE_CHECK)(
                *args, **kwargs
            )
        except TypeError as e:
            raise SDKTypeError(e) from e
        return result

    return wrapper
