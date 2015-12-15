# coding:utf-8
import sys
sys.path.append('.')

from stellar_base.operation import Payment
from stellar_base.asset import Asset
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.keypair import Keypair
from stellar_base.memo import *

url = 'https://horizon-testnet.stellar.org'

# Only for sample 'requests' and 'simplejson' are required.
import requests
import simplejson as json

def newAccount(creator=False):
	kp = Keypair.random()
	r = requests.get(url + '/friendbot?addr=' + kp.address().decode('ascii')) # Get 1000 lumens
	assert 'hash' in json.loads(r.text)
	return {
		'address': kp.address().decode('ascii'),
		'seed': kp.seed().decode('ascii')
	}

def packer(envelope=False):
	import base64
	from stellar_base.stellarxdr import StellarXDR_pack as Xdr
	x = Xdr.STELLARXDRPacker()
	x.pack_TransactionEnvelope(envelope.to_xdr_object())
	return base64.b64encode(x.get_buffer())

anna = newAccount()
bob = newAccount()
print('Anna: ', json.dumps(anna, sort_keys=True, indent=4 * ' '))
print('Bob: ', json.dumps(bob, sort_keys=True, indent=4 * ' '))

operation = Payment({
	'source': anna['address'],
	'destination': bob['address'],
	'asset': Asset.native(),
	'amount': 10*10**6,
})
tx = Transaction(
	source=anna['address'],
	opts={
		'sequence': json.loads(requests.get(url+'/accounts/'+anna['address']).text)['sequence'],
		'timeBounds': [],
		'memo': NoneMemo(),
		'fee': 100,
		'operations': [
			operation,
		],
	},
)
envelope = Te(tx=tx, opts={"network_id": "TESTNET"})
envelope.sign(Keypair.from_seed(anna['seed']))

print('Tx: ', json.dumps(json.loads(requests.post(
	url=url+'/transactions',
	data={
		'tx': packer(envelope).decode('ascii')
	}
).text), sort_keys=True, indent=4 * ' '))
