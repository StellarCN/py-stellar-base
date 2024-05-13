from . import xdr as stellar_xdr

__all__ = ["DecoratedSignature"]


class DecoratedSignature:
    def __init__(
        self,
        signature_hint: bytes,
        signature: bytes,
    ) -> None:
        """The :class:`DecoratedSignature` object, which represents a DecoratedSignature on Stellar's network.

        :param signature_hint: The signer hint
        :param signature: The signature
        """
        self.signature_hint: bytes = signature_hint
        self.signature: bytes = signature

    def to_xdr_object(self) -> stellar_xdr.DecoratedSignature:
        """Returns the xdr object for this DecoratedSignature object.

        :return: XDR DecoratedSignature object
        """
        signature_hint = stellar_xdr.SignatureHint(self.signature_hint)
        signature = stellar_xdr.Signature(self.signature)
        return stellar_xdr.DecoratedSignature(signature_hint, signature)

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.DecoratedSignature
    ) -> "DecoratedSignature":
        """Create a :class:`DecoratedSignature` from an XDR DecoratedSignature object.

        :param xdr_object: The XDR DecoratedSignature object.
        :return: A new :class:`DecoratedSignature` object from the given XDR DecoratedSignature object.
        """
        signature_hint = xdr_object.hint.signature_hint
        signature = xdr_object.signature.signature
        return cls(signature_hint, signature)

    def __hash__(self):
        return hash((self.signature_hint, self.signature))

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (
            self.signature_hint == other.signature_hint
            and self.signature == other.signature
        )

    def __repr__(self):
        return f"<DecoratedSignature [signature_hint={self.signature_hint}, signature={self.signature}]>"
