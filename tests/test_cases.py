# coding:utf-8
# For use with nosetests

import base64

from stellar_base.memo import *
from stellar_base.operation import *
from stellar_base.transaction import Transaction
from stellar_base.keypair import Keypair
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.asset import Asset

SOURCE = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
SEED = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'
DESTINATION = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
SEQ_NUM = 1
FEE = 100
AMOUNT= 10 * 10**6

def bip(envelope=False): # Base64-ip, like zip.
	assert envelope
	from stellar_base.stellarxdr import StellarXDR_pack as Xdr
	x = Xdr.STELLARXDRPacker()
	x.pack_TransactionEnvelope(envelope.to_xdr_object())
	return base64.b64encode(x.get_buffer())
def do_single_signer(op, tx_opts):

	tx = Transaction( source=SOURCE, opts=tx_opts)
	tx.add_operation( operation=op )
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
	return True

def test_op_createAccount_minimal_defaults():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAJiWgAAAAAAAAAABzT4TYwAAAEBBR+eUTPqpyTBLiNMudfSl2AN+oZL9/yp0KE9SyYeIzM2Y7yQH+dGNlwz5PMaaCEGAD+82IZkAPSDyunElc+EP'
	assert(result == do_single_signer(
		op=CreateAccount({
			'destination': DESTINATION,
			'starting_balance': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_createAccount_minimal_placeholders():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAAAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAJiWgAAAAAAAAAABzT4TYwAAAEBBR+eUTPqpyTBLiNMudfSl2AN+oZL9/yp0KE9SyYeIzM2Y7yQH+dGNlwz5PMaaCEGAD+82IZkAPSDyunElc+EP'
	assert(result == do_single_signer(
		op=CreateAccount({
			'destination': DESTINATION,
			'starting_balance': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))	

def test_op_payment_minimal_defaults():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
	assert(result == do_single_signer(
		op=Payment({
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_payment_minimal_placeholders():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABAzEdbP2ISsB9pDqmIRPt6WEK0GkVOgAEljnelNQjNpDig6A60+jMtveQjdCocL13GwVbO1B8VBXgQdlAobs0fDg=='
	assert(result == do_single_signer(
		op=Payment({
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))
def test_op_payment_short_asset():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAABVVNENAAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQFosJrUliRYKU1jdh/po5Nyi9wiNiJ5Ve76C7Lu/THLxUfe2YKlORKGZ+aBbVe7q8FooQRutmnzbZ5GfIJYeYAk='
	assert(result == do_single_signer(
		op=Payment({
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset('USD4', SOURCE),
			'amount': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))
def test_op_payment_long_asset():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAACU05BQ0tTNzg5QUJDAAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAAACYloAAAAAAAAAAAc0+E2MAAABAE+vwbVK5XVhw3z8qqKW0P6HL7zZdgOSjSl6DVWQicmp2a0un8evaCUDXexCXxUx+UBf/HlowHJdLaXFKmRy5AQ=='
	assert(result == do_single_signer(
		op=Payment({
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset('SNACKS789ABC', SOURCE),
			'amount': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))
def test_op_payment_textMemo_ascii():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAHdGVzdGluZwAAAAABAAAAAQAAAADTUozdcK3X4scPuMNM5il78cYpIOhCjIvUltQ5zT4TYwAAAAEAAAAAra4WiCvFr/vydTiUbSQF0HwkqErP8wc6BUQav3qSQI4AAAAAAAAAAACYloAAAAAAAAAAAc0+E2MAAABApJRB7KqhymuVzBcsit9QUZsFfk2DwSwwp1CSI6qI1scogBoNchw32lJzJqDDXXUmoi3blG8XxNGkzdFk0BDDAA=='
	assert(result == do_single_signer(
		op=Payment({
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': TextMemo('testing'),
			'fee': FEE,
		},
	))
def test_op_payment_textMemo_unicode():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAEAAAAMdMSTxaF0xKvFhsSjAAAAAQAAAAEAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2MAAAABAAAAAK2uFogrxa/78nU4lG0kBdB8JKhKz/MHOgVEGr96kkCOAAAAAAAAAAAAmJaAAAAAAAAAAAHNPhNjAAAAQJkdyCjp7w6UzRxaaHqg9lrIfWJlEyvEga2ZNhbJ7w1NZxwkqiI7AG2oJg0dg91m83W1ZP85VPOf4iDkIAI2YAs='
	assert(result == do_single_signer(
		op=Payment({
			'source': SOURCE,
			'destination': DESTINATION,
			'asset': Asset.native(),
			'amount': AMOUNT,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': TextMemo('tēštīņģ'),
			'fee': FEE,
		},
	))

def test_op_pathPayment_min_defaults():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=PathPayment({
			'source': SOURCE,
			'destination': DESTINATION,
			'send_asset': Asset.native(),
			'dest_asset': Asset.native(),
			'send_max': AMOUNT,
			'dest_amount': AMOUNT,
			'path': [],
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_pathPayment_min_placeholders():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=PathPayment({
			'source': SOURCE,
			'destination': DESTINATION,
			'send_asset': Asset.native(),
			'dest_asset': Asset.native(),
			'send_max': AMOUNT,
			'dest_amount': AMOUNT,
			'path': [],
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_op_manageOffer_min_defaults():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=ManageOffer({
			'selling': Asset('beer', SOURCE),
			'buying': Asset('beer', DESTINATION),
			'amount': 100,
			'n': 9,
			'd': 8,
			'offerId': 1,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_manageOffer_min_placeholders():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=ManageOffer({
			'selling': Asset('beer', SOURCE),
			'buying': Asset('beer', DESTINATION),
			'amount': 100,
			'n': 9,
			'd': 8,
			'offerId': 1,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_op_createPassiveOffer_min_defaults():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=CreatePassiveOffer({
			'selling': Asset('beer', SOURCE),
			'buying': Asset('beer', DESTINATION),
			'amount': 100,
			'n': 9,
			'd': 8,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_createPassiveOffer_min_placeholders():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=CreatePassiveOffer({
			'selling': Asset('beer', SOURCE),
			'buying': Asset('beer', DESTINATION),
			'amount': 100,
			'n': 9,
			'd': 8,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_op_SetOptions_empty_defaults():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=SetOptions({
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))
def test_op_SetOptions_emptly_placeholders():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=SetOptions({
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_op_changeTrust_min_defaults():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQL0R9eOS0qesc+HHKQoHMjFUJWvzeQOy+u/7HBHNooo37AOaG85y9jyNoa1D4EduroZmK8vCfCF0V3rn5o9CpgA='
	assert(result == do_single_signer(
		op=ChangeTrust({
			'asset': Asset('beer', DESTINATION),
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_changeTrust_min_placeholders():
	result = b'AAAAANNSjN1wrdfixw+4w0zmKXvxxikg6EKMi9SW1DnNPhNjAAAAZAAAAAAAAAACAAAAAAAAAAAAAAABAAAAAAAAAAYAAAABYmVlcgAAAACtrhaIK8Wv+/J1OJRtJAXQfCSoSs/zBzoFRBq/epJAjn//////////AAAAAAAAAAHNPhNjAAAAQL0R9eOS0qesc+HHKQoHMjFUJWvzeQOy+u/7HBHNooo37AOaG85y9jyNoa1D4EduroZmK8vCfCF0V3rn5o9CpgA='
	assert(result == do_single_signer(
		op=ChangeTrust({
			'asset': Asset('beer', DESTINATION),
			'amount': 100,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_op_allowTrust_min_defaults():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=AllowTrust({
			'trustor': DESTINATION,
			'asset_code': 'beer',
			'authorize': True,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
		},
	))
def test_op_allowTrust_min_placeholders():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=AllowTrust({
			'trustor': DESTINATION,
			'asset_code': 'beer',
			'authorize': True,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))

def test_op_accountMerge_min_defaults():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=AccountMerge({
			'destination': DESTINATION,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))
def test_op_accountMerge_min_placeholders():
	result = b'' # TODO
	assert(result == do_single_signer(
		op=AccountMerge({
			'destination': DESTINATION,
		}),
		tx_opts={
			'seqNum': SEQ_NUM,
			'timeBounds': [],
			'memo': NoneMemo(),
			'fee': FEE,
		},
	))
