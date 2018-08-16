from stellar_base.keypair import Keypair
from stellar_base.asset import Asset
from stellar_base.operation import Payment, SetOptions
from stellar_base.transaction import Transaction
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.memo import TextMemo
from stellar_base.horizon import horizon_testnet, horizon_livenet

alice_seed = 'SBUORYV26AZ3ULEEC5FQ4NKPVRO7MBAWTW26YKCDPPKFGMK7WAYNX4UN'
bob_address = 'GBZF7GQJXXHD3OL3B5IOUICFDYIATZZ3F3XQ7SOQ5PXLVQMDSOI5ACEE'

Alice = Keypair.from_seed(alice_seed)
horizon = horizon_testnet()  # for TESTNET
# horizon = horizon_livenet() # for LIVENET

# create op
payment_op = Payment(
    # source=Alice.address().decode(),
    destination=bob_address,
    asset=Asset('XLM'),
    amount='10.5')

set_home_domain_op = SetOptions(home_domain='fed.network')

# create a memo
msg = TextMemo('Buy yourself a beer!')

# get sequence of Alice
# Python 3
sequence = horizon.account(Alice.address().decode('utf-8')).get('sequence')
# Python 2
# sequence = horizon.account(Alice.address()).get('sequence')

operations = [payment_op, set_home_domain_op]
# construct Tx
tx = Transaction(
    source=Alice.address().decode(),
    sequence=int(sequence),
    # time_bounds = {'minTime': 1531000000, 'maxTime': 1531234600},
    memo=msg,
    fee=100 * len(operations),
    operations=operations,
)

# build envelope
envelope = Te(tx=tx, network_id="TESTNET")
# envelope = Te(tx=tx, network_id="PUBLIC") for LIVENET
# sign
envelope.sign(Alice)
# submit
xdr = envelope.xdr()
response = horizon.submit(xdr)
print(response)