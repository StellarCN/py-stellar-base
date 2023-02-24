import abc

from .. import xdr as stellar_xdr

__all__ = ["BaseScValAlias"]


class BaseScValAlias(metaclass=abc.ABCMeta):
    """An abstract base class for Stellar identifiers."""

    @abc.abstractmethod
    def to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        pass

    @classmethod
    def from_xdr_sc_val(cls, sc_val: stellar_xdr.SCVal):
        raise NotImplementedError
