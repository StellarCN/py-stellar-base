import abc
from stellar_sdk import xdr as stellar_xdr


class BaseScValAlias(metaclass=abc.ABCMeta):
    """An abstract base class for Stellar identifiers."""

    @abc.abstractmethod
    def _to_xdr_sc_val(self) -> stellar_xdr.SCVal:
        pass
