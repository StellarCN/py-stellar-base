import json
from typing import Generic, TypeVar, Callable

from pydantic import ValidationError

from ..__version__ import __issues__
from ..call_builder import base_call_builder
from ..client.response import Response
from ..exceptions import ParseResponseError, NotPageableError
from ..response.rate_limit_info import RateLimitInfo

T = TypeVar("T")


class WrappedResponse(Generic[T]):
    """Used to wrap the data returned by Horizon.

    :param raw_data: Raw data returned by horizon.
    :param parse_func: The function for parsing raw data.
    """

    def __init__(
        self,
        parse_func: Callable[[dict], T],
        raw_data: dict = None,
        raw_response: Response = None,
        builder: "base_call_builder.BaseCallBuilder" = None,
    ) -> None:
        if raw_data is not None:
            self.raw_data = raw_data

        self._raw_response: Response = raw_response
        if raw_response is not None:
            self.raw_data: dict = raw_response.json()
            self.raw_headers = raw_response.headers
        self._parse_func = parse_func
        self._builder = builder

    def parse_data(self) -> T:
        """Attempt to return the parsed data.

        :return: parsed data.
        :raises: :exc:`ParseResponseError <stellar_sdk.exceptions.ParseResponseError>`: This error occurs when parsing the
            response fails.
        """
        try:
            return self._parse_func(self.raw_data)
        except ValidationError as e:
            raise ParseResponseError(
                "Parsing the response failed. This may be due to a change in the Horizon field. "
                "Please try upgrading the SDK or submit a issue: {}.".format(__issues__)
            ) from e

    def parse_rate_limit_info(self) -> RateLimitInfo:
        """Attempt to return the parsed data.

        :return: parsed data.
        :raises: :exc:`ParseResponseError <stellar_sdk.exceptions.ParseResponseError>`: This error occurs when parsing the
            response fails.
        """
        if self.raw_headers is None:
            raise ParseResponseError("Can not found rate limit info.")

        try:
            return RateLimitInfo.parse_obj(self.raw_headers)
        except ValidationError as e:
            raise ParseResponseError(
                "Parsing the response failed. This may be due to a change in the Horizon response headers. "
                "Please try upgrading the SDK or submit a issue: {}.".format(__issues__)
            ) from e

    def next(self):
        if self._builder is None:
            raise NotPageableError("This endpoint does not support this method.")
        return self._builder.next()

    def prev(self):
        if self._builder is None:
            raise NotPageableError("This endpoint does not support this method.")
        return self._builder.prev()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.raw_data == other.raw_data

    def __str__(self) -> str:
        return json.dumps(self.raw_data, indent=4)
