"""This example demonstrates CAP-71 delegated authorization (Protocol 27+).

A modular account contract verifies no signature of its own. Instead, its
``__check_auth`` reads the delegate signers attached to the authorization entry
and forwards the authorization to each of them. Here the delegates are two
classic Stellar accounts, each signing with the default account signature.

Simulation only records a plain ``ADDRESS_V2`` entry for the modular account,
so we wrap it into a ``SOROBAN_CREDENTIALS_ADDRESS_WITH_DELEGATES`` entry with
:func:`stellar_sdk.auth.build_with_delegates_entry`, let each delegate sign it,
and simulate the signed transaction again to get the final footprint.

Contracts used:
- https://github.com/stellar/soroban-examples/tree/main/modular_account
  (deployed with both delegate accounts below as its ``signers``)
- https://github.com/stellar/soroban-examples/tree/main/auth

See https://github.com/stellar/stellar-protocol/blob/master/core/cap-0071.md
"""

from stellar_sdk import (
    InvokeHostFunction,
    Keypair,
    Network,
    SorobanServer,
    TransactionBuilder,
    scval,
)
from stellar_sdk import xdr as stellar_xdr
from stellar_sdk.auth import (
    DelegateSignature,
    authorize_entry,
    build_with_delegates_entry,
)
from stellar_sdk.soroban_rpc import GetTransactionStatus, SendTransactionStatus

rpc_server_url = "https://soroban-testnet.stellar.org:443"
network_passphrase = Network.TESTNET_NETWORK_PASSPHRASE

# https://github.com/stellar/soroban-examples/tree/main/modular_account
modular_account_id = "CCIOMSEBRNXAPWR7VPLU7N6FPEI6HTNX23GXJEUMVF3GRL7YLBMC2FID"
# https://github.com/stellar/soroban-examples/tree/main/auth
auth_contract_id = "CBFGVCGZXKCT6WRCGAQNGLYFJCFWHAV42XVT3OUJSHIENRHUYSH577SB"

tx_submitter_kp = Keypair.from_secret(
    "SAAPYAPTTRZMCUZFPG3G66V4ZMHTK4TWA6NS7U4F7Z3IMUD52EK4DDEV"
)
# The signers registered in the modular account's constructor. Each one must be
# an existing account on the network.
delegate_kps = [
    Keypair.from_secret("SDFGVYMAM6GR4ZBVO2ICEHUD7CYLE3ZQEDGFGBCL7Q7ELM46I2F6JEV2"),
    Keypair.from_secret("SCFBVA23LWXCIQZSYBKJQUYT42X3CY4GOE24PB3AE6Q3HDS43WTLQMNT"),
]

server = SorobanServer(rpc_server_url)
source = server.load_account(tx_submitter_kp.public_key)

# `increment` calls `user.require_auth()`, with the modular account as `user`.
tx = (
    TransactionBuilder(source, network_passphrase, base_fee=100)
    .set_timeout(300)
    .append_invoke_contract_function_op(
        contract_id=auth_contract_id,
        function_name="increment",
        parameters=[scval.to_address(modular_account_id), scval.to_uint32(10)],
    )
    .build()
)

# The simulation records one ADDRESS_V2 entry for the modular account.
simulation = server.simulate_transaction(tx)
if simulation.error:
    raise RuntimeError(f"Simulation failed: {simulation.error}")
assert simulation.results is not None and simulation.results[0].auth is not None
entry = stellar_xdr.SorobanAuthorizationEntry.from_xdr(simulation.results[0].auth[0])

# Every signer of a delegated entry commits to the same expiration ledger.
valid_until_ledger_sequence = simulation.latest_ledger + 100

# The modular account carries no signature of its own (the top-level signature
# stays `scvVoid`); it authorizes through its delegates.
entry = build_with_delegates_entry(
    entry,
    valid_until_ledger_sequence,
    [DelegateSignature(kp.public_key) for kp in delegate_kps],
)
# Each delegate signs the same payload, bound to the modular account's address,
# and the signature is written to its own delegate node.
for kp in delegate_kps:
    entry = authorize_entry(
        entry,
        kp,
        valid_until_ledger_sequence,
        network_passphrase,
        for_address=kp.public_key,
    )

op = tx.transaction.operations[0]
assert isinstance(op, InvokeHostFunction)
op.auth = [entry]

# Simulate again with the signed entry, so the footprint and resources cover
# the modular account's `__check_auth` and the delegates' verification.
# prepare_transaction keeps op.auth because it is already populated.
tx = server.prepare_transaction(tx)
tx.sign(tx_submitter_kp)
print(f"Signed XDR:\n{tx.to_xdr()}")

send_response = server.send_transaction(tx)
if send_response.status != SendTransactionStatus.PENDING:
    raise RuntimeError(f"Failed to send transaction: {send_response}")

get_response = server.poll_transaction(send_response.hash)
if get_response.status != GetTransactionStatus.SUCCESS:
    raise RuntimeError(f"Transaction failed: {get_response}")

assert get_response.result_meta_xdr is not None
meta = stellar_xdr.TransactionMeta.from_xdr(get_response.result_meta_xdr)
body = meta.v4 if meta.v4 is not None else meta.v3
assert body is not None and body.soroban_meta is not None
assert body.soroban_meta.return_value is not None
print(
    f"Transaction success, result: {scval.from_uint32(body.soroban_meta.return_value)}"
)
