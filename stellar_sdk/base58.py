# coding: utf-8
'''Base58 encoding

Implementations of Base58 and Base58Check endcodings that are compatible
with the bitcoin network.
'''

# This module is based upon base58 snippets found scattered over many bitcoin
# tools written in python. From what I gather the original source is from a
# forum post by Gavin Andresen, so direct your praise to him.
# This module adds shiny packaging and support for python3.

__version__ = '0.2.2'

from hashlib import sha256

# 58 character alphabet used
alphabet = 'gsphnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCr65jkm8oFqi1tuvAxyz'

if bytes == str:  # python2
    iseq = lambda s: map(ord, s)
    bseq = lambda s: ''.join(map(chr, s))
    buffer = lambda s: s
else:  # python3
    iseq = lambda s: s
    bseq = bytes
    buffer = lambda s: s.buffer


def b58encode(v):
    """Encode a string using Base58"""

    origlen = len(v)
    v = v.lstrip(b'\0')
    newlen = len(v)

    p, acc = 1, 0
    for c in iseq(v[::-1]):
        acc += p * c
        p = p << 8

    result = ''
    while acc > 0:
        acc, mod = divmod(acc, 58)
        result += alphabet[mod]

    return (result + alphabet[0] * (origlen - newlen))[::-1]


def b58decode(v):
    """Decode a Base58 encoded string"""

    if not isinstance(v, str):
        v = v.decode('ascii')

    origlen = len(v)
    v = v.lstrip(alphabet[0])
    newlen = len(v)

    p, acc = 1, 0
    for c in v[::-1]:
        acc += p * alphabet.index(c)
        p *= 58

    result = []
    while acc > 0:
        acc, mod = divmod(acc, 256)
        result.append(mod)

    return (bseq(result) + b'\0' * (origlen - newlen))[::-1]


def b58encode_check(v):
    """Encode a string using Base58 with a 4 character checksum"""

    digest = sha256(sha256(v).digest()).digest()
    return b58encode(v + digest[:4])


def b58decode_check(v):
    """Decode and verify the checksum of a Base58 encoded string"""

    result = b58decode(v)
    result, check = result[:-4], result[-4:]
    digest = sha256(sha256(result).digest()).digest()

    if check != digest[:4]:
        raise ValueError("Invalid checksum")

    return result


def main():
    '''Base58 encode or decode FILE, or standard input, to standard output.'''

    import sys
    import argparse

    stdout = buffer(sys.stdout)

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        type=argparse.FileType('r'),
        default='-')
    parser.add_argument(
        '-d', '--decode', action='store_true', help='decode data')
    parser.add_argument(
        '-c',
        '--check',
        action='store_true',
        help='append a checksum before encoding')

    args = parser.parse_args()
    fun = {
        (False, False): b58encode,
        (False, True): b58encode_check,
        (True, False): b58decode,
        (True, True): b58decode_check
    }[(args.decode, args.check)]

    data = buffer(args.file).read().rstrip(b'\n')

    try:
        result = fun(data)
    except Exception as e:
        sys.exit(e)

    if not isinstance(result, bytes):
        result = result.encode('ascii')

    stdout.write(result)


if __name__ == '__main__':
    main()
