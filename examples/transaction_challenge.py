"""
This example demonstrates how the client interacts with the server as described in SEP-10.

See: https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0010.md
"""
from stellar_sdk import Keypair, Network, Server, TransactionBuilder
from stellar_sdk.exceptions import NotFoundError
from stellar_sdk.sep.exceptions import InvalidSep10ChallengeError
from stellar_sdk.sep.stellar_web_authentication import (
    build_challenge_transaction,
    read_challenge_transaction,
    verify_challenge_transaction_signed_by_client_master_key,
    verify_challenge_transaction_threshold,
)

server_keypair = Keypair.from_secret(
    "SBGCNEOQGECW5R4A55C26ZFS736IONKCHY5PPPSFZVXSJSU63MWNM4K6"
)
client_master_keypair = Keypair.from_secret(
    "SDWZHXKWSHTQ2YGPT6YQQSOJWJX5JX2IEU7KOLGQ2XEJEECIQHUU3RMR"
)
client_signer_keypair1 = Keypair.from_secret(
    "SCKJFEF2H767XINUY5YFBORUO7AAWOAXSTQ2B2YHSI6N4UF23HFV42I7"
)
client_signer_keypair2 = Keypair.from_secret(
    "SCE2JBZ6FKPTQ5LM4X4NIZOOZPIC5DXVG6VP2TKSBZCQAGXABJV55IN5"
)

server = Server("https://horizon-testnet.stellar.org")
home_domain = "example.com"
web_auth_domain = "auth.example.com"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE


def setup_multisig():
    client_master_account = server.load_account(client_master_keypair.public_key)
    te = (
        TransactionBuilder(client_master_account, network_passphrase)
        .append_ed25519_public_key_signer(client_signer_keypair1.public_key, 40)
        .append_ed25519_public_key_signer(client_signer_keypair2.public_key, 60)
        .append_set_options_op(
            master_weight=0, low_threshold=1, med_threshold=10, high_threshold=100
        )
        .build()
    )
    te.sign(client_master_keypair)
    resp = server.submit_transaction(te)
    print(resp)


def example_verify_challenge_tx_threshold():
    # Server builds challenge transaction
    challenge_tx = build_challenge_transaction(
        server_keypair.secret,
        client_master_keypair.public_key,
        home_domain,
        web_auth_domain,
        network_passphrase,
        300,
    )

    # Client reads and signs challenge transaction
    parsed_challenge_tx = read_challenge_transaction(
        challenge_tx,
        server_keypair.public_key,
        home_domain,
        web_auth_domain,
        network_passphrase,
    )
    tx, tx_client_account_id = (
        parsed_challenge_tx.transaction,
        parsed_challenge_tx.client_account_id,
    )
    if tx_client_account_id != client_master_keypair.public_key:
        print("Error: challenge tx is not for expected client account")
        return
    tx.sign(client_signer_keypair1)
    tx.sign(client_signer_keypair2)
    signed_challenge_tx = tx.to_xdr()

    # Server verifies signed challenge transaction
    read_challenge_transaction(
        challenge_tx,
        server_keypair.public_key,
        home_domain,
        web_auth_domain,
        network_passphrase,
    )
    client_account_exists = False
    horizon_client_account = None
    try:
        horizon_client_account = server.load_account(client_master_keypair.public_key)
        client_account_exists = True
    except NotFoundError:
        print("Account does not exist, use master key to verify")

    if client_account_exists:
        # gets list of signers from account
        signers = horizon_client_account.load_ed25519_public_key_signers()
        # chooses the threshold to require: low, med or high
        threshold = horizon_client_account.thresholds.med_threshold
        try:
            signers_found = verify_challenge_transaction_threshold(
                signed_challenge_tx,
                server_keypair.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
                threshold,
                signers,
            )
        except InvalidSep10ChallengeError as e:
            print("You should handle possible exceptions:")
            print(e)
            return

        print("Client Signers Verified:")
        for signer in signers_found:
            print(f"Signer: {signer.account_id}, weight: {signer.weight}")
    else:
        # verifies that master key has signed challenge transaction
        try:
            verify_challenge_transaction_signed_by_client_master_key(
                signed_challenge_tx,
                server_keypair.public_key,
                home_domain,
                web_auth_domain,
                network_passphrase,
            )
            print("Client Master Key Verified.")
        except InvalidSep10ChallengeError as e:
            print("You should handle possible exceptions:")
            print(e)


if __name__ == "__main__":
    setup_multisig()
    example_verify_challenge_tx_threshold()
