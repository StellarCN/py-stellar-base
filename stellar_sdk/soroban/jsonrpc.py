from typing import Union, TypeVar, Generic, Optional

from pydantic.generics import GenericModel

T = TypeVar("T")
E = TypeVar("E")

Id = Union[str, int]


class Request(GenericModel, Generic[T]):
    jsonrpc: str = "2.0"
    id: Id  # TODO: Optional?
    method: str
    params: Optional[T]


class Error(GenericModel, Generic[E]):
    code: int
    message: Optional[str]
    data: Optional[E]


class Response(GenericModel, Generic[T, E]):
    jsonrpc: str
    id: Id
    result: Optional[T]
    error: Optional[Error[E]]
