# coding: utf-8

import binascii
import base64
import crc16
import struct
versionBytes = {'account_id': binascii.a2b_hex('30'), 'seed': binascii.a2b_hex('90')}


def decode_check(version_byte_name, encoded):
    # TODO 一直传递的是bytes,将string转为bytes，解决base64依赖
    # if type(encoded) != bytes:
    encoded = base64._bytes_from_decode_data(encoded)

    if encoded != base64.b32encode(base64.b32decode(encoded)):
        raise Exception('invalid encoded bytes')

    # raise Error
    decoded = memoryview(base64.b32decode(encoded))

    version_byte = bytes(decoded[0:1])
    payload = bytes(decoded[0:-2])
    data = bytes(decoded[1:-2])
    checksum = bytes(decoded[-2:])

    # raise KeyError
    expected_version = versionBytes[version_byte_name]
    if version_byte != expected_version:
        raise Exception('invalid version byte. expected ' + str(expected_version)+', got '+str(version_byte))
   
    expected_checksum = calculate_checksum(payload)
    if expected_checksum != checksum:
        raise Exception('invalid checksum')
  
    return data


def encode_check(version_byte_name, data):
    if data is None:
        raise Exception("cannot encode null data")

    # raise KerError
    version_byte = versionBytes[version_byte_name]
    payload = version_byte+data
    crc = calculate_checksum(payload)
    return base64.b32encode(payload+crc)


def calculate_checksum(payload):
    # This code calculates CRC16-XModem checksum of payload
    checksum = crc16.crc16xmodem(payload)
    checksum = struct.pack('H', checksum)
    return checksum
