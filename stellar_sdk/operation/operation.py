import decimal
import typing
from abc import ABCMeta, abstractmethod
from decimal import Decimal, Context, Inexact

from ..strkey import StrKey
from ..keypair import Keypair
from ..stellarxdr import Xdr
from ..types import OperationUnion


class Operation(metaclass=ABCMeta):
    _ONE = Decimal(10 ** 7)

    def __init__(self, source: str = None) -> None:
        self.source = source

    @classmethod
    def type_code(cls) -> int:
        pass  # pragma: no cover

    @staticmethod
    def to_xdr_amount(value: str) -> int:
        if not isinstance(value, str):
            raise TypeError("Value of type '{}' must be of type String, but got {}.".format(value, type(value)))
        # throw exception if value * ONE has decimal places (it can't be represented as int64)
        try:
            amount = int((Decimal(value) * Operation._ONE).to_integral_exact(context=Context(traps=[Inexact])))
        except decimal.Inexact:
            raise ValueError("Value of '{}' must have at most 7 digits after the decimal.".format(value))

        if amount < 0 or amount > 9223372036854775807:
            raise ValueError("Value of '{}' must represent a positive number "
                             "and the max valid value is 9223372036854775807.".format(value))

        return amount

    @staticmethod
    def from_xdr_amount(value: int) -> str:
        return str(Decimal(value) / Operation._ONE)

    @abstractmethod
    def to_operation_body(self) -> Xdr.nullclass:
        pass  # pragma: no cover

    def to_xdr_object(self) -> Xdr.types.Operation:
        source_account = []
        if self.source is not None:
            source_account = [Keypair.from_public_key(self.source).xdr_account_id()]

        return Xdr.types.Operation(source_account, self.to_operation_body())

    @classmethod
    def from_xdr_object(cls, op_xdr_object: Xdr.types.Operation) -> OperationUnion:
        for sub_cls in cls.__subclasses__():
            if sub_cls.type_code() == op_xdr_object.type:
                return sub_cls.from_xdr_object(op_xdr_object)
        raise NotImplementedError("Operation of type={} is not implemented"
                                  ".".format(op_xdr_object.type))

    @staticmethod
    def get_source_from_xdr_obj(xdr_object: Xdr.types.Operation) -> typing.Optional[str]:
        if xdr_object.sourceAccount:
            return StrKey.encode_ed25519_public_key(xdr_object.sourceAccount[0].ed25519)
        return None

    def __eq__(self, other: 'Operation') -> bool:
        return self.to_xdr_object().to_xdr() == self.to_xdr_object().to_xdr()
