from abc import ABCMeta, abstractmethod
from decimal import Decimal
from typing import Optional, Union

from .. import utils
from .. import xdr as stellar_xdr
from ..muxed_account import MuxedAccount

__all__ = ["Operation"]


class Operation(metaclass=ABCMeta):
    """The :class:`Operation` object, which represents an operation on
    Stellar's network.

    An operation is an individual command that mutates Stellar's ledger. It is
    typically rolled up into a transaction (a transaction is a list of
    operations with additional metadata).

    Operations are executed on behalf of the source account specified in the
    transaction, unless there is an override defined for the operation.

    For more on operations, see `Stellar's documentation on operations
    <https://developers.stellar.org/docs/glossary/operations/>`_ as
    well as `Stellar's List of Operations
    <https://developers.stellar.org/docs/start/list-of-operations/>`_,
    which includes information such as the security necessary for a given
    operation, as well as information about when validity checks occur on the
    network.

    The :class:`Operation` class is typically not used, but rather one of its
    subclasses is typically included in transactions.

    :param source: The source account for the operation. Defaults to the
        transaction's source account.

    """

    def __init__(self, source: Optional[Union[MuxedAccount, str]] = None) -> None:
        if isinstance(source, str):
            source = MuxedAccount.from_account(source)
        self.source: Optional[MuxedAccount] = source

    @property
    @abstractmethod
    def _XDR_OPERATION_TYPE(self) -> stellar_xdr.OperationType:
        pass  # pragma: no cover

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
        <https://developers.stellar.org/docs/issuing-assets/anatomy-of-an-asset/#amount-precision>`_
        for more information.

        :param value: The amount to convert to an integer for XDR
            serialization.

        """
        return utils.to_xdr_amount(value)

    @staticmethod
    def from_xdr_amount(value: int) -> str:
        """Converts a str amount from an XDR amount object

        :param value: The amount to convert to a string from an XDR int64
            amount.

        """
        return utils.from_xdr_amount(value)

    @abstractmethod
    def _to_operation_body(self) -> stellar_xdr.OperationBody:
        pass  # pragma: no cover

    def to_xdr_object(self) -> stellar_xdr.Operation:
        """Creates an XDR Operation object that represents this
        :class:`Operation`.

        """
        source_account = None
        if self.source:
            source_account = self.source.to_xdr_object()
        return stellar_xdr.Operation(source_account, self._to_operation_body())

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.Operation) -> "Operation":
        """Create the appropriate :class:`Operation` subclass from the XDR
        object.

        :param xdr_object: The XDR object to create an :class:`Operation` (or
            subclass) instance from.
        """
        for sub_cls in cls.__subclasses__():
            if sub_cls._XDR_OPERATION_TYPE == xdr_object.body.type:
                return sub_cls.from_xdr_object(xdr_object)
        raise NotImplementedError(
            f"Operation of type={xdr_object.body.type} is not implemented."
        )

    @staticmethod
    def get_source_from_xdr_obj(
        xdr_object: stellar_xdr.Operation,
    ) -> Optional[MuxedAccount]:
        """Get the source account from account the operation xdr object.

        :param xdr_object: the operation xdr object.
        :return: The source account from account the operation xdr object.
        """
        if xdr_object.source_account:
            return MuxedAccount.from_xdr_object(xdr_object.source_account)
        return None

    def __hash__(self):
        return hash(self.to_xdr_object())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_xdr_object() == other.to_xdr_object()
