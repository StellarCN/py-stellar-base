from . import xdr as stellar_xdr
from .signer_key import SignerKey
from .strkey import StrKey
from .type_checked import type_checked

__all__ = ["SignedPayloadSigner"]


@type_checked
class SignedPayloadSigner:
    """The :class:`SignedPayloadSigner` object, which represents a signed payload signer on Stellar's network.

    :param account_id: The account id.
    :param payload: The raw payload.
    """

    def __init__(self, account_id: str, payload: bytes) -> None:
        self.account_id: str = account_id
        self.payload: bytes = payload

    @classmethod
    def from_encoded_signer_key(self, signer_key: str) -> "SignedPayloadSigner":
        """Create Signer from strkey encoded signer key.

        :param signer_key: strkey encoded signer key. (ex. ``PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUAAAAFGBU``)
        :return: SignedPayloadSigner
        """
        key = SignerKey.ed25519_signed_payload(signer_key)
        return self.from_xdr_object(key.to_xdr_object())

    @property
    def encoded_signer_key(self) -> str:
        """
        return: The signer key encoded in Strkey format. (ex. ``PA7QYNF7SOWQ3GLR2BGMZEHXAVIRZA4KVWLTJJFC7MGXUA74P7UJUAAAAAOQCAQDAQCQMBYIBEFAWDANBYHRAEISCMKBKFQXDAMRUGY4DUAAAAFGBU``)
        """
        decoded_account_id = StrKey.decode_ed25519_public_key(self.account_id)
        payload_length = len(self.payload)
        payload = self.payload
        payload += b"\0" * ((4 - payload_length % 4) % 4)
        ed25519_signed_payload = (
            decoded_account_id
            + int.to_bytes(payload_length, length=4, byteorder="big")
            + payload
        )
        return SignerKey.ed25519_signed_payload(
            ed25519_signed_payload
        ).encoded_signer_key

    def to_xdr_object(self) -> stellar_xdr.SignerKey:
        """Returns the xdr object for this SignedPayloadSigner object.

        :return: XDR Signer object
        """
        decoded_account_id = StrKey.decode_ed25519_public_key(self.account_id)
        ed25519_signed_payload = stellar_xdr.SignerKeyEd25519SignedPayload(
            ed25519=stellar_xdr.Uint256(decoded_account_id),
            payload=self.payload,
        )
        return stellar_xdr.SignerKey(
            type=stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD,
            ed25519_signed_payload=ed25519_signed_payload,
        )

    @classmethod
    def from_xdr_object(
        cls, xdr_object: stellar_xdr.SignerKey
    ) -> "SignedPayloadSigner":
        """Create a :class:`SignedPayloadSigner` from an XDR SignerKey object.

        :param xdr_object: The XDR SignerKey object.
        :return: A new :class:`SignedPayloadSigner` object from the given XDR SignerKey object.
        """
        if (
            xdr_object.type
            != stellar_xdr.SignerKeyType.SIGNER_KEY_TYPE_ED25519_SIGNED_PAYLOAD
        ):
            raise ValueError("Invalid Signer Key type.")
        assert xdr_object.ed25519_signed_payload is not None
        encoded_account_id = StrKey.encode_ed25519_public_key(
            xdr_object.ed25519_signed_payload.ed25519.uint256
        )
        payload = xdr_object.ed25519_signed_payload.payload
        return cls(account_id=encoded_account_id, payload=payload)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.account_id == other.account_id and self.payload == self.payload

    def __str__(self):
        return f"<SignedPayloadSigner [account_id={self.account_id}, payload={self.payload}]>"
