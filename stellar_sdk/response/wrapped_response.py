import json

from typing import Generic, TypeVar, Callable

T = TypeVar("T")


class WrappedResponse(Generic[T]):
    def __init__(self, raw_data: dict, parse_func: Callable[[dict], T]) -> None:
        self.raw_data: dict = raw_data
        self._parse_func = parse_func

    @property
    def parsed(self) -> T:
        return self._parse_func(self.raw_data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.raw_data == other.raw_data

    def __str__(self) -> str:
        return json.dumps(self.raw_data, indent=4)
