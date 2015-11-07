import utils

__b58chars = 'gsphnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCr65jkm8oFqi1tuvAxyz'
__b58base = len(__b58chars)

__b58inv = {}
for i, c in enumerate(__b58chars):
	__b58inv[c] = i


def encode(v):

	long_value = int(v.encode("hex_codec"), 16)

	result = ''
	while long_value >= __b58base:
		long_value, mod = divmod(long_value, __b58base)
		result += __b58chars[mod]
	result += __b58chars[long_value]

	z = 0
	while v[z] == '\0':
		z += 1

	return __b58chars[0]*z + result[::-1]


def decode(v):

	#	count number of leading zeroes
	z = 0
	while v[z] == __b58chars[0]:
		z += 1

	long_value = 0
	for c in v:
		long_value *= __b58base
		long_value += __b58inv[c]

	result = utils.int_to_bytes(long_value)
	result = z * '\0' + result
	return result
