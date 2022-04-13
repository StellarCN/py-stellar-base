# This example shows how to use the new features introduced in Protocol 19.
import binascii

from stellar_sdk import (
    TransactionBuilder,
    Network,
    Server,
    Keypair,
    SignedPayloadSigner,
    Account,
)

kp1 = Keypair.from_secret("SAT4KQ4PSHSHXDCJQRE46OHLKDOG6M4ZEFHTKVR3QIPHFZ56TELZNFE5")
kp2 = Keypair.from_secret("SDHKS4E4ZJ4ADKQQAILLF6ZU7B7RON2RNSKHWLEFWOPSVEJVNM3A4QVY")
kp3 = Keypair.from_secret("SDE2526FIFPQOSY3QDTR5GP722YGZJ4JL3IHYWKHOJRFMN72DUSHT6YS")

server = Server(horizon_url="https://horizon-testnet.stellar.org")
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE
base_fee = 100

kp1_source = Account(kp1.public_key, 8689178401319000)

tx = (
    TransactionBuilder(kp1_source, network_passphrase, base_fee)
    .append_bump_sequence_op(0)
    .set_timeout(300)
    .set_ledger_bounds(2798490, 0)
    .set_min_sequence_number(8689178401308600)
    .set_min_sequence_ledger_gap(30)
    .set_min_sequence_age(60 * 5)
    .add_extra_signer(kp2.public_key)
    .add_extra_signer(
        SignedPayloadSigner(
            kp3.public_key,
            binascii.unhexlify(
                "0102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f20"
            ),
        )
    )
    .build()
)

tx.sign(kp1)
tx.sign(kp2)
tx.sign_extra_signers_payload(kp3)

resp = server.submit_transaction(tx)
print(resp)
