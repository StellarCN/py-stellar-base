from . import xdr as stellar_xdr

__all__ = ["LedgerBounds"]


class LedgerBounds:
    """LedgerBounds represents the ledger interval that a transaction is valid.

    :param min_ledger: The minimum ledger this transaction is valid at, or after.
        Cannot be negative. If the value is ``0``, the transaction is valid immediately.
    :param max_ledger: The maximum ledger this transaction is valid before.
        Cannot be negative. If the value is ``0``, the transaction is valid indefinitely.
    :raises: :exc:`ValueError <stellar_sdk.exceptions.ValueError>`: if `max_ledger` less than `min_ledger`.
    """

    def __init__(self, min_ledger: int, max_ledger: int) -> None:
        if min_ledger < 0:
            raise ValueError("min_ledger cannot be negative.")

        if max_ledger < 0:
            raise ValueError("max_ledger cannot be negative.")

        if 0 < max_ledger < min_ledger:
            raise ValueError("min_ledger cannot be greater than max_ledger.")

        self.min_ledger: int = min_ledger
        self.max_ledger: int = max_ledger

    def to_xdr_object(self) -> stellar_xdr.LedgerBounds:
        """Returns the xdr object for this LedgerBounds object.

        :return: XDR LedgerBounds object
        """
        min_ledger = stellar_xdr.Uint32(self.min_ledger)
        max_ledger = stellar_xdr.Uint32(self.max_ledger)
        return stellar_xdr.LedgerBounds(min_ledger, max_ledger)

    @classmethod
    def from_xdr_object(cls, xdr_object: stellar_xdr.LedgerBounds) -> "LedgerBounds":
        """Create a :class:`LedgerBounds` from an XDR LedgerBounds object.

        :param xdr_object: The XDR LedgerBounds object.
        :return: A new :class:`LedgerBounds` object from the given XDR LedgerBounds object.
        """
        return cls(
            min_ledger=xdr_object.min_ledger.uint32,
            max_ledger=xdr_object.max_ledger.uint32,
        )

    def __hash__(self):
        return hash((self.min_ledger, self.max_ledger))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.min_ledger == other.min_ledger and self.max_ledger == other.max_ledger
        )

    def __repr__(self):
        return f"<LedgerBounds [min_ledger={self.min_ledger}, max_ledger={self.max_ledger}]>"
