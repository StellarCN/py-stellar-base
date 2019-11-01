import decimal
from abc import ABCMeta, abstractmethod
from decimal import Decimal, Context, Inexact
from typing import Optional, List, Union

from .utils import check_source
from ..keypair import Keypair
from ..strkey import StrKey
from ..xdr import Xdr
from ..exceptions import ValueError, TypeError


class Operation(metaclass=ABCMeta):
    """The :class:`Operation` object, which represents an operation on
    Stellar's network.

    An operation is an individual command that mutates Stellar's ledger. It is
    typically rolled up into a transaction (a transaction is a list of
    operations with additional metadata).

    Operations are executed on behalf of the source account specified in the
    transaction, unless there is an override defined for the operation.

    For more on operations, see `Stellar's documentation on operations
    <https://www.stellar.org/developers/guides/concepts/operations.html>`_ as
    well as `Stellar's List of Operations
    <https://www.stellar.org/developers/guides/concepts/list-of-operations.html>`_,
    which includes information such as the security necessary for a given
    operation, as well as information about when validity checks occur on the
    network.

    The :class:`Operation` class is typically not used, but rather one of its
    subclasses is typically included in transactions.

    :param source: The source account for the payment. Defaults to the
        transaction's source account.

    """

    _ONE = Decimal(10 ** 7)

    def __init__(self, source: str = None) -> None:
        check_source(source)
        self.source: Optional[str] = source

    @classmethod
    def type_code(cls) -> int:
        pass

    @staticmethod
    def to_xdr_amount(value: Union[str, Decimal]) -> int:
        """Converts an amount to the appropriate value to send over the network
        as a part of an XDR object.

        Each asset amount is encoded as a signed 64-bit integer in the XDR
        structures. An asset amount unit (that which is seen by end users) is
        scaled down by a factor of ten million (10,000,000) to arrive at the
        native 64-bit integer representation. For example, the integer amount
        value 25,123,456 equals 2.5123456 units of the asset. This scaling
        allows for seven decimal places of precision in human-friendly amount
        units.

        This static method correctly multiplies the value by the scaling factor
        in order to come to the integer value used in XDR structures.

        See `Stellar's documentation on Asset Precision
        <https://www.stellar.org/developers/guides/concepts/assets.html#amount-precision-and-representation>`_
        for more information.

        :param value: The amount to convert to an integer for XDR
            serialization.

        """
        if not (isinstance(value, str) or isinstance(value, Decimal)):
            raise TypeError(
                "Value of type '{}' must be of type {} or {}, but got {}.".format(
                    value, str, Decimal, type(value)
                )
            )
        # throw exception if value * ONE has decimal places (it can't be represented as int64)
        try:
            amount = int(
                (Decimal(value) * Operation._ONE).to_integral_exact(
                    context=Context(traps=[Inexact])
                )
            )
        except decimal.Inexact:
            raise ValueError(
                "Value of '{}' must have at most 7 digits after the decimal.".format(
                    value
                )
            )

        if amount < 0 or amount > 9223372036854775807:
            raise ValueError(
                "Value of '{}' must represent a positive number "
                "and the max valid value is 922337203685.4775807.".format(value)
            )

        return amount

    @staticmethod
    def from_xdr_amount(value: int) -> str:
        """Converts an str amount from an XDR amount object

        :param value: The amount to convert to a string from an XDR int64
            amount.

        """
        return str(Decimal(value) / Operation._ONE)

    @abstractmethod
    def _to_operation_body(self) -> Xdr.nullclass:
        pass

    def to_xdr_object(self) -> Xdr.types.Operation:
        """Creates an XDR Operation object that represents this
        :class:`Operation`.

        """
        source_account: List[Xdr.types.PublicKey] = []
        if self.source is not None:
            source_account = [Keypair.from_public_key(self.source).xdr_account_id()]

        return Xdr.types.Operation(source_account, self._to_operation_body())

    @classmethod
    def from_xdr_object(cls, operation_xdr_object: Xdr.types.Operation) -> "Operation":
        """Create the appropriate :class:`Operation` subclass from the XDR
        object.

        :param operation_xdr_object: The XDR object to create an :class:`Operation` (or
            subclass) instance from.
        """
        for sub_cls in cls.__subclasses__():
            if sub_cls.type_code() == operation_xdr_object.type:
                return sub_cls.from_xdr_object(operation_xdr_object)
        raise NotImplementedError(
            "Operation of type={} is not implemented"
            ".".format(operation_xdr_object.type)
        )

    @staticmethod
    def get_source_from_xdr_obj(xdr_object: Xdr.types.Operation) -> Optional[str]:
        """Get the source account from account the operation xdr object.

        :param xdr_object: the operation xdr object.
        :return: The source account from account the operation xdr object.
        """
        if xdr_object.sourceAccount:
            return StrKey.encode_ed25519_public_key(xdr_object.sourceAccount[0].ed25519)
        return None

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented  # pragma: no cover
        return self.to_xdr_object().to_xdr() == other.to_xdr_object().to_xdr()
