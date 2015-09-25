# coding:utf-8

import sys
sys.path.append('') # the path
from stellar_base.stellarxdr import StellarXDR_pack as xdr
from stellar_base.operation import Operation
from stellar_base.asset import Asset
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelopo import TransactionEnvelope as TE
from stellar_base.keypair import KeyPair
import base64

#base info
seqNum = "34909494181888"
address = "GDVDKQFP665JAO7A2LSHNLQIUNYNAAIGJ6FYJVMG4DT3YJQQJSRBLQDG"
secret = 'SCVLSUGYEAUC4MVWJORB63JBMY2CEX6ATTJ5MXTENGD3IELUQF4F6HUB'
#input
destination='GBS43BF24ENNS3KPACUZVKK2VYPOZVBQO2CISGZ777RYGOPYC2FT6S3K'
asset=Asset.native()
amount=1000

#process
opts = {'source':address,'destination':destination,'asset':asset,'amount':amount}
operation = Operation.payment(opts)


opts = {'seqNum':seqNum}

tx = Transaction(address,opts)
tx.addOperation(operation)
envelope = TE(tx)
signer = KeyPair.fromSeed(secret)
envelope.sign(signer)
exo = envelope.toXDRObject()
x = xdr.STELLARXDRPacker()
x.pack_TransactionEnvelope(exo)
ex = x.get_buffer()
ex = base64.b64encode(ex)
print(ex)