# coding:utf-8
# For use with nosetests

import sys
sys.path.append('src')
sys.path.append('src/lib/stellar-sdk-py')

SOURCE = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
SEED = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
DESTINATION = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
SEQ_NUM = 1 # Remember to increment it
FEE = 100
AMOUNT= 10 * 10**6

def bip(envelope=False): # Base64-ip, like zip.
	assert envelope
	import base64
	from stellar_base.stellarxdr import StellarXDR_pack as Xdr
	x = Xdr.STELLARXDRPacker()
	x.pack_TransactionEnvelope(envelope.to_xdr_object())
	return base64.b64encode(x.get_buffer())

def do_single_signer(operation_opts=False, tx_opts=False):
	assert operation_opts and tx_opts
	from stellar_base.operation import Payment
	from stellar_base.transaction import Transaction
	from stellar_base.keypair import Keypair
	from stellar_base.transaction_envelope import TransactionEnvelope as Te

	operation = Payment( opts=operation_opts)
	tx = Transaction( source=SOURCE, opts=tx_opts)
	tx.add_operation( operation=operation )
	envelope = Te( tx=tx, opts={"network_id": "TESTNET"} )
	signer = Keypair.from_seed( seed=SEED )
	envelope.sign( keypair=signer )
	envelope_b64 = bip(envelope)

	print(envelope_b64)
	return envelope_b64

def setup_module(module):
	pass

def teardown_module(module):
	pass

def my_setup_function():
	pass
 
def my_teardown_function():
	pass

def test_load_module():
	import stellar_base
	return True

def test_minimal_defaults():
	from stellar_base.asset import Asset

	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
	assert(result == do_single_signer(
		operation_opts={
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		},
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))

def test_minimal_placeholders():
	from stellar_base.asset import Asset
	from stellar_base.memo import NoneMemo

	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
	assert(result == do_single_signer(
		operation_opts={
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		},
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_short_asset():
	from stellar_base.asset import Asset
	from stellar_base.memo import NoneMemo

	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABVVNENAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQFosJrUliRYKU1jdh/po5Nyi9wiNiJ5Ve76C7Lu/THLxUfe2YKlORKGZ+aBbVe7q8FooQRutmnzbZ5GfIJYeYAk='

	assert(result == do_single_signer(
		operation_opts={
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset('USD4', SOURCE),
			'amount': AMOUNT,
		},
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_long_asset():
	from stellar_base.asset import Asset
	from stellar_base.memo import NoneMemo

	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACU05BQ0tTNzg5QUJDAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAAACYloAAAAAAAAAAAc0+E2MAAABAE+vwbVK5XVhw3z8qqKW0P6HL7zZdgOSjSl6DVWQicmp2a0un8evaCUDXexCXxUx+UBf/HlowHJdLaXFKmRy5AQ=='
	assert(result == do_single_signer(
		operation_opts={
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset('SNACKS789ABC', SOURCE),
			'amount': AMOUNT,
		},
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_textMemo_ascii():
	from stellar_base.asset import Asset
	from stellar_base.memo import TextMemo

	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAHdGVzdGluZwAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABApJRB7KqhymuVzBcsit9QUZsFfk2DwSwwp1CSI6qI1scogBoNchw32lJzJqDDXXUmoi3blG8XxNGkzdFk0BDDAA=='
	assert(result == do_single_signer(
		operation_opts={
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		},
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': TextMemo('testing'),
			'fee': FEE,
		},
	))

def test_textMemo_unicode():
	from stellar_base.asset import Asset
	from stellar_base.memo import TextMemo

	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAMdMSTxaF0xKvFhsSjAAAAAQAAAAEAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAABAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAAAAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQJkdyCjp7w6UzRxaaHqg9lrIfWJlEyvEga2ZNhbJ7w1NZxwkqiI7AG2oJg0dg91m83W1ZP85VPOf4iDkIAI2YAs='
	assert(result == do_single_signer(
		operation_opts={
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		},
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': TextMemo('tēštīņģ'),
			'fee': FEE,
		},
	))
