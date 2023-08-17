import abc

from ... import xdr as stellar_xdr

__all__ = ["BaseScValAlias"]


class BaseScValAlias(metaclass=abc.ABCMeta):
    """This is an abstract class. If you want to create a new Soroban type alias,
    you need to inherit from this class and implement its methods, otherwise
    your instance will not be correctly convertible to an :class:`stellar_sdk.xdr.SCVal` XDR object.
    """

    @abc.abstractmethod
    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        """Converts the instance to an :class:`stellar_sdk.xdr.SCVal` XDR object.

        :return: An :class:`stellar_sdk.xdr.SCVal` XDR object.
        """

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal) -> "BaseScValAlias":
        """Converts an :class:`stellar_sdk.xdr.SCVal` object to an instance of the class.

        :param sc_val: An :class:`stellar_sdk.xdr.SCVal` XDR object.
        :return: An instance of the class.
        """
        raise NotImplementedError
