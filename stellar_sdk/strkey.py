import base64
import binascii
import struct
from typing import Union

from .vendor.crc16 import crc16xmodem

from .exceptions import (
    Ed25519SecretSeedInvalidError,
    Ed25519PublicKeyInvalidError,
    ValueError,
    TypeError,
)

__all__ = ["StrKey"]

_version_bytes = {
    "ed25519_public_key": binascii.a2b_hex("30"),  # G 48 6 << 3
    "ed25519_secret_seed": binascii.a2b_hex("90"),  # S 144 18 << 3
    "pre_auth_tx": binascii.a2b_hex("98"),  # T 152 19 << 3
    "sha256_hash": binascii.a2b_hex("b8"),  # X 184 23 << 3
}


class StrKey:
    """StrKey is a helper class that allows encoding and decoding strkey."""

    @staticmethod
    def encode_ed25519_public_key(data: bytes) -> str:
        """Encodes data to strkey ed25519 public key.

        :param data: data to encode
        :return: strkey ed25519 public key
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return encode_check("ed25519_public_key", data)

    @staticmethod
    def decode_ed25519_public_key(data: str) -> bytes:
        """Decodes strkey ed25519 public key to raw data.

        :param data: strkey ed25519 public key
        :return: raw bytes
        :raises:
            :exc:`Ed25519PublicKeyInvalidError <stellar_sdk.exceptions.Ed25519PublicKeyInvalidError>`
        """
        try:
            return decode_check("ed25519_public_key", data)
        except Exception:
            raise Ed25519PublicKeyInvalidError(
                "Invalid Ed25519 Public Key: {}".format(data)
            )

    @staticmethod
    def is_valid_ed25519_public_key(public_key: str) -> bool:
        """Returns True if the given Stellar public key is a valid ed25519 public key.

        :param public_key: strkey ed25519 public key to check
        :return: `True` if the given Stellar public key is a valid ed25519 public key.
        """
        return is_valid("ed25519_public_key", public_key)

    @staticmethod
    def encode_ed25519_secret_seed(data: bytes) -> str:
        """Encodes data to strkey ed25519 seed.

        :param data: data to encode
        :return: strkey ed25519 seed
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return encode_check("ed25519_secret_seed", data)

    @staticmethod
    def decode_ed25519_secret_seed(data: str) -> bytes:
        """Decodes strkey ed25519 seed to raw data.

        :param data: strkey ed25519 seed
        :return: raw bytes
        :raises:
            :exc:`Ed25519SecretSeedInvalidError <stellar_sdk.exceptions.Ed25519SecretSeedInvalidError>`
        """
        try:
            return decode_check("ed25519_secret_seed", data)
        except Exception:
            raise Ed25519SecretSeedInvalidError(f"Invalid Ed25519 Secret Seed: {data}")

    @staticmethod
    def is_valid_ed25519_secret_seed(seed: str):
        """Returns True if the given Stellar secret key is a valid ed25519 secret seed.

        :param seed: strkey ed25519 secret seed
        :return: `True` if the given Stellar secret key is a valid ed25519 secret seed.
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return is_valid("ed25519_secret_seed", seed)

    @staticmethod
    def encode_pre_auth_tx(data: bytes) -> str:
        """Encodes data to strkey preAuthTx.

        :param data: data to encode
        :return: strkey preAuthTx
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return encode_check("pre_auth_tx", data)

    @staticmethod
    def decode_pre_auth_tx(data: str) -> bytes:
        """Decodes strkey PreAuthTx to raw data.

        :param data: strkey preAuthTx
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return decode_check("pre_auth_tx", data)

    @staticmethod
    def encode_sha256_hash(data: bytes) -> str:
        """Encodes data to strkey sha256 hash.

        :param data: data to encode
        :return: strkey sha256 hash
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return encode_check("sha256_hash", data)

    @staticmethod
    def decode_sha256_hash(data: str) -> bytes:
        """Decodes strkey sha256 hash to raw data.

        :param data: strkey sha256 hash
        :return: raw bytes
        :raises:
            :exc:`ValueError <stellar_sdk.exceptions.ValueError>`
            :exc:`TypeError <stellar_sdk.exceptions.TypeError>`
        """
        return decode_check("sha256_hash", data)


def decode_check(version_byte_name: str, encoded: str) -> bytes:
    encoded_data = _bytes_from_decode_data(encoded)
    encoded_data = encoded_data + b"=" * ((4 - len(encoded_data) % 4) % 4)

    try:
        decoded_data = base64.b32decode(encoded_data)
    except binascii.Error:
        raise ValueError("Incorrect padding.")

    if encoded_data != base64.b32encode(decoded_data):  # Is that even possible?
        raise ValueError("Invalid encoded bytes.")

    version_byte = decoded_data[0:1]
    payload = decoded_data[0:-2]
    data = decoded_data[1:-2]
    checksum = decoded_data[-2:]

    expected_version = _version_bytes.get(version_byte_name)
    if expected_version is None:
        raise TypeError(
            f'{version_byte_name} is not a valid version byte name. expected one of "ed25519_public_key", '
            '"ed25519_secret_seed", "pre_auth_tx", "sha256_hash"'
        )

    if version_byte != expected_version:
        raise TypeError(
            f"Invalid version byte. Expected {expected_version!r}, got {version_byte!r}"
        )

    expected_checksum = _calculate_checksum(payload)
    if expected_checksum != checksum:
        raise ValueError("Invalid checksum")

    return data


def encode_check(version_byte_name: str, data: bytes) -> str:
    if data is None:
        raise ValueError("cannot encode null data")

    version_byte = _version_bytes.get(version_byte_name)
    if version_byte is None:
        raise TypeError(
            f'{version_byte_name} is not a valid version byte name. expected one of "ed25519_public_key", '
            '"ed25519_secret_seed", "pre_auth_tx", "sha256_hash"'
        )
    payload = version_byte + data
    crc = _calculate_checksum(payload)
    return base64.b32encode(payload + crc).decode("utf-8").rstrip("=")


def is_valid(version_byte_name: str, encoded: str) -> bool:
    if encoded and len(encoded) != 56:
        return False
    try:
        decoded = decode_check(version_byte_name, encoded)
        # if len(decoded) != 32:
        #     return False
    except (ValueError, TypeError):
        return False
    return True


def _bytes_from_decode_data(s: Union[str, bytes, bytearray]) -> bytes:
    """copy from base64._bytes_from_decode_data"""
    bytes_types = (bytes, bytearray)  # Types acceptable as binary data
    if isinstance(s, str):
        try:
            return s.encode("ascii")
        except UnicodeEncodeError:
            raise ValueError("string argument should contain only ASCII characters")
    if isinstance(s, bytes_types):
        return s
    try:
        return memoryview(s).tobytes()
    except TypeError:
        raise TypeError(
            f"argument should be a bytes-like object or ASCII "
            f"string, not {s.__class__.__name__}"
        ) from None


def _calculate_checksum(payload):
    # This code calculates CRC16-XModem checksum of payload
    checksum = crc16xmodem(payload)
    # Ensure that the checksum is in LSB order.
    checksum = struct.pack("<H", checksum)
    return checksum
