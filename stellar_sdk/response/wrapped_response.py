import json
from typing import Generic, TypeVar, Callable

from pydantic import ValidationError

from ..exceptions import ParseResponseError
from ..__version__ import __issues__
T = TypeVar("T")


class WrappedResponse(Generic[T]):
    def __init__(self, raw_data: dict, parse_func: Callable[[dict], T]) -> None:
        self.raw_data: dict = raw_data
        self._parse_func = parse_func

    def parse(self) -> T:
        try:
            return self._parse_func(self.raw_data)
        except ValidationError as e:
            raise ParseResponseError("Parsing the response failed. This may be due to a change in the Horizon field. "
                                     "Please try upgrading the SDK or submit a issue: {}.".format(__issues__)) from e

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.raw_data == other.raw_data

    def __str__(self) -> str:
        return json.dumps(self.raw_data, indent=4)
