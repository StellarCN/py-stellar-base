# coding: utf-8

import binascii
import base64
import crc16
import struct
versionBytes = {'accountId': binascii.a2b_hex('30'), 'seed': binascii.a2b_hex('90')}


def decodeCheck(versionByteName, encoded):
    # TODO 一直传递的是bytes,将string转为bytes，解决base64依赖
    # if type(encoded) != bytes:
    encoded = base64._bytes_from_decode_data(encoded)

    if encoded != base64.b32encode(base64.b32decode(encoded)):
        raise Exception('invalid encoded bytes')

    # raise Error
    decoded = memoryview(base64.b32decode(encoded))

    versionByte = bytes(decoded[0:1])
    payload = bytes(decoded[0:-2])
    data = bytes(decoded[1:-2])
    checksum = bytes(decoded[-2:])

    # raise KeyError
    expectedVersion = versionBytes[versionByteName]
    if versionByte != expectedVersion:
        raise Exception('invalid version byte. expected '+ str(expectedVersion)+', got '+str(versionByte))
   
    expectedChecksum = calculateChecksum(payload)
    if expectedChecksum != checksum:
        raise Exception('invalid checksum')
  
    return data


def encodeCheck(versionByteName, data):
    if data is None:
        raise Exception("cannot encode null data")

    # raise KerError
    versionByte = versionBytes[versionByteName]
    payload = versionByte+data
    crc = calculateChecksum(payload)   
    return base64.b32encode(payload+crc)


def calculateChecksum(payload) :
    # This code calculates CRC16-XModem checksum of payload
    checksum = crc16.crc16xmodem(payload)
    checksum = struct.pack('H', checksum)
    return checksum
