import base64
import binascii
import struct
from enum import Enum

from xdrlib3 import Packer, Unpacker

from . import xdr as stellar_xdr
from .exceptions import (
    Ed25519PublicKeyInvalidError,
    Ed25519SecretSeedInvalidError,
    MuxedEd25519AccountInvalidError,
)

__all__ = ["StrKey"]


class _VersionByte(Enum):
    ED25519_PUBLIC_KEY = binascii.a2b_hex("30")  # G 48 6 << 3
    ED25519_SECRET_SEED = binascii.a2b_hex("90")  # S 144 18 << 3
    PRE_AUTH_TX = binascii.a2b_hex("98")  # T 152 19 << 3
    SHA256_HASH = binascii.a2b_hex("b8")  # X 184 23 << 3
    MUXED_ACCOUNT = binascii.a2b_hex("60")  # M 96 12 << 3
    ED25519_SIGNED_PAYLOAD = binascii.a2b_hex("78")  # P 120 15 << 3
    CONTRACT = binascii.a2b_hex("10")  # C 16 2 << 3


class StrKey:
    """StrKey is a helper class that allows encoding and decoding strkey."""

    @staticmethod
    def encode_ed25519_public_key(data: bytes) -> str:
        """Encodes data to encoded ed25519 public key strkey.

        :param data: data to encode
        :return: encoded ed25519 public key strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        return _encode_check(_VersionByte.ED25519_PUBLIC_KEY, data)

    @staticmethod
    def decode_ed25519_public_key(data: str) -> bytes:
        """Decodes encoded ed25519 public key strkey to raw data.

        :param data: encoded ed25519 public key strkey
        :return: raw bytes
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`
        """
        try:
            return _decode_check(_VersionByte.ED25519_PUBLIC_KEY, data)
        except Exception:
            raise Ed25519PublicKeyInvalidError(f"Invalid Ed25519 Public Key: {data}")

    @staticmethod
    def is_valid_ed25519_public_key(public_key: str) -> bool:
        """Returns ``True`` if the given `seed` is a valid ed25519 public key strkey.

        :param public_key: encoded ed25519 public key strkey
        :return: ``True`` if the given key is valid
        """
        return _is_valid(_VersionByte.ED25519_PUBLIC_KEY, public_key)

    @staticmethod
    def encode_ed25519_secret_seed(data: bytes) -> str:
        """Encodes data to encoded ed25519 secret seed strkey.

        :param data: data to encode
        :return: encoded ed25519 secret seed strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        return _encode_check(_VersionByte.ED25519_SECRET_SEED, data)

    @staticmethod
    def decode_ed25519_secret_seed(data: str) -> bytes:
        """Decodes encoded ed25519 secret seed strkey to raw data.

        :param data: encoded ed25519 secret seed strkey
        :return: raw bytes
        :raises:
            :exc:`Ed25519SecretSeedInvalidError <stellar_sdk.exceptions.Ed25519SecretSeedInvalidError>`
        """
        try:
            return _decode_check(_VersionByte.ED25519_SECRET_SEED, data)
        except Exception:
            raise Ed25519SecretSeedInvalidError(f"Invalid Ed25519 Secret Seed: {data}")

    @staticmethod
    def is_valid_ed25519_secret_seed(seed: str) -> bool:
        """Returns ``True`` if the given `seed` is a valid ed25519 secret seed strkey.

        :param seed: encoded ed25519 secret seed strkey
        :return: ``True`` if the given key is valid
        """
        return _is_valid(_VersionByte.ED25519_SECRET_SEED, seed)

    @staticmethod
    def encode_pre_auth_tx(data: bytes) -> str:
        """Encodes data to encoded pre auth tx strkey.

        :param data: data to encode
        :return: encoded pre auth tx strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        return _encode_check(_VersionByte.PRE_AUTH_TX, data)

    @staticmethod
    def decode_pre_auth_tx(data: str) -> bytes:
        """Decodes encoded pre auth tx strkey to raw data.

        :param data: encoded pre auth tx strkey
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        try:
            return _decode_check(_VersionByte.PRE_AUTH_TX, data)
        except Exception as e:
            raise ValueError(f"Invalid Pre Auth Tx Key: {data}") from e

    @staticmethod
    def is_valid_pre_auth_tx(pre_auth_tx: str) -> bool:
        """Returns ``True`` if the given `pre_auth_tx` is a valid encoded pre auth tx strkey.

        :param pre_auth_tx: encoded pre auth tx strkey
        :return: ``True`` if the given key is valid
        """
        return _is_valid(_VersionByte.PRE_AUTH_TX, pre_auth_tx)

    @staticmethod
    def encode_sha256_hash(data: bytes) -> str:
        """Encodes data to encoded sha256 hash strkey.

        :param data: data to encode
        :return: encoded sha256 hash strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        return _encode_check(_VersionByte.SHA256_HASH, data)

    @staticmethod
    def decode_sha256_hash(data: str) -> bytes:
        """Decodes encoded sha256 hash strkey to raw data.

        :param data: encoded sha256 hash strkey
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        try:
            return _decode_check(_VersionByte.SHA256_HASH, data)
        except Exception as e:
            raise ValueError(f"Invalid sha256 Hash Key: {data}") from e

    @staticmethod
    def is_valid_sha256_hash(sha256_hash: str) -> bool:
        """Returns ``True`` if the given `sha256_hash` is a valid encoded sha256 hash(HashX) strkey.

        :param sha256_hash: encoded sha256 hash(HashX) strkey
        :return: ``True`` if the given key is valid
        """
        return _is_valid(_VersionByte.SHA256_HASH, sha256_hash)

    @staticmethod
    def encode_muxed_account(data: stellar_xdr.MuxedAccount) -> str:
        """Encodes data to encoded muxed account strkey.

        :param data: data to encode
        :return: encoded muxed account strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        if data.type == stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519:
            assert data.ed25519 is not None
            return StrKey.encode_ed25519_public_key(data.ed25519.uint256)

        assert data.med25519 is not None
        packer = Packer()
        data.med25519.ed25519.pack(packer)
        data.med25519.id.pack(packer)
        return _encode_check(_VersionByte.MUXED_ACCOUNT, packer.get_buffer())

    @staticmethod
    def decode_muxed_account(data: str) -> stellar_xdr.MuxedAccount:
        """Decodes encoded muxed account strkey to raw data.

        :param data: encoded muxed account strkey
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        data_length = len(data)
        if data_length == 56:
            muxed = stellar_xdr.MuxedAccount(
                type=stellar_xdr.CryptoKeyType.KEY_TYPE_ED25519,
                ed25519=stellar_xdr.Uint256(StrKey.decode_ed25519_public_key(data)),
            )
        elif data_length == 69:
            # let's optimize it in v3.
            try:
                xdr_bytes = _decode_check(_VersionByte.MUXED_ACCOUNT, data)
            except Exception:
                raise MuxedEd25519AccountInvalidError(
                    "Invalid Muxed Account: {}".format(data)
                )

            unpacker = Unpacker(xdr_bytes)
            ed25519 = stellar_xdr.Uint256.unpack(unpacker)
            id = stellar_xdr.Uint64.unpack(unpacker)
            med25519 = stellar_xdr.MuxedAccountMed25519(
                id=id,
                ed25519=ed25519,
            )
            muxed = stellar_xdr.MuxedAccount(
                type=stellar_xdr.CryptoKeyType.KEY_TYPE_MUXED_ED25519, med25519=med25519
            )
        else:
            raise ValueError("Invalid encoded string, this is not a valid account.")
        return muxed

    @staticmethod
    def encode_ed25519_signed_payload(data: bytes) -> str:
        """Encodes data to encoded ed25519 signed payload strkey.

        :param data: data to encode
        :return: encoded ed25519 signed payload strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        return _encode_check(_VersionByte.ED25519_SIGNED_PAYLOAD, data)

    @staticmethod
    def decode_ed25519_signed_payload(data: str) -> bytes:
        """Decodes encoded ed25519 signed payload strkey to raw data.

        :param data: encoded ed25519 signed payload strkey
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        try:
            return _decode_check(_VersionByte.ED25519_SIGNED_PAYLOAD, data)
        except Exception as e:
            raise ValueError(f"Invalid Ed25519 Signed Payload Key: {data}") from e

    @staticmethod
    def is_valid_ed25519_signed_payload(ed25519_signed_payload: str) -> bool:
        """Returns ``True`` if the given `ed25519_signed_payload` is a valid encoded ed25519 signed payload strkey.

        :param ed25519_signed_payload: encoded ed25519 signed payload strkey
        :return: ``True`` if the given key is valid
        """
        return _is_valid(_VersionByte.ED25519_SIGNED_PAYLOAD, ed25519_signed_payload)

    @staticmethod
    def encode_contract(data: bytes) -> str:
        """Encodes data to encoded contract strkey.

        :param data: data to encode
        :return: encoded contract strkey
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        return _encode_check(_VersionByte.CONTRACT, data)

    @staticmethod
    def decode_contract(data: str) -> bytes:
        """Decodes encoded contract strkey to raw data.

        :param data: encoded contract strkey
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
        """
        try:
            return _decode_check(_VersionByte.CONTRACT, data)
        except Exception as e:
            raise ValueError(f"Invalid Pre Auth Tx Key: {data}") from e

    @staticmethod
    def is_valid_contract(contract: str) -> bool:
        """Returns ``True`` if the given `contract` is a valid encoded contract strkey.

        :param pre_auth_tx: encoded contract strkey
        :return: ``True`` if the given key is valid
        """
        return _is_valid(_VersionByte.CONTRACT, contract)


def _decode_check(version_byte: _VersionByte, encoded: str) -> bytes:
    encoded_data = encoded.encode("ascii")
    encoded_data = encoded_data + b"=" * ((8 - len(encoded_data) % 8) % 8)

    try:
        decoded_data = base64.b32decode(encoded_data)
    except binascii.Error:
        raise ValueError("Incorrect padding.")

    if encoded_data != base64.b32encode(decoded_data):  # Is that even possible?
        raise ValueError("Invalid encoded bytes.")

    version_byte_in_data = decoded_data[0:1]
    payload = decoded_data[0:-2]
    data = decoded_data[1:-2]
    checksum = decoded_data[-2:]

    if version_byte.value != version_byte_in_data:
        raise ValueError(
            f"Invalid version byte. Expected {version_byte.value!r}, got {version_byte_in_data!r}"
        )

    if version_byte == _VersionByte.ED25519_SIGNED_PAYLOAD:
        if len(data) < 32 + 4 + 4 or len(data) > 32 + 4 + 64:
            raise ValueError(f"Invalid length: {encoded}")
    elif version_byte == _VersionByte.MUXED_ACCOUNT:
        if len(data) != 32 + 8:
            raise ValueError(f"Invalid length: {encoded}")
    else:
        if len(data) != 32:
            raise ValueError(f"Invalid length: {encoded}")

    expected_checksum = _calculate_checksum(payload)
    if expected_checksum != checksum:
        raise ValueError("Invalid checksum")
    if version_byte == _VersionByte.ED25519_SIGNED_PAYLOAD:
        payload_length_prefix = int.from_bytes(data[32:36], byteorder="big")
        if len(data[36:]) % 4 != 0:
            raise ValueError(f"Invalid Ed25519 Signed Payload Key: {encoded}")
        if payload_length_prefix + ((4 - payload_length_prefix % 4) % 4) != len(
            data[36:]
        ):
            raise ValueError(f"Invalid Ed25519 Signed Payload Key: {encoded}")
    return data


def _encode_check(version_byte: _VersionByte, data: bytes) -> str:
    payload = version_byte.value + data
    crc = _calculate_checksum(payload)
    return base64.b32encode(payload + crc).decode("utf-8").rstrip("=")


def _is_valid(version_byte: _VersionByte, encoded: str) -> bool:
    try:
        _decode_check(version_byte, encoded)
    except (ValueError, TypeError):
        return False
    return True


def _get_version_byte_for_prefix(encoded: str) -> _VersionByte:
    prefix = encoded[0]
    _version_byte = ((ord(prefix) - ord("A")) << 3).to_bytes(1, byteorder="big")
    return _VersionByte(_version_byte)


def _calculate_checksum(payload: bytes) -> bytes:
    # memo note: https://gist.github.com/manran/a8357808ef71415d266dc64f0079f298
    # This code calculates CRC16-XModem checksum of payload
    checksum = binascii.crc_hqx(payload, 0)
    # Ensure that the checksum is in LSB order.
    return struct.pack("<H", checksum)
