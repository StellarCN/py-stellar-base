# coding:utf-8

import base64
import binascii
import hashlib
import struct

import crc16

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    from pure25519 import ed25519_oop as ed25519
except:
    import ed25519
from .stellarxdr import Xdr
from fractions import Fraction
import numpy
from decimal import *

# Compatibility for Python 3.x that don't have unicode type
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


class BaseError(Exception):
    def __init__(self, msg):
        super(BaseError, self).__init__(msg)


class XdrLengthError(BaseError):
    pass


class SignatureExistError(BaseError):
    pass


class DecodeError(BaseError):
    pass


class AccountNotExistError(BaseError):
    pass


class NotValidParamError(BaseError):
    pass


def decode_check(version_byte_name, encoded):
    encoded = bytes_from_decode_data(encoded)

    try:
        decoded = base64.b32decode(encoded)
    except binascii.Error:
        raise DecodeError('Incorrect padding')
    except:
        raise

    if encoded != base64.b32encode(decoded):
        raise DecodeError('invalid encoded bytes')

    version_byte = decoded[0:1]
    payload = decoded[0:-2]
    data = decoded[1:-2]
    checksum = decoded[-2:]

    # raise KeyError
    expected_version = versionBytes[version_byte_name]
    if version_byte != expected_version:
        raise DecodeError(
                'invalid version byte. expected ' + str(expected_version) + ', got ' + str(version_byte))

    expected_checksum = calculate_checksum(payload)
    if expected_checksum != checksum:
        raise DecodeError('invalid checksum')

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


def best_rational_approximation(x):
    x = Decimal(x)
    INT32_MAX = Decimal(2147483647)
    a = None
    f = None
    fractions = numpy.array([[Decimal(0), Decimal(1)], [Decimal(1), Decimal(0)]])
    i = 2
    while True:
        if x > INT32_MAX:
            break
        a = x.to_integral_exact(rounding=ROUND_FLOOR)
        f = x - a
        h = a * fractions[i - 1][0] + fractions[i - 2][0]
        k = a * fractions[i - 1][1] + fractions[i - 2][1]
        if h > INT32_MAX or k > INT32_MAX:
            break
        fractions = numpy.vstack([fractions, [h, k]])
        if f.is_zero():
            break
        x = 1 / f
        i = i + 1
    n = fractions[len(fractions) - 1][0]
    d = fractions[len(fractions) - 1][1]
    if n.is_zero() or d.is_zero():
        raise Exception("Couldn't find approximation")
    return {'n': int(n), 'd': int(d)}


def division(n, d):
    return float(Fraction(n, d))
