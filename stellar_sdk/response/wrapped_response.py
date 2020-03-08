import json
from typing import Generic, TypeVar, Callable

from pydantic import ValidationError

from ..__version__ import __issues__
from ..exceptions import ParseResponseError

T = TypeVar("T")


class WrappedResponse(Generic[T]):
    """Used to wrap the data returned by Horizon.

    :param raw_data: Raw data returned by horizon.
    :param parse_func: The function for parsing raw data.
    """

    def __init__(self, raw_data: dict, parse_func: Callable[[dict], T]) -> None:
        self.raw_data: dict = raw_data
        self._parse_func = parse_func

    def parse(self) -> T:
        """Attempt to return the parsed data.

        :return: parsed data.
        :raises: :exc:`ParseResponseError <stellar_sdk.exceptions.ParseResponseError>`: This error occurs when parsing the
            response fails.
        """
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
