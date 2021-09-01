"""
A fee-bump transaction enables any account to pay the fee for an existing transaction
without the need to re-sign the existing transaction or manage sequence numbers.
They’re useful if you need to increase the fee on a pre-signed transaction, or
if you want to build a service that covers user fees. Like a regular transaction,
these are submitted to the /transactions endpoint. Unlike a regular transaction,
however, which contains 1-100 operations, a fee-bump transaction contains a single
transaction envelope.

See: https://developers.stellar.org/docs/glossary/fee-bumps/
"""
import pprint

from stellar_sdk import Keypair, Network, Server, TransactionBuilder, Asset
from stellar_sdk.exceptions import BadRequestError

horizon_url = "https://horizon-testnet.stellar.org/"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

fee_source_keypair = Keypair.from_secret(
    "SASZKBDB6PFHXN6LRH4NQNTRGLGDTI3PSUVIKMZMLTYYBB7NDVMA6DSL"
)
inner_source_keypair = Keypair.from_secret(
    "SC5O7VZUXDJ6JBDSZ74DSERXL7W3Y5LTOAMRF7RQRL3TAGAPS7LUVG3L"
)
destination_address = "GBVKI23OQZCANDUZ2SI7XU7W6ICYKYT74JBXDD2CYRDAFZHZNRPASSQK"

server = Server(horizon_url=horizon_url)
inner_account = server.load_account(inner_source_keypair)

inner_tx = (
    TransactionBuilder(
        source_account=inner_account,
        network_passphrase=network_passphrase,
        base_fee=50,
        v1=True,
    )
    .append_payment_op(
        destination=destination_address, amount="100", asset=Asset.native()
    )
    .build()
)
inner_tx.sign(inner_source_keypair)

try:
    # This transaction will fail.
    tx_insufficient_fee_resp = server.submit_transaction(inner_tx)
except BadRequestError as e:
    print(e)

fee_bump_tx = TransactionBuilder.build_fee_bump_transaction(
    fee_source=fee_source_keypair,
    base_fee=200,
    inner_transaction_envelope=inner_tx,
    network_passphrase=network_passphrase,
)
fee_bump_tx.sign(fee_source_keypair)
response = server.submit_transaction(fee_bump_tx)
pprint.pprint(response)
