# coding:utf-8

import binascii
import base64
import crc16
import struct
import hashlib
# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pure25519 import ed25519_oop as ed25519
except:
    import ed25519
from .stellarxdr import StellarXDR_pack as Xdr

# Compatibility for Python 3.x that dont have unicode type
try:
    type(unicode)
except NameError:
    unicode = str

bytes_types = (bytes, bytearray)  # Types acceptable as binary data
versionBytes = {'account': binascii.a2b_hex('30'), 'seed': binascii.a2b_hex('90')}

def suppress_context(exc):
    """ Python 2 compatible version of raise from None """
    exc.__context__ = None
    return exc

def xdr_hash(data):
    return hashlib.sha256(data).digest()


def account_xdr_object(account):
    public_key = decode_check('account', account)
    axo = Xdr.types.PublicKey(Xdr.const.KEY_TYPE_ED25519, public_key)
    return axo


def bytes_from_decode_data(s):
    """copy from base64._bytes_from_decode_data
    """
    if isinstance(s, (str, unicode)):
        try:
            return s.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')
    if isinstance(s, bytes_types):
        return s
    try:
        return memoryview(s).tobytes()
    except TypeError:
        raise suppress_context(TypeError("argument should be a bytes-like "
                                         "object or ASCII string, not %r" %
                                         s.__class__.__name__))


class XdrLengthError(Exception):
    def __init__(self, msg):
        super(XdrLengthError, self).__init__(msg)


def decode_check(version_byte_name, encoded):
    encoded = bytes_from_decode_data(encoded)

    if encoded != base64.b32encode(base64.b32decode(encoded)):
        raise Exception('invalid encoded bytes')

    decoded = base64.b32decode(encoded)
    version_byte = decoded[0:1]
    payload = decoded[0:-2]
    data = decoded[1:-2]
    checksum = decoded[-2:]

    # raise KeyError
    expected_version = versionBytes[version_byte_name]
    if version_byte != expected_version:
        raise XdrLengthError(
            'invalid version byte. expected ' + str(expected_version) + ', got ' + str(version_byte))

    expected_checksum = calculate_checksum(payload)
    if expected_checksum != checksum:
        raise Exception('invalid checksum')

    return data


def encode_check(version_byte_name, data):
    if data is None:
        raise Exception("cannot encode null data")

    # raise KerError
    version_byte = versionBytes[version_byte_name]
    payload = version_byte + data
    crc = calculate_checksum(payload)
    return base64.b32encode(payload + crc)


def calculate_checksum(payload):
    # This code calculates CRC16-XModem checksum of payload
    checksum = crc16.crc16xmodem(payload)
    checksum = struct.pack('H', checksum)
    return checksum
