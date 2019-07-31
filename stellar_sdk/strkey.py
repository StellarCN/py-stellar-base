import base64
import binascii
import struct

from crc16 import crc16xmodem

from .exceptions import Ed25519SecretSeedInvalidError, Ed25519PublicKeyInvalidError

_version_bytes = {
    'ed25519_public_key': binascii.a2b_hex('30'),  # G 48 6 << 3
    'ed25519_secret_seed': binascii.a2b_hex('90'),  # S 144 18 << 3
    'pre_auth_tx': binascii.a2b_hex('98'),  # T 152 19 << 3
    'sha256_hash': binascii.a2b_hex('b8')  # X 184 23 << 3
}


class StrKey:
    @staticmethod
    def encode_ed25519_public_key(data: bytes) -> str:
        return encode_check('ed25519_public_key', data)

    @staticmethod
    def decode_ed25519_public_key(data: str) -> bytes:
        try:
            return decode_check('ed25519_public_key', data)
        except Exception:
            raise Ed25519PublicKeyInvalidError('Invalid Ed25519 Public Key: {}'.format(data))

    @staticmethod
    def is_valid_ed25519_public_key(public_key: str):
        return is_valid('ed25519_public_key', public_key)

    @staticmethod
    def encode_ed25519_secret_seed(data: bytes) -> str:
        return encode_check('ed25519_secret_seed', data)

    @staticmethod
    def decode_ed25519_secret_seed(data: str) -> bytes:
        try:
            return decode_check('ed25519_secret_seed', data)
        except Exception:
            raise Ed25519SecretSeedInvalidError('Invalid Ed25519 Secret Seed: {}'.format(data))

    @staticmethod
    def is_valid_ed25519_secret_seed(seed: str):
        return is_valid('ed25519_secret_seed', seed)

    @staticmethod
    def encode_pre_auth_tx(data: bytes) -> str:
        return encode_check('pre_auth_tx', data)

    @staticmethod
    def decode_pre_auth_tx(data: str) -> bytes:
        return decode_check('pre_auth_tx', data)

    @staticmethod
    def encode_sha256_hash(data: bytes) -> str:
        return encode_check('sha256_hash', data)

    @staticmethod
    def decode_sha256_hash(data: str) -> bytes:
        return decode_check('sha256_hash', data)


def decode_check(version_byte_name: str, encoded: str) -> bytes:
    encoded = _bytes_from_decode_data(encoded)

    try:
        decoded = base64.b32decode(encoded)
    except binascii.Error:
        raise Exception('Incorrect padding.')

    if encoded != base64.b32encode(decoded):  # Is that even possible?
        raise Exception('Invalid encoded bytes.')

    version_byte = decoded[0:1]
    payload = decoded[0:-2]
    data = decoded[1:-2]
    checksum = decoded[-2:]

    try:
        expected_version = _version_bytes[version_byte_name]
    except KeyError:
        raise KeyError('{} is not a valid version byte name. expected one of "ed25519_public_key", '
                       '"ed25519_secret_seed", "pre_auth_tx", "sha256_hash"'.format(version_byte_name))  # TODO

    if version_byte != expected_version:
        raise Exception('Invalid version byte. Expected {}, got {}'.format(
            str(expected_version), str(version_byte)))

    expected_checksum = _calculate_checksum(payload)
    if expected_checksum != checksum:
        raise Exception('Invalid checksum')

    return data


def encode_check(version_byte_name: str, data: bytes) -> str:
    if data is None:
        raise TypeError("cannot encode null data")

    try:
        version_byte = _version_bytes[version_byte_name]
    except KeyError:
        raise KeyError('{} is not a valid version byte name. expected one of "ed25519_public_key", '
                       '"ed25519_secret_seed", "pre_auth_tx", "sha256_hash"'.format(version_byte_name))  # TODO

    payload = version_byte + data
    crc = _calculate_checksum(payload)
    return base64.b32encode(payload + crc).decode('utf-8')


def is_valid(version_byte_name: str, encoded: str) -> bool:
    if encoded and len(encoded) != 56:
        return False
    try:
        decoded = decode_check(version_byte_name, encoded)
        # if len(decoded) != 32:
        #     return False
    except Exception as e:  # TODO: log
        return False
    return True


def _bytes_from_decode_data(s):
    """copy from base64._bytes_from_decode_data
    """
    bytes_types = (bytes, bytearray)  # Types acceptable as binary data
    if isinstance(s, str):
        try:
            return s.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')
    if isinstance(s, bytes_types):
        return s
    try:
        return memoryview(s).tobytes()
    except TypeError:
        raise TypeError("argument should be a bytes-like object or ASCII "
                        "string, not %r" % s.__class__.__name__) from None


def _calculate_checksum(payload):
    # This code calculates CRC16-XModem checksum of payload
    checksum = crc16xmodem(payload)
    # Ensure that the checksum is in LSB order.
    checksum = struct.pack('<H', checksum)
    return checksum
