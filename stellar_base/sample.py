# coding:utf-8
import requests
import simplejson as json
from urllib.parse import urlencode

import base64
import os, sys
from stellar_base.stellarxdr import StellarXDR_pack as Xdr
from stellar_base.operation import PaymentOperation
from stellar_base.asset import Asset
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.keypair import Keypair
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# base info
seqNum = 2094810169081858 # Remember to increment it
address = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
secret = 'SAHPFH5CXKRMFDXEIHO6QATHJCX6PREBLCSFKYXTTCDDV6FJ3FXX4POT'

# input
destination = 'GCW24FUIFPC2767SOU4JI3JEAXIHYJFIJLH7GBZ2AVCBVP32SJAI53F5'
asset = Asset.native()
amount = 10000000

# process
opts = {'source': address, 'destination': destination, 'asset': asset, 'amount': amount}
operation = PaymentOperation(opts)

tx = Transaction(address, {'seqNum': seqNum, 'fee': 100})
tx.add_operation(operation)
envelope = Te(tx)
signer = Keypair.from_seed(secret)
envelope.sign(signer)
exo = envelope.to_xdr_object()
x = Xdr.STELLARXDRPacker()
x.pack_TransactionEnvelope(exo)
ex = x.get_buffer()
ex = base64.b64encode(ex)

url = "https://horizon-testnet.stellar.org/transactions"
r = requests.post(url, data={'tx': ex.decode('ascii')})
print(r.text)
